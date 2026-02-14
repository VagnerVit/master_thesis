"""MediaPipe Pose configuration and constants"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class MediaPipeConfig:
    """Configuration for MediaPipe Pose estimation"""

    # Model complexity: 0, 1, or 2 (higher = more accurate but slower)
    model_complexity: int = 2

    # Minimum confidence for detection
    min_detection_confidence: float = 0.7

    # Minimum confidence for tracking
    min_tracking_confidence: float = 0.7

    # Enable segmentation mask (useful for underwater/background separation)
    enable_segmentation: bool = False

    # Smooth landmarks across frames
    smooth_landmarks: bool = True

    # Static image mode (False for video streams)
    static_image_mode: bool = False


# MediaPipe Pose landmark indices
class PoseLandmark:
    """MediaPipe Pose landmark indices (33 keypoints)"""

    # Face
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10

    # Upper body
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    # Hands
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22

    # Lower body
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


# Landmark connections for visualization (skeleton lines)
POSE_CONNECTIONS = [
    # Face
    (PoseLandmark.LEFT_EYE, PoseLandmark.RIGHT_EYE),
    (PoseLandmark.LEFT_EAR, PoseLandmark.LEFT_EYE),
    (PoseLandmark.RIGHT_EAR, PoseLandmark.RIGHT_EYE),
    (PoseLandmark.MOUTH_LEFT, PoseLandmark.MOUTH_RIGHT),

    # Torso
    (PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER),
    (PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP),
    (PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_HIP),
    (PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP),

    # Left arm
    (PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW),
    (PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_WRIST),
    (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_PINKY),
    (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_INDEX),
    (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_THUMB),

    # Right arm
    (PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW),
    (PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_WRIST),
    (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_PINKY),
    (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_INDEX),
    (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_THUMB),

    # Left leg
    (PoseLandmark.LEFT_HIP, PoseLandmark.LEFT_KNEE),
    (PoseLandmark.LEFT_KNEE, PoseLandmark.LEFT_ANKLE),
    (PoseLandmark.LEFT_ANKLE, PoseLandmark.LEFT_HEEL),
    (PoseLandmark.LEFT_ANKLE, PoseLandmark.LEFT_FOOT_INDEX),

    # Right leg
    (PoseLandmark.RIGHT_HIP, PoseLandmark.RIGHT_KNEE),
    (PoseLandmark.RIGHT_KNEE, PoseLandmark.RIGHT_ANKLE),
    (PoseLandmark.RIGHT_ANKLE, PoseLandmark.RIGHT_HEEL),
    (PoseLandmark.RIGHT_ANKLE, PoseLandmark.RIGHT_FOOT_INDEX),
]


# Swimming-specific landmark groups
SWIMMING_LANDMARKS = {
    "arms": [
        PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER,
        PoseLandmark.LEFT_ELBOW, PoseLandmark.RIGHT_ELBOW,
        PoseLandmark.LEFT_WRIST, PoseLandmark.RIGHT_WRIST,
    ],
    "torso": [
        PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER,
        PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP,
    ],
    "legs": [
        PoseLandmark.LEFT_HIP, PoseLandmark.RIGHT_HIP,
        PoseLandmark.LEFT_KNEE, PoseLandmark.RIGHT_KNEE,
        PoseLandmark.LEFT_ANKLE, PoseLandmark.RIGHT_ANKLE,
    ],
}


def get_confidence_color(confidence: float) -> Tuple[int, int, int]:
    """Get RGB color based on confidence level

    Args:
        confidence: Confidence value (0.0 to 1.0)

    Returns:
        RGB color tuple (0-255 range)
    """
    if confidence >= 0.8:
        return (0, 255, 0)  # Green - high confidence
    elif confidence >= 0.6:
        return (255, 255, 0)  # Yellow - medium confidence
    else:
        return (255, 0, 0)  # Red - low confidence
