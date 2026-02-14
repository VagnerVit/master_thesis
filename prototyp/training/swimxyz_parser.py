"""SwimXYZ CSV annotation parser

Parses SwimXYZ dataset annotation files:
- 2D_cam.txt: 2D keypoints in camera pixel coordinates (but stored as x,y,z)
- 2D_pelvis.txt: 2D keypoints normalized to pelvis origin
- 3D_cam.txt: 3D keypoints in camera coordinate system
- 3D_pelvis.txt: 3D keypoints normalized to pelvis origin

NOTE: Despite the "2D" naming, all SwimXYZ files contain x,y,z coordinates.
The "2D" files contain projected 2D coordinates with z representing depth/distance.

Format:
- Semicolon-separated CSV
- European decimal format (comma -> dot)
- Header: Keypoint.x;Keypoint.y;Keypoint.z;... (always 3 values per keypoint)
- One row per frame
"""

from pathlib import Path
from typing import List, Tuple
import numpy as np


def parse_swimxyz_csv(file_path: Path) -> Tuple[List[str], np.ndarray, int]:
    """Parse SwimXYZ CSV annotation file

    Args:
        file_path: Path to annotation txt file (semicolon-separated)

    Returns:
        (keypoint_names, frames_data, dims_per_keypoint) where:
        - keypoint_names: List of unique keypoint names
        - frames_data: numpy array of shape [num_frames, num_values]
        - dims_per_keypoint: Number of dimensions per keypoint (2 or 3)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file is empty or malformed
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Annotation file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"Empty annotation file: {file_path}")

    # Parse header - extract unique keypoint names and detect dimensions
    header = lines[0].strip().rstrip(';').split(';')
    keypoint_names: List[str] = []
    seen_names: set = set()
    suffixes: set = set()

    for col in header:
        if '.' in col:
            base_name, suffix = col.rsplit('.', 1)
            suffixes.add(suffix)
        else:
            base_name = col
        if base_name not in seen_names:
            keypoint_names.append(base_name)
            seen_names.add(base_name)

    # Detect dimensions from suffixes
    dims_per_keypoint = len(suffixes) if suffixes else 3

    # Parse data rows
    frames_data: List[List[float]] = []

    for line in lines[1:]:
        line = line.strip().rstrip(';')
        if not line:
            continue

        values: List[float] = []
        for val in line.split(';'):
            try:
                # Handle comma as decimal separator (European format)
                values.append(float(val.replace(',', '.')))
            except ValueError:
                values.append(0.0)

        frames_data.append(values)

    if not frames_data:
        raise ValueError(f"No data rows in annotation file: {file_path}")

    return keypoint_names, np.array(frames_data, dtype=np.float32), dims_per_keypoint


def get_annotation_dimensions(annotation_type: str) -> int:
    """Get number of dimensions per keypoint for annotation type

    Args:
        annotation_type: One of "2D_cam", "2D_pelvis", "3D_cam", "3D_pelvis"

    Returns:
        Number of dimensions (2 or 3)
    """
    if annotation_type.startswith("2D"):
        return 2
    elif annotation_type.startswith("3D"):
        return 3
    else:
        raise ValueError(f"Unknown annotation type: {annotation_type}")


def reshape_keypoints(
    flat_data: np.ndarray,
    num_keypoints: int,
    dims: int
) -> np.ndarray:
    """Reshape flat keypoint data to structured format

    Args:
        flat_data: Array of shape [num_frames, num_values]
        num_keypoints: Number of keypoints
        dims: Dimensions per keypoint (2 or 3)

    Returns:
        Array of shape [num_frames, num_keypoints, dims]
    """
    num_frames = flat_data.shape[0]
    expected_values = num_keypoints * dims

    if flat_data.shape[1] != expected_values:
        raise ValueError(
            f"Shape mismatch: got {flat_data.shape[1]} values, "
            f"expected {expected_values} ({num_keypoints} keypoints × {dims} dims)"
        )

    return flat_data.reshape(num_frames, num_keypoints, dims)
