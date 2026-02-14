"""Joint angle calculation utilities for swimming analysis

Calculates joint angles from SwimXYZ keypoint sequences (48 keypoints, base format).

SwimXYZ Base Keypoint Indices (48 keypoints):
    0: Pelvis
    1: Head
    2: HeadNub
    3-20: Left side (L_Calf, L_Clavicle, L_Finger0-4, L_Foot, L_Forearm, L_Hand,
                     L_Thigh, L_Heel, L_Toe0-4, L_UpperArm)
    21: Neck
    22-39: Right side (same structure as left)
    40-42: Spine1, Spine2, Spine
    43-47: Ear_L, Ear_R, Eye_L, Eye_R, Nose
"""

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np


# SwimXYZ Base format keypoint indices (48 keypoints)
@dataclass(frozen=True)
class SwimXYZKeypoints:
    """Keypoint indices for SwimXYZ base format (48 keypoints)"""
    # Core
    PELVIS: int = 0
    HEAD: int = 1
    HEAD_NUB: int = 2
    NECK: int = 21

    # Left side
    L_CALF: int = 3
    L_CLAVICLE: int = 4
    L_FINGER0: int = 5
    L_FINGER1: int = 6
    L_FINGER2: int = 7
    L_FINGER3: int = 8
    L_FINGER4: int = 9
    L_FOOT: int = 10
    L_FOREARM: int = 11
    L_HAND: int = 12
    L_THIGH: int = 13
    L_HEEL: int = 14
    L_TOE0: int = 15
    L_TOE1: int = 16
    L_TOE2: int = 17
    L_TOE3: int = 18
    L_TOE4: int = 19
    L_UPPER_ARM: int = 20

    # Right side
    R_CALF: int = 22
    R_CLAVICLE: int = 23
    R_FINGER0: int = 24
    R_FINGER1: int = 25
    R_FINGER2: int = 26
    R_FINGER3: int = 27
    R_FINGER4: int = 28
    R_FOOT: int = 29
    R_FOREARM: int = 30
    R_HAND: int = 31
    R_THIGH: int = 32
    R_HEEL: int = 33
    R_TOE0: int = 34
    R_TOE1: int = 35
    R_TOE2: int = 36
    R_TOE3: int = 37
    R_TOE4: int = 38
    R_UPPER_ARM: int = 39

    # Spine
    SPINE1: int = 40
    SPINE2: int = 41
    SPINE: int = 42

    # Face
    EAR_L: int = 43
    EAR_R: int = 44
    EYE_L: int = 45
    EYE_R: int = 46
    NOSE: int = 47


KP = SwimXYZKeypoints()


# Joint definitions: (point1, vertex, point2) for angle calculation
JOINT_DEFINITIONS = {
    # Elbows: upper_arm -> forearm -> hand
    'left_elbow': (KP.L_UPPER_ARM, KP.L_FOREARM, KP.L_HAND),
    'right_elbow': (KP.R_UPPER_ARM, KP.R_FOREARM, KP.R_HAND),

    # Shoulders: neck -> clavicle -> upper_arm
    'left_shoulder': (KP.NECK, KP.L_CLAVICLE, KP.L_UPPER_ARM),
    'right_shoulder': (KP.NECK, KP.R_CLAVICLE, KP.R_UPPER_ARM),

    # Knees: thigh -> calf -> foot
    'left_knee': (KP.L_THIGH, KP.L_CALF, KP.L_FOOT),
    'right_knee': (KP.R_THIGH, KP.R_CALF, KP.R_FOOT),

    # Hips: spine -> pelvis -> thigh
    'left_hip': (KP.SPINE, KP.PELVIS, KP.L_THIGH),
    'right_hip': (KP.SPINE, KP.PELVIS, KP.R_THIGH),

    # Body alignment: head -> spine -> pelvis
    'body_alignment': (KP.HEAD, KP.SPINE2, KP.PELVIS),

    # Arm extension: clavicle -> upper_arm -> forearm
    'left_arm_extension': (KP.L_CLAVICLE, KP.L_UPPER_ARM, KP.L_FOREARM),
    'right_arm_extension': (KP.R_CLAVICLE, KP.R_UPPER_ARM, KP.R_FOREARM),
}


def calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
    """Calculate angle at vertex p2 between vectors p1-p2 and p2-p3

    Args:
        p1: First point [x, y, z] or [x, y]
        p2: Vertex point (where angle is measured)
        p3: Third point

    Returns:
        Angle in degrees (0-180)
    """
    v1 = p1 - p2
    v2 = p3 - p2

    # Handle zero vectors
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 < 1e-8 or norm2 < 1e-8:
        return 0.0

    cos_angle = np.dot(v1, v2) / (norm1 * norm2)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_angle)))


def get_joint_angle(
    keypoints: np.ndarray,
    joint_name: str
) -> Optional[float]:
    """Calculate angle for a named joint

    Args:
        keypoints: Keypoint array of shape [num_keypoints, dims] or [num_keypoints, 3]
        joint_name: Name from JOINT_DEFINITIONS

    Returns:
        Angle in degrees, or None if joint not found
    """
    if joint_name not in JOINT_DEFINITIONS:
        return None

    idx1, idx2, idx3 = JOINT_DEFINITIONS[joint_name]

    # Validate indices
    if max(idx1, idx2, idx3) >= keypoints.shape[0]:
        return None

    return calculate_angle(
        keypoints[idx1],
        keypoints[idx2],
        keypoints[idx3]
    )


def get_all_joint_angles(keypoints: np.ndarray) -> Dict[str, float]:
    """Calculate all swimming-relevant joint angles

    Args:
        keypoints: Keypoint array of shape [num_keypoints, dims]

    Returns:
        Dictionary of joint_name -> angle_in_degrees
    """
    angles: Dict[str, float] = {}

    for joint_name in JOINT_DEFINITIONS:
        angle = get_joint_angle(keypoints, joint_name)
        if angle is not None:
            angles[joint_name] = angle

    return angles


def get_sequence_angles(keypoints_sequence: np.ndarray) -> np.ndarray:
    """Calculate joint angles for a sequence of frames

    Args:
        keypoints_sequence: Array of shape [num_frames, num_keypoints, dims]

    Returns:
        Array of shape [num_frames, num_joints] with angles for each frame
    """
    num_frames = keypoints_sequence.shape[0]
    joint_names = list(JOINT_DEFINITIONS.keys())
    num_joints = len(joint_names)

    angles = np.zeros((num_frames, num_joints), dtype=np.float32)

    for frame_idx in range(num_frames):
        frame_angles = get_all_joint_angles(keypoints_sequence[frame_idx])
        for joint_idx, joint_name in enumerate(joint_names):
            if joint_name in frame_angles:
                angles[frame_idx, joint_idx] = frame_angles[joint_name]

    return angles


def get_joint_names() -> list:
    """Get list of joint names in order"""
    return list(JOINT_DEFINITIONS.keys())


@dataclass
class AngleStatistics:
    """Statistics for joint angles"""
    mean: float
    std: float
    min_val: float
    max_val: float
    median: float

    def to_dict(self) -> Dict[str, float]:
        return {
            'mean': round(self.mean, 2),
            'std': round(self.std, 2),
            'min': round(self.min_val, 2),
            'max': round(self.max_val, 2),
            'median': round(self.median, 2)
        }


def compute_angle_statistics(angles: np.ndarray) -> AngleStatistics:
    """Compute statistics for angle array

    Args:
        angles: 1D array of angle values

    Returns:
        AngleStatistics with mean, std, min, max, median
    """
    # Filter out zeros (invalid angles)
    valid_angles = angles[angles > 0]

    if len(valid_angles) == 0:
        return AngleStatistics(0.0, 0.0, 0.0, 0.0, 0.0)

    return AngleStatistics(
        mean=float(np.mean(valid_angles)),
        std=float(np.std(valid_angles)),
        min_val=float(np.min(valid_angles)),
        max_val=float(np.max(valid_angles)),
        median=float(np.median(valid_angles))
    )
