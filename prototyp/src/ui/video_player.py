"""Video player widget with pose estimation overlay"""

from pathlib import Path
from typing import Optional
import numpy as np
import cv2

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QImage, QPixmap

from ..core.video_processor import VideoProcessor
from ..core.pose_estimator import PoseEstimator, PoseResult
from ..core.frame_buffer import FrameBuffer, Frame
from ..models.mediapipe_config import MediaPipeConfig, POSE_CONNECTIONS, get_confidence_color
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class PoseProcessingThread(QThread):
    """Thread for pose estimation processing"""

    pose_result_ready = Signal(object, object)  # (frame, pose_result)

    def __init__(self, frame_buffer: FrameBuffer):
        super().__init__()
        self.frame_buffer = frame_buffer
        self.pose_estimator: Optional[PoseEstimator] = None
        self._running = False

    def run(self):
        """Process frames from buffer"""
        self.pose_estimator = PoseEstimator(MediaPipeConfig())
        if not self.pose_estimator.initialize():
            logger.error("Failed to initialize pose estimator in thread")
            return

        self._running = True
        logger.info("Pose processing thread started")

        try:
            while self._running:
                # Get frame from buffer
                frame = self.frame_buffer.get(block=True, timeout=1.0)

                if frame is None:  # Sentinel value or timeout
                    continue

                # Run pose estimation
                pose_result = self.pose_estimator.process_frame(
                    frame.data,
                    frame.frame_number,
                    frame.timestamp
                )

                # Emit result
                if pose_result:
                    self.pose_result_ready.emit(frame, pose_result)

        except Exception as e:
            if self._running:
                logger.error(f"Error in pose processing thread: {e}", exc_info=True)
        finally:
            if self.pose_estimator:
                self.pose_estimator.close()
            logger.info("Pose processing thread stopped")

    def stop(self):
        """Stop processing"""
        self._running = False


class VideoPlayer(QWidget):
    """Video player widget with pose estimation overlay"""

    video_opened = Signal(dict)  # Emits video info
    playback_state_changed = Signal(str)  # playing, paused, stopped
    video_progress = Signal(int, int)  # (current_frame, total_frames)
    video_ended = Signal()  # Emitted when video reaches end

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.video_processor: Optional[VideoProcessor] = None
        self.frame_buffer: Optional[FrameBuffer] = None
        self.pose_thread: Optional[PoseProcessingThread] = None

        self.current_frame: Optional[np.ndarray] = None
        self.current_pose: Optional[PoseResult] = None

        self._playback_state = "stopped"  # stopped, playing, paused
        self._collected_keypoints: list = []  # Collected keypoints for analysis

        self._init_ui()
        self._setup_timer()

        logger.info("Video player initialized")

    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("QLabel { background-color: black; }")
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setText("No video loaded")
        self.video_label.setStyleSheet("QLabel { color: white; background-color: black; font-size: 18px; }")

        layout.addWidget(self.video_label)

    def _setup_timer(self):
        """Setup display timer"""
        self.display_timer = QTimer(self)
        self.display_timer.timeout.connect(self._update_display)
        self.display_timer.setInterval(33)  # ~30 FPS

    def open_video(self, video_path: Path) -> bool:
        """Open video file

        Args:
            video_path: Path to video file

        Returns:
            True if successfully opened
        """
        # Cleanup existing resources
        self.cleanup()

        # Create frame buffer
        self.frame_buffer = FrameBuffer(maxsize=30)

        # Create video processor
        self.video_processor = VideoProcessor(
            video_path=video_path,
            frame_buffer=self.frame_buffer,
            target_fps=30,
            target_size=(640, 480),
            normalize=False  # Keep uint8 for display
        )

        # Open video
        if not self.video_processor.open():
            return False

        # Emit video info
        video_info = {
            "width": self.video_processor.width,
            "height": self.video_processor.height,
            "fps": self.video_processor.fps,
            "duration": self.video_processor.duration,
            "total_frames": self.video_processor.total_frames,
        }
        self.video_opened.emit(video_info)

        # Show first frame as preview
        self._show_first_frame_preview(video_path)

        logger.info(f"Video opened: {video_path.name}")
        return True

    def play(self):
        """Start video playback"""
        if self.video_processor is None:
            logger.warning("No video loaded")
            return

        # Resume if paused, otherwise start fresh
        if self._playback_state == "paused":
            self.video_processor.resume()
        else:
            if not self.video_processor.start():
                logger.error("Failed to start video processor")
                return

        # Start pose processing thread only if not running
        if self.pose_thread is None or not self.pose_thread.isRunning():
            self.pose_thread = PoseProcessingThread(self.frame_buffer)
            self.pose_thread.pose_result_ready.connect(self._on_pose_result_ready)
            self.pose_thread.start()

        # Start display timer
        self.display_timer.start()

        self._playback_state = "playing"
        self.playback_state_changed.emit("playing")

        logger.info("Playback started")

    def pause(self):
        """Pause playback"""
        if self.video_processor:
            self.video_processor.pause()

        # Stop pose thread on pause to avoid stale frames
        if self.pose_thread:
            self.pose_thread.stop()
            self.pose_thread.wait(2000)
            self.pose_thread = None

        self.display_timer.stop()

        self._playback_state = "paused"
        self.playback_state_changed.emit("paused")

        logger.info("Playback paused")

    def stop(self):
        """Stop playback"""
        self.cleanup()

        self._playback_state = "stopped"
        self.playback_state_changed.emit("stopped")

        logger.info("Playback stopped")

    def replay(self):
        """Replay video from beginning"""
        if self.video_processor is None:
            return

        logger.info("Replaying video")

        # Save path BEFORE stop() clears video_processor
        video_path = self.video_processor.video_path
        self.stop()

        # Reopen video and play
        if video_path:
            self.open_video(video_path)
            self.play()

    def seek(self, position: float):
        """Seek to position in video

        Args:
            position: Normalized position (0.0 to 1.0)
        """
        if self.video_processor is None:
            return

        was_playing = self._playback_state == "playing"
        if was_playing:
            self.pause()

        # Clear cached frames to prevent old frames from showing
        self.current_frame = None
        self.current_pose = None

        # Clear frame buffer
        if self.frame_buffer:
            self.frame_buffer.clear()

        self.video_processor.seek_to_position(position)
        logger.debug(f"Seeked to position {position:.2f}")

        if was_playing:
            self.play()

    def get_progress(self) -> tuple:
        """Get current playback progress

        Returns:
            (current_frame, total_frames)
        """
        if self.video_processor is None:
            return (0, 0)
        return (
            self.video_processor.current_frame_number,
            self.video_processor.total_frames
        )

    def cleanup(self):
        """Cleanup resources"""
        # Stop display timer
        if hasattr(self, "display_timer"):
            self.display_timer.stop()

        # Stop video processor
        if self.video_processor:
            self.video_processor.stop()
            self.video_processor = None

        # Stop pose thread
        if self.pose_thread:
            self.pose_thread.stop()
            self.pose_thread.wait(5000)
            self.pose_thread = None

        # Clear buffer
        if self.frame_buffer:
            self.frame_buffer.close()
            self.frame_buffer = None

        # Clear display
        self.current_frame = None
        self.current_pose = None

        # Reset video label to empty state
        self.video_label.clear()
        self.video_label.setText("No video loaded")

    def _show_first_frame_preview(self, video_path: Path) -> None:
        """Show first frame as preview thumbnail"""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create QImage and display
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            frame_rgb.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)
        logger.debug("First frame preview displayed")

    def _on_pose_result_ready(self, frame: Frame, pose_result: PoseResult):
        """Handle pose result from processing thread

        Args:
            frame: Frame data
            pose_result: Pose estimation result
        """
        self.current_frame = frame.data
        self.current_pose = pose_result

        # Collect keypoints for analysis
        if pose_result and pose_result.detected:
            kp_array = np.array([[kp.x, kp.y, kp.visibility] for kp in pose_result.keypoints])
            self._collected_keypoints.append(kp_array)

    def _update_display(self):
        """Update video display"""
        if self.current_frame is None:
            # Check if video ended
            if self.video_processor and self._playback_state == "playing":
                current, total = self.get_progress()
                if current >= total - 1 and total > 0:
                    self._playback_state = "stopped"
                    self.playback_state_changed.emit("stopped")
                    self.video_ended.emit()
                    self.display_timer.stop()
                    logger.info("Video ended")
            return

        # Emit progress
        if self.video_processor:
            current, total = self.get_progress()
            self.video_progress.emit(current, total)

        # Create display frame
        display_frame = self.current_frame.copy()

        # Draw pose overlay
        if self.current_pose and self.current_pose.detected:
            display_frame = self._draw_pose_overlay(display_frame, self.current_pose)

        # Convert to QImage
        height, width, channel = display_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            display_frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )

        # Display
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)

    def _draw_pose_overlay(self, frame: np.ndarray, pose_result: PoseResult) -> np.ndarray:
        """Draw pose keypoints and connections

        Args:
            frame: RGB frame
            pose_result: Pose estimation result

        Returns:
            Frame with overlay
        """
        height, width = frame.shape[:2]

        # Convert keypoints to pixel coordinates
        pixel_keypoints = []
        for kp in pose_result.keypoints:
            px = int(kp.x * width)
            py = int(kp.y * height)
            pixel_keypoints.append((px, py, kp.visibility, kp.landmark_id))

        # Filter reflections: ignore points in top 50% of image (water surface)
        reflection_cutoff = 0.50

        # Draw connections
        for connection in POSE_CONNECTIONS:
            start_idx, end_idx = connection

            if start_idx >= len(pixel_keypoints) or end_idx >= len(pixel_keypoints):
                continue

            start_x, start_y, start_vis, _ = pixel_keypoints[start_idx]
            end_x, end_y, end_vis, _ = pixel_keypoints[end_idx]

            # Skip points in reflection zone (top of image)
            start_y_norm = start_y / height
            end_y_norm = end_y / height
            if start_y_norm < reflection_cutoff or end_y_norm < reflection_cutoff:
                continue

            # Draw if both points detected (low threshold for underwater visibility)
            if start_vis > 0.1 and end_vis > 0.1:
                color = get_confidence_color(min(start_vis, end_vis))
                cv2.line(frame, (start_x, start_y), (end_x, end_y), color, 2)

        # Draw keypoints
        for px, py, vis, _ in pixel_keypoints:
            py_norm = py / height
            # Skip points in reflection zone
            if py_norm < reflection_cutoff:
                continue
            if vis > 0.1:
                color = get_confidence_color(vis)
                cv2.circle(frame, (px, py), 4, color, -1)
                cv2.circle(frame, (px, py), 5, (255, 255, 255), 1)  # White border

        return frame

    def get_collected_keypoints(self) -> Optional[np.ndarray]:
        """Get collected keypoints as numpy array

        Returns:
            Keypoints array [num_frames, num_keypoints, 3] or None if no data
        """
        if not self._collected_keypoints:
            return None
        return np.array(self._collected_keypoints)

    def clear_keypoints(self) -> None:
        """Clear collected keypoints"""
        self._collected_keypoints = []
        logger.debug("Keypoints cleared")

    def get_keypoint_count(self) -> int:
        """Get number of collected keypoint frames

        Returns:
            Number of frames with keypoints
        """
        return len(self._collected_keypoints)
