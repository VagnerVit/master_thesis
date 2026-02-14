"""Joint angle calculation directly from MediaPipe keypoints

Calculates anatomically correct joint angles without format conversion.
Uses MediaPipe Pose landmarks (33 keypoints) directly.

MediaPipe landmark indices:
    11-12: shoulders, 13-14: elbows, 15-16: wrists
    23-24: hips, 25-26: knees, 27-28: ankles
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


class MP:
    """MediaPipe Pose landmark indices"""
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28


# Joint definitions: (point1, vertex, point2) - angle measured at vertex
JOINT_DEFINITIONS: Dict[str, Tuple[int, int, int]] = {
    # Elbows: shoulder → elbow → wrist
    'left_elbow': (MP.LEFT_SHOULDER, MP.LEFT_ELBOW, MP.LEFT_WRIST),
    'right_elbow': (MP.RIGHT_SHOULDER, MP.RIGHT_ELBOW, MP.RIGHT_WRIST),

    # Shoulders: elbow → shoulder → hip
    'left_shoulder': (MP.LEFT_ELBOW, MP.LEFT_SHOULDER, MP.LEFT_HIP),
    'right_shoulder': (MP.RIGHT_ELBOW, MP.RIGHT_SHOULDER, MP.RIGHT_HIP),

    # Knees: hip → knee → ankle
    'left_knee': (MP.LEFT_HIP, MP.LEFT_KNEE, MP.LEFT_ANKLE),
    'right_knee': (MP.RIGHT_HIP, MP.RIGHT_KNEE, MP.RIGHT_ANKLE),

    # Hips: shoulder → hip → knee
    'left_hip': (MP.LEFT_SHOULDER, MP.LEFT_HIP, MP.LEFT_KNEE),
    'right_hip': (MP.RIGHT_SHOULDER, MP.RIGHT_HIP, MP.RIGHT_KNEE),
}

JOINT_NAMES = list(JOINT_DEFINITIONS.keys())


def calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
    """Calculate angle at vertex p2 between vectors p1-p2 and p2-p3

    Args:
        p1: First point [x, y] or [x, y, z]
        p2: Vertex point (where angle is measured)
        p3: Third point

    Returns:
        Angle in degrees (0-180)
    """
    v1 = p1[:2] - p2[:2]  # Use only x, y
    v2 = p3[:2] - p2[:2]

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 < 1e-8 or norm2 < 1e-8:
        return 0.0

    cos_angle = np.dot(v1, v2) / (norm1 * norm2)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_angle)))


def get_joint_angle(keypoints: np.ndarray, joint_name: str) -> Optional[float]:
    """Calculate angle for a named joint from MediaPipe keypoints

    Args:
        keypoints: MediaPipe keypoints [33, 3] (x, y, visibility)
        joint_name: Name from JOINT_DEFINITIONS

    Returns:
        Angle in degrees, or None if invalid
    """
    if joint_name not in JOINT_DEFINITIONS:
        return None

    idx1, idx2, idx3 = JOINT_DEFINITIONS[joint_name]

    if keypoints.shape[0] < 33:
        return None

    return calculate_angle(
        keypoints[idx1],
        keypoints[idx2],
        keypoints[idx3]
    )


def get_all_joint_angles(keypoints: np.ndarray) -> Dict[str, float]:
    """Calculate all joint angles from MediaPipe keypoints

    Args:
        keypoints: MediaPipe keypoints [33, 3]

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
        keypoints_sequence: Array [num_frames, 33, 3]

    Returns:
        Array [num_frames, num_joints] with angles for each frame
    """
    num_frames = keypoints_sequence.shape[0]
    num_joints = len(JOINT_DEFINITIONS)

    angles = np.zeros((num_frames, num_joints), dtype=np.float32)

    for frame_idx in range(num_frames):
        frame_angles = get_all_joint_angles(keypoints_sequence[frame_idx])
        for joint_idx, joint_name in enumerate(JOINT_NAMES):
            if joint_name in frame_angles:
                angles[frame_idx, joint_idx] = frame_angles[joint_name]

    return angles


@dataclass
class JointReference:
    """Reference values for a joint angle"""
    optimal_min: float
    optimal_max: float
    name_cs: str  # Czech name


# Reference values from biomechanics literature (Maglischo 2003, Chollet 2000)
FREESTYLE_REFERENCE: Dict[str, JointReference] = {
    'left_elbow': JointReference(90, 140, "levý loket"),
    'right_elbow': JointReference(90, 140, "pravý loket"),
    'left_shoulder': JointReference(140, 180, "levé rameno"),
    'right_shoulder': JointReference(140, 180, "pravé rameno"),
    'left_knee': JointReference(150, 180, "levé koleno"),
    'right_knee': JointReference(150, 180, "pravé koleno"),
    'left_hip': JointReference(160, 180, "levý kyčel"),
    'right_hip': JointReference(160, 180, "pravý kyčel"),
}


def evaluate_angle(
    joint_name: str,
    angle: float,
    reference: Dict[str, JointReference] = FREESTYLE_REFERENCE
) -> Tuple[str, float]:
    """Evaluate if angle is within optimal range

    Args:
        joint_name: Name of joint
        angle: Measured angle in degrees
        reference: Reference dictionary

    Returns:
        Tuple of (severity, deviation)
        severity: "ok", "minor", "moderate", "severe"
        deviation: How far outside range (0 if within)
    """
    if joint_name not in reference:
        return ("ok", 0.0)

    ref = reference[joint_name]

    if ref.optimal_min <= angle <= ref.optimal_max:
        return ("ok", 0.0)

    if angle < ref.optimal_min:
        deviation = ref.optimal_min - angle
    else:
        deviation = angle - ref.optimal_max

    if deviation < 10:
        return ("minor", deviation)
    elif deviation < 20:
        return ("moderate", deviation)
    else:
        return ("severe", deviation)
