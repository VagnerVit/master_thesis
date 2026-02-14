"""Image preprocessing utilities for video frames"""

import numpy as np
import cv2
from typing import Tuple, Optional

def resize_frame(
    frame: np.ndarray,
    target_size: Tuple[int, int] = (224, 224),
    keep_aspect_ratio: bool = False
) -> np.ndarray:
    """Resize frame to target size

    Args:
        frame: Input frame (H, W, C)
        target_size: Target (width, height)
        keep_aspect_ratio: If True, pad to maintain aspect ratio

    Returns:
        Resized frame
    """
    if keep_aspect_ratio:
        h, w = frame.shape[:2]
        target_w, target_h = target_size

        # Calculate scaling factor
        scale = min(target_w / w, target_h / h)
        new_w, new_h = int(w * scale), int(h * scale)

        # Resize
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Pad to target size
        pad_w = (target_w - new_w) // 2
        pad_h = (target_h - new_h) // 2
        result = cv2.copyMakeBorder(
            resized,
            pad_h, target_h - new_h - pad_h,
            pad_w, target_w - new_w - pad_w,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )
        return result
    else:
        return cv2.resize(frame, target_size, interpolation=cv2.INTER_LINEAR)


def normalize_frame(
    frame: np.ndarray,
    method: str = "zero_center"
) -> np.ndarray:
    """Normalize frame pixel values

    Args:
        frame: Input frame (H, W, C) with values 0-255
        method: Normalization method
            - "zero_center": X / X.max() → [0, 1]
            - "standard": (X - mean) / std → centered
            - "imagenet": ImageNet-style normalization

    Returns:
        Normalized frame (float32)
    """
    frame_float = frame.astype(np.float32)

    if method == "zero_center":
        max_val = frame_float.max()
        if max_val > 0:
            return frame_float / max_val
        return frame_float

    elif method == "standard":
        mean = frame_float.mean()
        std = frame_float.std()
        if std > 0:
            return (frame_float - mean) / std
        return frame_float - mean

    elif method == "imagenet":
        # ImageNet mean and std (BGR order for OpenCV)
        mean = np.array([103.939, 116.779, 123.68], dtype=np.float32)
        std = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        return (frame_float - mean) / std

    else:
        raise ValueError(f"Unknown normalization method: {method}")


def convert_color(
    frame: np.ndarray,
    src_format: str = "BGR",
    dst_format: str = "RGB"
) -> np.ndarray:
    """Convert frame color format

    Args:
        frame: Input frame
        src_format: Source format (BGR, RGB, GRAY)
        dst_format: Destination format (BGR, RGB, GRAY)

    Returns:
        Converted frame
    """
    if src_format == dst_format:
        return frame

    conversion_map = {
        ("BGR", "RGB"): cv2.COLOR_BGR2RGB,
        ("RGB", "BGR"): cv2.COLOR_RGB2BGR,
        ("BGR", "GRAY"): cv2.COLOR_BGR2GRAY,
        ("RGB", "GRAY"): cv2.COLOR_RGB2GRAY,
        ("GRAY", "BGR"): cv2.COLOR_GRAY2BGR,
        ("GRAY", "RGB"): cv2.COLOR_GRAY2RGB,
    }

    conversion_code = conversion_map.get((src_format, dst_format))
    if conversion_code is None:
        raise ValueError(f"Unsupported conversion: {src_format} -> {dst_format}")

    return cv2.cvtColor(frame, conversion_code)


def enhance_underwater(
    frame: np.ndarray,
    gamma: float = 1.2,
    contrast_factor: float = 1.3
) -> np.ndarray:
    """Enhance underwater footage

    Applies gamma correction and contrast enhancement to improve
    underwater video quality before pose estimation.

    Args:
        frame: Input frame (BGR, uint8)
        gamma: Gamma correction factor (>1 brightens, <1 darkens)
        contrast_factor: Contrast enhancement factor

    Returns:
        Enhanced frame (BGR, uint8)
    """
    # Gamma correction
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)
    ]).astype(np.uint8)
    frame_gamma = cv2.LUT(frame, table)

    # Contrast enhancement (CLAHE - Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(frame_gamma, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=contrast_factor, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return enhanced


def extract_multi_frame_window(
    frames: list[np.ndarray],
    window_size: int = 5
) -> Optional[np.ndarray]:
    """Extract multi-frame window for temporal analysis

    Args:
        frames: List of frames
        window_size: Number of frames to fuse

    Returns:
        Fused frames (H, W, C*window_size) or None if insufficient frames
    """
    if len(frames) < window_size:
        return None

    # Take last window_size frames
    window = frames[-window_size:]

    # Stack along channel dimension
    fused = np.concatenate(window, axis=2)

    return fused
