"""Video processing module using OpenCV

Handles video file decoding, frame extraction, and threading for real-time processing.
"""

import cv2
import threading
from pathlib import Path
from typing import Optional, Callable
import time

from .frame_buffer import FrameBuffer, Frame
from ..utils.logging_config import get_logger
from ..utils.preprocessing import resize_frame, normalize_frame, convert_color

logger = get_logger(__name__)


class VideoProcessor:
    """Video decoder and frame extractor

    Reads video file and extracts frames in separate thread.
    Pushes frames to FrameBuffer for downstream processing.
    """

    def __init__(
        self,
        video_path: Path,
        frame_buffer: FrameBuffer,
        target_fps: int = 30,
        target_size: tuple[int, int] = (224, 224),
        normalize: bool = True,
    ):
        """Initialize video processor

        Args:
            video_path: Path to video file
            frame_buffer: Buffer to push frames to
            target_fps: Target frame rate (will skip frames if needed)
            target_size: Target frame size (width, height)
            normalize: Whether to normalize frames (zero-centering)
        """
        self.video_path = Path(video_path)
        self.frame_buffer = frame_buffer
        self.target_fps = target_fps
        self.target_size = target_size
        self.normalize = normalize

        self._cap: Optional[cv2.VideoCapture] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._paused = False
        self._lock = threading.Lock()

        # Video properties
        self.total_frames: int = 0
        self.fps: float = 0.0
        self.width: int = 0
        self.height: int = 0
        self.duration: float = 0.0

        # Processing stats
        self._frames_read = 0
        self._frames_skipped = 0
        self._start_time: float = 0.0
        self._current_frame_number: int = 0

    def open(self) -> bool:
        """Open video file and read properties

        Returns:
            True if successfully opened
        """
        if not self.video_path.exists():
            logger.error(f"Video file not found: {self.video_path}")
            return False

        self._cap = cv2.VideoCapture(str(self.video_path))
        if not self._cap.isOpened():
            logger.error(f"Failed to open video: {self.video_path}")
            return False

        # Read video properties
        self.fps = self._cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps if self.fps > 0 else 0.0

        logger.info(
            f"Opened video: {self.video_path.name} "
            f"({self.width}x{self.height}, {self.fps:.2f} FPS, "
            f"{self.total_frames} frames, {self.duration:.2f}s)"
        )

        return True

    def start(self) -> bool:
        """Start video processing thread

        Returns:
            True if successfully started
        """
        if self._cap is None or not self._cap.isOpened():
            if not self.open():
                return False

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._process_loop, daemon=True)
        self._thread.start()
        self._start_time = time.time()

        logger.info("Video processing started")
        return True

    def stop(self) -> None:
        """Stop video processing thread"""
        logger.info("Stopping video processing...")
        self._stop_event.set()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)

        self._cleanup()
        logger.info("Video processing stopped")

    def pause(self) -> None:
        """Pause video processing"""
        with self._lock:
            self._paused = True
        logger.debug("Video processing paused")

    def resume(self) -> None:
        """Resume video processing"""
        with self._lock:
            self._paused = False
        logger.debug("Video processing resumed")

    def is_paused(self) -> bool:
        """Check if paused"""
        with self._lock:
            return self._paused

    @property
    def current_frame_number(self) -> int:
        """Get current frame number"""
        with self._lock:
            return self._current_frame_number

    def seek(self, frame_number: int) -> bool:
        """Seek to specific frame

        Args:
            frame_number: Target frame number (0-based)

        Returns:
            True if seek successful
        """
        if self._cap is None or not self._cap.isOpened():
            return False

        frame_number = max(0, min(frame_number, self.total_frames - 1))

        with self._lock:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            self._current_frame_number = frame_number

        logger.debug(f"Seeked to frame {frame_number}")
        return True

    def seek_to_position(self, position: float) -> bool:
        """Seek to position (0.0 to 1.0)

        Args:
            position: Normalized position (0.0 = start, 1.0 = end)

        Returns:
            True if seek successful
        """
        frame_number = int(position * self.total_frames)
        return self.seek(frame_number)

    def _process_loop(self) -> None:
        """Main processing loop (runs in separate thread)"""
        frame_interval = 1.0 / self.target_fps if self.target_fps > 0 else 0.0
        source_frame_interval = 1.0 / self.fps if self.fps > 0 else 0.0

        # Calculate skip factor
        skip_factor = max(1, int(source_frame_interval / frame_interval)) if frame_interval > 0 else 1

        frame_number = 0
        last_process_time = 0.0

        try:
            while not self._stop_event.is_set():
                # Check if paused
                if self.is_paused():
                    time.sleep(0.1)
                    continue

                # Read frame
                ret, raw_frame = self._cap.read()
                if not ret:
                    logger.info("End of video reached")
                    break

                frame_number += 1
                with self._lock:
                    self._current_frame_number = frame_number
                timestamp = frame_number / self.fps if self.fps > 0 else 0.0

                # Skip frames to match target FPS
                if frame_number % skip_factor != 0:
                    self._frames_skipped += 1
                    continue

                # Preprocess frame
                try:
                    processed_frame = self._preprocess_frame(raw_frame)
                except Exception as e:
                    logger.error(f"Frame preprocessing failed at frame {frame_number}: {e}")
                    continue

                # Create Frame object
                frame = Frame(
                    data=processed_frame,
                    frame_number=frame_number,
                    timestamp=timestamp,
                    processed=True
                )

                # Push to buffer (with timeout to avoid indefinite blocking)
                try:
                    success = self.frame_buffer.put(frame, block=True, timeout=1.0)
                    if success:
                        self._frames_read += 1
                    else:
                        logger.warning(f"Frame buffer full, dropped frame {frame_number}")
                except Exception as e:
                    logger.error(f"Failed to push frame {frame_number}: {e}")

                # Rate limiting (optional, for real-time playback)
                current_time = time.time()
                elapsed = current_time - last_process_time
                if frame_interval > 0 and elapsed < frame_interval:
                    time.sleep(frame_interval - elapsed)
                last_process_time = current_time

        except Exception as e:
            logger.error(f"Error in processing loop: {e}", exc_info=True)
        finally:
            self.frame_buffer.close()
            logger.info(
                f"Processing finished: {self._frames_read} frames read, "
                f"{self._frames_skipped} frames skipped"
            )

    def _preprocess_frame(self, frame: cv2.Mat) -> cv2.Mat:
        """Preprocess frame (resize, normalize, color conversion)

        Args:
            frame: Raw frame from OpenCV (BGR, uint8)

        Returns:
            Preprocessed frame
        """
        # Convert BGR to RGB (MediaPipe expects RGB)
        frame_rgb = convert_color(frame, src_format="BGR", dst_format="RGB")

        # Resize
        frame_resized = resize_frame(frame_rgb, target_size=self.target_size)

        # Normalize
        if self.normalize:
            frame_normalized = normalize_frame(frame_resized, method="zero_center")
            # Convert back to uint8 for visualization
            frame_final = (frame_normalized * 255).astype("uint8")
        else:
            frame_final = frame_resized

        return frame_final

    def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def get_stats(self) -> dict:
        """Get processing statistics

        Returns:
            Dictionary with stats
        """
        elapsed = time.time() - self._start_time if self._start_time > 0 else 0.0
        actual_fps = self._frames_read / elapsed if elapsed > 0 else 0.0

        return {
            "frames_read": self._frames_read,
            "frames_skipped": self._frames_skipped,
            "total_frames": self.total_frames,
            "progress": self._frames_read / self.total_frames if self.total_frames > 0 else 0.0,
            "elapsed_time": elapsed,
            "actual_fps": actual_fps,
            "buffer_stats": self.frame_buffer.get_stats(),
        }

    def __enter__(self):
        """Context manager entry"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
