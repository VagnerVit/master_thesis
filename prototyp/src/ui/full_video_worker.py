"""Worker for processing entire video and running analysis"""

from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal

from ..core.pose_estimator import PoseEstimator
from ..models.mediapipe_config import MediaPipeConfig
from ..analysis.stroke_analyzer import StrokeAnalyzer, AnalysisResult
from ..analysis.feedback_generator import FeedbackGenerator, Feedback
from ..utils.logging_config import get_logger

logger = get_logger(__name__)

DEFAULT_REFERENCE_PATH = Path(__file__).parent.parent.parent / "models" / "freestyle_reference.json"


class FullVideoAnalysisWorker(QThread):
    """Worker that processes entire video and runs analysis

    Unlike real-time analysis, this processes the video as fast as possible
    without waiting for playback.
    """

    analysis_complete = Signal(object)  # Feedback
    progress = Signal(int)  # 0-100
    status_update = Signal(str)  # Text status message
    error = Signal(str)

    def __init__(
        self,
        video_path: Path,
        style: str = "freestyle",
        reference_path: Optional[Path] = None,
        skip_frames: int = 2,
        parent=None
    ):
        """Initialize worker

        Args:
            video_path: Path to video file
            style: Swimming style to analyze
            reference_path: Path to reference JSON (optional)
            skip_frames: Process every Nth frame (1=all, 2=every other, etc.)
            parent: Parent QObject
        """
        super().__init__(parent)
        self._video_path = Path(video_path)
        self._style = style
        self._reference_path = reference_path or DEFAULT_REFERENCE_PATH
        self._skip_frames = max(1, skip_frames)
        self._cancelled = False

    def run(self) -> None:
        """Process entire video and run analysis"""
        try:
            # Open video
            cap = cv2.VideoCapture(str(self._video_path))
            if not cap.isOpened():
                self.error.emit(f"Nepodařilo se otevřít video: {self._video_path.name}")
                return

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            logger.info(f"Processing video: {total_frames} frames, {fps:.1f} FPS")

            self.status_update.emit(f"Video načteno: {total_frames} snímků")

            # Initialize pose estimator
            pose_estimator = PoseEstimator(MediaPipeConfig())
            if not pose_estimator.initialize():
                self.error.emit("Nepodařilo se inicializovat pose estimator")
                cap.release()
                return

            self.progress.emit(5)
            self.status_update.emit("Zpracování snímků...")

            # Collect keypoints
            keypoints_list = []
            frame_number = 0

            while not self._cancelled:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_number += 1

                # Skip frames for speed
                if frame_number % self._skip_frames != 0:
                    continue

                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Run pose estimation
                timestamp = frame_number / fps if fps > 0 else 0.0
                pose_result = pose_estimator.process_frame(frame_rgb, frame_number, timestamp)

                if pose_result and pose_result.detected:
                    kp_array = np.array([[kp.x, kp.y, kp.visibility] for kp in pose_result.keypoints])
                    keypoints_list.append(kp_array)

                # Update progress (0-60% for video processing)
                progress_pct = int(5 + (frame_number / total_frames) * 55)
                self.progress.emit(min(60, progress_pct))

                # Update status every 10%
                if frame_number % max(1, total_frames // 10) == 0:
                    self.status_update.emit(f"Snímek {frame_number}/{total_frames}")

            cap.release()
            pose_estimator.close()

            if self._cancelled:
                return

            logger.info(f"Collected {len(keypoints_list)} keypoint frames")
            self.status_update.emit(f"Detekováno {len(keypoints_list)} póz")

            if len(keypoints_list) < 30:
                self.error.emit(
                    f"Nedostatek detekovaných póz ({len(keypoints_list)} framů).\n"
                    "Video možná neobsahuje viditelnou osobu."
                )
                return

            self.progress.emit(65)

            # Convert to numpy array (MediaPipe format: [N, 33, 3])
            keypoints = np.array(keypoints_list)
            logger.info(f"Keypoints shape: {keypoints.shape}")

            self.progress.emit(70)
            self.status_update.emit("Analýza techniky...")

            # Run analysis directly on MediaPipe keypoints
            analyzer = StrokeAnalyzer(self._reference_path if self._reference_path.exists() else None)
            result: AnalysisResult = analyzer.analyze(keypoints, style=self._style)

            self.progress.emit(85)

            if self._cancelled:
                return

            logger.info(f"Analysis complete: {result.num_cycles} cycles, score={result.overall_score:.1f}")
            self.status_update.emit(f"Nalezeno {result.num_cycles} cyklů")

            # Generate feedback
            self.progress.emit(90)
            self.status_update.emit("Generování zpětné vazby...")
            generator = FeedbackGenerator(language="cs")
            feedback: Feedback = generator.generate(result)

            self.progress.emit(100)
            self.status_update.emit("Analýza dokončena")
            self.analysis_complete.emit(feedback)

        except Exception as e:
            logger.error(f"Full video analysis failed: {e}", exc_info=True)
            self.error.emit(f"Analýza selhala: {str(e)}")

    def cancel(self) -> None:
        """Cancel the analysis"""
        self._cancelled = True
        logger.info("Full video analysis cancelled")
