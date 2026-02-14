"""Swimming stroke analysis module

Provides tools for analyzing swimming technique:
- DTW-based sequence comparison
- Stroke cycle detection
- Joint angle analysis
- Czech feedback generation
"""

from .dtw import dtw_distance, dtw_similarity, DTWResult
from .stroke_analyzer import StrokeAnalyzer, AnalysisResult, StrokeCycle
from .feedback_generator import FeedbackGenerator, Feedback
from .keypoint_mapper import map_mediapipe_to_swimxyz

__all__ = [
    "dtw_distance",
    "dtw_similarity",
    "DTWResult",
    "StrokeAnalyzer",
    "AnalysisResult",
    "StrokeCycle",
    "FeedbackGenerator",
    "Feedback",
    "map_mediapipe_to_swimxyz",
]
