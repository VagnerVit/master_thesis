"""Background worker for swimming technique analysis"""

from pathlib import Path
from typing import Optional

import numpy as np
from PySide6.QtCore import QThread, Signal

from ..analysis.stroke_analyzer import StrokeAnalyzer, AnalysisResult
from ..analysis.feedback_generator import FeedbackGenerator, Feedback
from ..utils.logging_config import get_logger

logger = get_logger(__name__)

# Default reference path
DEFAULT_REFERENCE_PATH = Path(__file__).parent.parent.parent / "models" / "freestyle_reference.json"


class AnalysisWorker(QThread):
    """Worker thread for swimming technique analysis

    Runs StrokeAnalyzer and FeedbackGenerator in background
    to avoid blocking the UI.
    """

    analysis_complete = Signal(object)  # Feedback
    progress = Signal(int)  # 0-100
    error = Signal(str)

    def __init__(
        self,
        keypoints: np.ndarray,
        style: str = "freestyle",
        reference_path: Optional[Path] = None,
        parent=None
    ):
        """Initialize worker

        Args:
            keypoints: MediaPipe keypoints [num_frames, 33, 3]
            style: Swimming style to analyze
            reference_path: Path to reference JSON (optional)
            parent: Parent QObject
        """
        super().__init__(parent)
        self._keypoints = keypoints
        self._style = style
        self._reference_path = reference_path or DEFAULT_REFERENCE_PATH
        self._cancelled = False

    def run(self) -> None:
        """Execute analysis in background"""
        try:
            logger.info(f"Starting analysis: {self._keypoints.shape[0]} frames, style={self._style}")
            self.progress.emit(10)

            # Use MediaPipe keypoints directly (no conversion needed)
            keypoints = self._keypoints

            logger.debug(f"Input keypoints shape: {keypoints.shape}, dtype: {keypoints.dtype}")
            if keypoints.ndim >= 2:
                logger.debug(f"Keypoint value ranges: X=[{keypoints[:,:,0].min():.3f}, {keypoints[:,:,0].max():.3f}], "
                            f"Y=[{keypoints[:,:,1].min():.3f}, {keypoints[:,:,1].max():.3f}]")

            # Initialize analyzer (will load style-specific reference)
            ref_path = self._reference_path if self._reference_path.exists() else None
            analyzer = StrokeAnalyzer(ref_path)
            self.progress.emit(20)

            if self._cancelled:
                return

            # Run analysis
            result: AnalysisResult = analyzer.analyze(keypoints, style=self._style)
            self.progress.emit(70)

            if self._cancelled:
                return

            logger.info(f"Analysis complete: {result.num_cycles} cycles, score={result.overall_score:.1f}")

            # Generate feedback
            generator = FeedbackGenerator(language="cs")
            feedback: Feedback = generator.generate(result)
            self.progress.emit(90)

            if self._cancelled:
                return

            # Emit result
            self.progress.emit(100)
            self.analysis_complete.emit(feedback)

        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            self.error.emit(f"Analýza selhala: {str(e)}")

    def cancel(self) -> None:
        """Cancel the analysis"""
        self._cancelled = True
        logger.info("Analysis cancelled")
