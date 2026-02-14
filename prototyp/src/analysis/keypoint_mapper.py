"""Keypoint format mapper for MediaPipe to SwimXYZ conversion

Converts MediaPipe Pose landmarks (33 keypoints) to SwimXYZ-compatible
format (48 keypoints) for use with StrokeAnalyzer.

MediaPipe landmarks:
    0: nose, 1-6: eyes, 7-8: ears, 9-10: mouth
    11-12: shoulders, 13-14: elbows, 15-16: wrists
    17-22: hands (pinky, index, thumb)
    23-24: hips, 25-26: knees, 27-28: ankles
    29-30: heels, 31-32: foot indices

SwimXYZ base format (48 keypoints):
    0: pelvis, 1: head, 21: neck
    Left side: 3-calf, 4-clavicle, 10-foot, 11-forearm, 12-hand, 13-thigh, 20-upper_arm
    Right side: 22-calf, 23-clavicle, 29-foot, 30-forearm, 31-hand, 32-thigh, 39-upper_arm
    40-42: spine points
"""

import numpy as np
from typing import Optional


class MediaPipeLandmark:
    """MediaPipe Pose landmark indices"""
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
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
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


MP = MediaPipeLandmark()


def map_mediapipe_to_swimxyz(keypoints: np.ndarray) -> np.ndarray:
    """Convert MediaPipe keypoints to SwimXYZ-compatible format

    Args:
        keypoints: MediaPipe keypoints [num_frames, 33, 3] or [33, 3]

    Returns:
        SwimXYZ-compatible keypoints [num_frames, 48, 3] or [48, 3]
    """
    single_frame = keypoints.ndim == 2
    if single_frame:
        keypoints = keypoints[np.newaxis, ...]

    num_frames = keypoints.shape[0]
    dims = keypoints.shape[2] if keypoints.ndim > 2 else 3

    result = np.zeros((num_frames, 48, dims), dtype=keypoints.dtype)

    for i in range(num_frames):
        kp = keypoints[i]
        out = result[i]

        # Compute synthetic points
        pelvis = (kp[MP.LEFT_HIP] + kp[MP.RIGHT_HIP]) / 2
        neck = (kp[MP.LEFT_SHOULDER] + kp[MP.RIGHT_SHOULDER]) / 2
        spine_mid = (pelvis + neck) / 2

        # Interpolated arm points (MediaPipe has fewer points than SwimXYZ)
        l_upper_arm = (kp[MP.LEFT_SHOULDER] + kp[MP.LEFT_ELBOW]) / 2
        r_upper_arm = (kp[MP.RIGHT_SHOULDER] + kp[MP.RIGHT_ELBOW]) / 2

        # Core points
        out[0] = pelvis                                    # PELVIS
        out[1] = kp[MP.NOSE]                               # HEAD
        out[2] = kp[MP.NOSE]                               # HEAD_NUB
        out[21] = neck                                     # NECK

        # Left side
        # Shoulder angle: NECK → L_CLAVICLE(vertex=shoulder) → L_UPPER_ARM(midpoint)
        # Elbow angle: L_UPPER_ARM(midpoint) → L_FOREARM(vertex=elbow) → L_HAND(wrist)
        out[3] = kp[MP.LEFT_KNEE]                          # L_CALF (knee position)
        out[4] = kp[MP.LEFT_SHOULDER]                      # L_CLAVICLE (shoulder)
        out[10] = kp[MP.LEFT_ANKLE]                        # L_FOOT
        out[11] = kp[MP.LEFT_ELBOW]                        # L_FOREARM (elbow)
        out[12] = kp[MP.LEFT_WRIST]                        # L_HAND (wrist)
        out[13] = kp[MP.LEFT_HIP]                          # L_THIGH
        out[14] = kp[MP.LEFT_HEEL]                         # L_HEEL
        out[20] = l_upper_arm                              # L_UPPER_ARM (interpolated)

        # Left fingers (use wrist as fallback)
        for idx in range(5, 10):
            out[idx] = kp[MP.LEFT_WRIST]

        # Left toes (use foot index)
        for idx in range(15, 20):
            out[idx] = kp[MP.LEFT_FOOT_INDEX]

        # Right side (same structure as left)
        out[22] = kp[MP.RIGHT_KNEE]                        # R_CALF
        out[23] = kp[MP.RIGHT_SHOULDER]                    # R_CLAVICLE (shoulder)
        out[29] = kp[MP.RIGHT_ANKLE]                       # R_FOOT
        out[30] = kp[MP.RIGHT_ELBOW]                       # R_FOREARM (elbow)
        out[31] = kp[MP.RIGHT_WRIST]                       # R_HAND (wrist)
        out[32] = kp[MP.RIGHT_HIP]                         # R_THIGH
        out[33] = kp[MP.RIGHT_HEEL]                        # R_HEEL
        out[39] = r_upper_arm                              # R_UPPER_ARM (interpolated)

        # Right fingers
        for idx in range(24, 29):
            out[idx] = kp[MP.RIGHT_WRIST]

        # Right toes
        for idx in range(34, 39):
            out[idx] = kp[MP.RIGHT_FOOT_INDEX]

        # Spine
        out[40] = spine_mid                                # SPINE1
        out[41] = spine_mid                                # SPINE2
        out[42] = spine_mid                                # SPINE

        # Face
        out[43] = kp[MP.LEFT_EAR]                          # EAR_L
        out[44] = kp[MP.RIGHT_EAR]                         # EAR_R
        out[45] = kp[MP.LEFT_EYE]                          # EYE_L
        out[46] = kp[MP.RIGHT_EYE]                         # EYE_R
        out[47] = kp[MP.NOSE]                              # NOSE

    if single_frame:
        return result[0]

    return result


def get_mediapipe_keypoint_count() -> int:
    """Get expected MediaPipe keypoint count"""
    return 33


def get_swimxyz_keypoint_count() -> int:
    """Get SwimXYZ keypoint count"""
    return 48
