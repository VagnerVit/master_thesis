"""Unit tests for preprocessing utilities"""

import pytest
import numpy as np
import cv2

from src.utils.preprocessing import (
    resize_frame,
    normalize_frame,
    convert_color,
    enhance_underwater,
    extract_multi_frame_window
)


def test_resize_frame_basic():
    """Test basic frame resizing"""
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    resized = resize_frame(frame, target_size=(224, 224), keep_aspect_ratio=False)

    assert resized.shape == (224, 224, 3)
    assert resized.dtype == np.uint8


def test_resize_frame_keep_aspect_ratio():
    """Test resizing with aspect ratio preservation"""
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    resized = resize_frame(frame, target_size=(224, 224), keep_aspect_ratio=True)

    assert resized.shape == (224, 224, 3)
    assert resized.dtype == np.uint8


def test_normalize_frame_zero_center():
    """Test zero-center normalization"""
    frame = np.array([[[100, 150, 200]]], dtype=np.uint8)

    normalized = normalize_frame(frame, method="zero_center")

    assert normalized.dtype == np.float32
    assert normalized.max() == pytest.approx(1.0)
    assert 0.0 <= normalized.min() <= 1.0


def test_normalize_frame_standard():
    """Test standard normalization"""
    frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    normalized = normalize_frame(frame, method="standard")

    assert normalized.dtype == np.float32
    # Standard normalization should have mean ~0
    assert abs(normalized.mean()) < 1.0


def test_normalize_frame_imagenet():
    """Test ImageNet-style normalization"""
    frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    normalized = normalize_frame(frame, method="imagenet")

    assert normalized.dtype == np.float32


def test_normalize_frame_invalid_method():
    """Test invalid normalization method"""
    frame = np.zeros((10, 10, 3), dtype=np.uint8)

    with pytest.raises(ValueError):
        normalize_frame(frame, method="invalid")


def test_convert_color_bgr_to_rgb():
    """Test BGR to RGB conversion"""
    # Create BGR frame (blue, green, red)
    bgr_frame = np.array([[[255, 0, 0]]], dtype=np.uint8)  # Blue in BGR

    rgb_frame = convert_color(bgr_frame, src_format="BGR", dst_format="RGB")

    # Should be red in RGB
    assert rgb_frame[0, 0, 0] == 0  # R
    assert rgb_frame[0, 0, 1] == 0  # G
    assert rgb_frame[0, 0, 2] == 255  # B


def test_convert_color_same_format():
    """Test conversion with same source and destination"""
    frame = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)

    converted = convert_color(frame, src_format="BGR", dst_format="BGR")

    np.testing.assert_array_equal(converted, frame)


def test_convert_color_to_grayscale():
    """Test color to grayscale conversion"""
    frame = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)

    gray = convert_color(frame, src_format="BGR", dst_format="GRAY")

    assert gray.ndim == 2  # Grayscale should be 2D
    assert gray.shape == (10, 10)


def test_convert_color_invalid():
    """Test invalid color conversion"""
    frame = np.zeros((10, 10, 3), dtype=np.uint8)

    with pytest.raises(ValueError):
        convert_color(frame, src_format="INVALID", dst_format="RGB")


def test_enhance_underwater():
    """Test underwater enhancement"""
    # Create simulated underwater frame (low contrast, bluish)
    frame = np.random.randint(80, 120, (100, 100, 3), dtype=np.uint8)

    enhanced = enhance_underwater(frame, gamma=1.2, contrast_factor=1.3)

    assert enhanced.shape == frame.shape
    assert enhanced.dtype == np.uint8
    # Enhanced frame should have different statistics
    assert not np.array_equal(enhanced, frame)


def test_extract_multi_frame_window():
    """Test multi-frame window extraction"""
    frames = [
        np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        for _ in range(10)
    ]

    window = extract_multi_frame_window(frames, window_size=5)

    assert window is not None
    assert window.shape == (100, 100, 15)  # 3 channels * 5 frames


def test_extract_multi_frame_window_insufficient_frames():
    """Test window extraction with insufficient frames"""
    frames = [
        np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        for _ in range(3)
    ]

    window = extract_multi_frame_window(frames, window_size=5)

    assert window is None


def test_resize_frame_edge_cases():
    """Test edge cases for resizing"""
    # Very small frame
    small_frame = np.ones((10, 10, 3), dtype=np.uint8)
    resized = resize_frame(small_frame, target_size=(224, 224))
    assert resized.shape == (224, 224, 3)

    # Very large frame
    large_frame = np.ones((2000, 2000, 3), dtype=np.uint8)
    resized = resize_frame(large_frame, target_size=(224, 224))
    assert resized.shape == (224, 224, 3)


def test_normalize_frame_zero_values():
    """Test normalization with all-zero frame"""
    frame = np.zeros((10, 10, 3), dtype=np.uint8)

    normalized = normalize_frame(frame, method="zero_center")

    assert normalized.dtype == np.float32
    assert normalized.max() == 0.0
    assert normalized.min() == 0.0
