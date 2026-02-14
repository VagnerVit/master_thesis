"""Pose estimation module using MediaPipe Pose"""

import numpy as np
import mediapipe as mp
from dataclasses import dataclass
from typing import Optional, List, Any
import time

from ..models.mediapipe_config import MediaPipeConfig, PoseLandmark
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class Keypoint:
    """Single keypoint with 2D/3D coordinates and confidence"""
    x: float  # Normalized 0-1 (or pixel coords if converted)
    y: float  # Normalized 0-1 (or pixel coords if converted)
    z: float  # Depth (relative to hips)
    visibility: float  # Confidence 0-1
    landmark_id: int  # MediaPipe landmark index


@dataclass
class PoseResult:
    """Pose estimation result for a single frame"""
    keypoints: List[Keypoint]
    frame_number: int
    timestamp: float
    processing_time: float  # milliseconds
    detected: bool  # Whether pose was detected


class PoseEstimator:
    """MediaPipe Pose wrapper for swimming pose estimation"""

    def __init__(self, config: Optional[MediaPipeConfig] = None):
        """Initialize pose estimator

        Args:
            config: MediaPipe configuration (uses defaults if None)
        """
        self.config = config or MediaPipeConfig()
        self._pose: Optional[mp.solutions.pose.Pose] = None
        self._initialized = False

        # Stats
        self._total_frames = 0
        self._detected_frames = 0
        self._total_processing_time = 0.0

    def initialize(self) -> bool:
        """Initialize MediaPipe Pose model

        Returns:
            True if successfully initialized
        """
        try:
            self._pose = mp.solutions.pose.Pose(
                static_image_mode=self.config.static_image_mode,
                model_complexity=self.config.model_complexity,
                smooth_landmarks=self.config.smooth_landmarks,
                enable_segmentation=self.config.enable_segmentation,
                min_detection_confidence=self.config.min_detection_confidence,
                min_tracking_confidence=self.config.min_tracking_confidence,
            )
            self._initialized = True
            logger.info(
                f"MediaPipe Pose initialized (complexity={self.config.model_complexity}, "
                f"detection_conf={self.config.min_detection_confidence})"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe Pose: {e}")
            return False

    def process_frame(
        self,
        frame: np.ndarray,
        frame_number: int = 0,
        timestamp: float = 0.0
    ) -> Optional[PoseResult]:
        """Process single frame and extract pose keypoints

        Args:
            frame: RGB frame (H, W, 3) uint8
            frame_number: Frame index
            timestamp: Frame timestamp in seconds

        Returns:
            PoseResult or None if processing failed
        """
        if not self._initialized:
            logger.error("Pose estimator not initialized. Call initialize() first.")
            return None

        start_time = time.perf_counter()

        try:
            # Run MediaPipe Pose
            results = self._pose.process(frame)

            processing_time = (time.perf_counter() - start_time) * 1000  # ms

            self._total_frames += 1
            self._total_processing_time += processing_time

            # Check if pose detected
            if results.pose_landmarks is None:
                logger.debug(f"No pose detected in frame {frame_number}")
                return PoseResult(
                    keypoints=[],
                    frame_number=frame_number,
                    timestamp=timestamp,
                    processing_time=processing_time,
                    detected=False
                )

            # Extract keypoints
            keypoints = self._extract_keypoints(results.pose_landmarks)

            self._detected_frames += 1

            return PoseResult(
                keypoints=keypoints,
                frame_number=frame_number,
                timestamp=timestamp,
                processing_time=processing_time,
                detected=True
            )

        except Exception as e:
            logger.error(f"Error processing frame {frame_number}: {e}", exc_info=True)
            return None

    def _extract_keypoints(
        self,
        landmarks: Any
    ) -> List[Keypoint]:
        """Extract keypoints from MediaPipe landmarks

        Args:
            landmarks: MediaPipe pose landmarks

        Returns:
            List of Keypoint objects
        """
        keypoints = []

        for idx, landmark in enumerate(landmarks.landmark):
            keypoint = Keypoint(
                x=landmark.x,
                y=landmark.y,
                z=landmark.z,
                visibility=landmark.visibility,
                landmark_id=idx
            )
            keypoints.append(keypoint)

        return keypoints

    def convert_to_pixel_coords(
        self,
        keypoints: List[Keypoint],
        frame_width: int,
        frame_height: int
    ) -> List[Keypoint]:
        """Convert normalized coordinates to pixel coordinates

        Args:
            keypoints: List of keypoints with normalized coords (0-1)
            frame_width: Frame width in pixels
            frame_height: Frame height in pixels

        Returns:
            List of keypoints with pixel coordinates
        """
        pixel_keypoints = []

        for kp in keypoints:
            pixel_kp = Keypoint(
                x=kp.x * frame_width,
                y=kp.y * frame_height,
                z=kp.z,  # Keep depth as is
                visibility=kp.visibility,
                landmark_id=kp.landmark_id
            )
            pixel_keypoints.append(pixel_kp)

        return pixel_keypoints

    def filter_low_confidence(
        self,
        keypoints: List[Keypoint],
        min_confidence: float = 0.5
    ) -> List[Keypoint]:
        """Filter out keypoints with low confidence

        Args:
            keypoints: List of keypoints
            min_confidence: Minimum visibility threshold

        Returns:
            Filtered keypoints
        """
        return [kp for kp in keypoints if kp.visibility >= min_confidence]

    def get_swimming_keypoints(self, keypoints: List[Keypoint]) -> dict:
        """Extract swimming-specific keypoint groups

        Args:
            keypoints: List of all keypoints

        Returns:
            Dictionary with grouped keypoints (arms, torso, legs)
        """
        swimming_groups = {
            "arms": [],
            "torso": [],
            "legs": []
        }

        arm_indices = [
            PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER,
            PoseLandmark.LEFT_ELBOW, PoseLandmark.RIGHT_ELBOW,
            PoseLandmark.LEFT_WRIST, PoseLandmark.RIGHT_WRIST,
        ]

        torso_indices = [
            PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER,
            PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP,
        ]

        leg_indices = [
            PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP,
            PoseLandmark.LEFT_KNEE, PoseLandmark.RIGHT_KNEE,
            PoseLandmark.LEFT_ANKLE, PoseLandmark.RIGHT_ANKLE,
        ]

        for kp in keypoints:
            if kp.landmark_id in arm_indices:
                swimming_groups["arms"].append(kp)
            if kp.landmark_id in torso_indices:
                swimming_groups["torso"].append(kp)
            if kp.landmark_id in leg_indices:
                swimming_groups["legs"].append(kp)

        return swimming_groups

    def get_stats(self) -> dict:
        """Get processing statistics

        Returns:
            Dictionary with stats
        """
        avg_processing_time = (
            self._total_processing_time / self._total_frames
            if self._total_frames > 0
            else 0.0
        )

        detection_rate = (
            self._detected_frames / self._total_frames
            if self._total_frames > 0
            else 0.0
        )

        return {
            "total_frames": self._total_frames,
            "detected_frames": self._detected_frames,
            "detection_rate": detection_rate,
            "avg_processing_time_ms": avg_processing_time,
            "fps": 1000.0 / avg_processing_time if avg_processing_time > 0 else 0.0,
        }

    def close(self) -> None:
        """Release MediaPipe resources"""
        if self._pose is not None:
            self._pose.close()
            self._pose = None
            self._initialized = False
            logger.info("Pose estimator closed")

    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
