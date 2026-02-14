"""Prepare downloaded datasets for training

- Validate annotations
- Create train/val/test split
- Generate dataset metadata
- Create reference templates

Supports:
- SwimXYZ: Custom CSV format (semicolon-separated, one file per video)
- COCO: Standard JSON format (for other datasets)

Usage:
    python prepare_dataset.py --dataset swimxyz --style freestyle
    python prepare_dataset.py --dataset swimxyz --all-styles --split 0.7/0.15/0.15
"""

import argparse
import sys
import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import random
from collections import defaultdict
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from utils.logging_config import setup_logging, get_logger

log_file = Path.home() / ".swimath" / "logs" / "prepare.log"
setup_logging(log_file=log_file, console=True)
logger = get_logger(__name__)


# SwimXYZ specific constants
SWIMXYZ_ANNOTATION_FILES = ["2D_cam.txt", "2D_pelvis.txt", "3D_cam.txt", "3D_pelvis.txt"]


@dataclass
class SwimXYZSequence:
    """Represents a single video sequence with annotations"""
    video_path: str
    style: str
    view: str  # Aerial, Front, Side_above_water, etc.
    num_frames: int
    keypoint_names: List[str]
    annotations_2d_cam: Optional[List[List[float]]] = None
    annotations_2d_pelvis: Optional[List[List[float]]] = None
    annotations_3d_cam: Optional[List[List[float]]] = None
    annotations_3d_pelvis: Optional[List[List[float]]] = None


def load_coco_annotations(annotation_file: Path) -> Dict:
    """Load COCO format annotations

    Args:
        annotation_file: Path to JSON annotation file

    Returns:
        Annotation dictionary
    """
    logger.info(f"Loading annotations: {annotation_file}")

    try:
        with open(annotation_file, 'r', encoding='utf-8') as f:
            annotations = json.load(f)

        logger.info(
            f"Loaded {len(annotations.get('images', []))} images, "
            f"{len(annotations.get('annotations', []))} annotations"
        )
        return annotations

    except Exception as e:
        logger.error(f"Failed to load annotations: {e}")
        return {}


def validate_annotations(annotations: Dict) -> Tuple[bool, List[str]]:
    """Validate COCO annotations structure

    Args:
        annotations: COCO annotation dictionary

    Returns:
        (is_valid, list_of_issues)
    """
    issues = []

    # Check required keys
    required_keys = ['images', 'annotations', 'categories']
    for key in required_keys:
        if key not in annotations:
            issues.append(f"Missing required key: {key}")

    if issues:
        return False, issues

    # Check image IDs
    image_ids = {img['id'] for img in annotations['images']}
    annotation_image_ids = {ann['image_id'] for ann in annotations['annotations']}

    orphaned_annotations = annotation_image_ids - image_ids
    if orphaned_annotations:
        issues.append(f"Found {len(orphaned_annotations)} annotations without corresponding images")

    # Check keypoint format
    for ann in annotations['annotations'][:10]:  # Check first 10
        if 'keypoints' in ann:
            kps = ann['keypoints']
            if len(kps) % 3 != 0:
                issues.append(f"Invalid keypoints format in annotation {ann['id']}")
                break

    is_valid = len(issues) == 0
    return is_valid, issues


def create_train_val_test_split(
    annotations: Dict,
    split_ratios: Tuple[float, float, float] = (0.7, 0.15, 0.15),
    random_seed: int = 42
) -> Tuple[Dict, Dict, Dict]:
    """Create train/val/test split

    Args:
        annotations: COCO annotations
        split_ratios: (train, val, test) ratios
        random_seed: Random seed for reproducibility

    Returns:
        (train_annotations, val_annotations, test_annotations)
    """
    random.seed(random_seed)

    train_ratio, val_ratio, test_ratio = split_ratios
    assert abs(sum(split_ratios) - 1.0) < 1e-6, "Split ratios must sum to 1.0"

    # Get all image IDs
    images = annotations['images']
    image_ids = [img['id'] for img in images]

    # Shuffle
    random.shuffle(image_ids)

    # Calculate split indices
    n_total = len(image_ids)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)

    # Split image IDs
    train_ids = set(image_ids[:n_train])
    val_ids = set(image_ids[n_train:n_train + n_val])
    test_ids = set(image_ids[n_train + n_val:])

    logger.info(f"Split: train={len(train_ids)}, val={len(val_ids)}, test={len(test_ids)}")

    # Create split annotations
    def create_split_annotations(split_ids: set) -> Dict:
        split_images = [img for img in images if img['id'] in split_ids]
        split_anns = [ann for ann in annotations['annotations'] if ann['image_id'] in split_ids]

        return {
            'images': split_images,
            'annotations': split_anns,
            'categories': annotations['categories'],
            'info': annotations.get('info', {}),
        }

    train_annotations = create_split_annotations(train_ids)
    val_annotations = create_split_annotations(val_ids)
    test_annotations = create_split_annotations(test_ids)

    return train_annotations, val_annotations, test_annotations


def save_split_annotations(
    train_anns: Dict,
    val_anns: Dict,
    test_anns: Dict,
    output_dir: Path
):
    """Save split annotations to files

    Args:
        train_anns: Training annotations
        val_anns: Validation annotations
        test_anns: Test annotations
        output_dir: Output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    splits = {
        'train': train_anns,
        'val': val_anns,
        'test': test_anns,
    }

    for split_name, anns in splits.items():
        output_file = output_dir / f"{split_name}_annotations.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(anns, f, indent=2)
        logger.info(f"Saved {split_name} annotations: {output_file}")


def generate_dataset_metadata(
    annotations: Dict,
    style: str,
    output_file: Path
):
    """Generate dataset metadata

    Args:
        annotations: COCO annotations
        style: Swimming style
        output_file: Output metadata file
    """
    metadata = {
        'style': style,
        'num_images': len(annotations['images']),
        'num_annotations': len(annotations['annotations']),
        'categories': annotations.get('categories', []),
        'keypoint_names': [],
        'num_keypoints': 0,
    }

    # Extract keypoint info from first annotation
    if annotations['annotations']:
        first_ann = annotations['annotations'][0]
        if 'keypoints' in first_ann:
            num_keypoints = len(first_ann['keypoints']) // 3
            metadata['num_keypoints'] = num_keypoints

            # Try to get keypoint names from categories
            for cat in annotations.get('categories', []):
                if 'keypoints' in cat:
                    metadata['keypoint_names'] = cat['keypoints']
                    break

    # Calculate statistics
    keypoint_counts = defaultdict(int)
    for ann in annotations['annotations']:
        if 'keypoints' in ann:
            kps = ann['keypoints']
            for i in range(0, len(kps), 3):
                visibility = kps[i + 2]
                if visibility > 0:
                    keypoint_counts[i // 3] += 1

    metadata['keypoint_visibility_stats'] = dict(keypoint_counts)

    # Save metadata
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved metadata: {output_file}")


def parse_swimxyz_csv(file_path: Path) -> Tuple[List[str], List[List[float]]]:
    """Parse SwimXYZ CSV annotation file

    Args:
        file_path: Path to annotation txt file (semicolon-separated)

    Returns:
        (keypoint_names, frames_data) where frames_data is list of lists of floats
    """
    keypoint_names: List[str] = []
    frames_data: List[List[float]] = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return keypoint_names, frames_data

    # Parse header - extract unique keypoint names (remove .x, .y, .z suffixes)
    header = lines[0].strip().rstrip(';').split(';')
    seen_names: set = set()
    for col in header:
        # Remove .x, .y, .z suffix to get base name
        base_name = col.rsplit('.', 1)[0] if '.' in col else col
        if base_name not in seen_names:
            keypoint_names.append(base_name)
            seen_names.add(base_name)

    # Parse data rows
    for line in lines[1:]:
        line = line.strip().rstrip(';')
        if not line:
            continue

        values = []
        for val in line.split(';'):
            try:
                # Handle comma as decimal separator (European format)
                values.append(float(val.replace(',', '.')))
            except ValueError:
                values.append(0.0)

        frames_data.append(values)

    return keypoint_names, frames_data


def find_swimxyz_sequences(annotations_dir: Path, style: str) -> List[SwimXYZSequence]:
    """Find all video sequences with annotations in SwimXYZ dataset

    Args:
        annotations_dir: Root annotations directory for the style
        style: Swimming style name

    Returns:
        List of SwimXYZSequence objects
    """
    sequences: List[SwimXYZSequence] = []

    # SwimXYZ structure: Style/View/Swimmer/Water/Lighting/Speed/Position/base/
    # Find all directories containing annotation files
    for ann_file in annotations_dir.rglob("2D_cam.txt"):
        seq_dir = ann_file.parent

        # Extract view from path (e.g., Aerial, Front, Side_above_water)
        rel_path = seq_dir.relative_to(annotations_dir)
        path_parts = rel_path.parts

        # First part after style is the view
        view = path_parts[1] if len(path_parts) > 1 else "unknown"

        # Construct video path (relative)
        video_rel_path = str(rel_path).replace("\\", "/")

        # Parse 2D_cam.txt to get keypoints and frame count
        keypoint_names, frames_2d_cam = parse_swimxyz_csv(ann_file)

        if not frames_2d_cam:
            continue

        sequence = SwimXYZSequence(
            video_path=video_rel_path,
            style=style,
            view=view,
            num_frames=len(frames_2d_cam),
            keypoint_names=keypoint_names,
            annotations_2d_cam=frames_2d_cam,
        )

        # Load other annotation files if present
        for ann_type, attr_name in [
            ("2D_pelvis.txt", "annotations_2d_pelvis"),
            ("3D_cam.txt", "annotations_3d_cam"),
            ("3D_pelvis.txt", "annotations_3d_pelvis"),
        ]:
            ann_path = seq_dir / ann_type
            if ann_path.exists():
                _, frames = parse_swimxyz_csv(ann_path)
                setattr(sequence, attr_name, frames)

        sequences.append(sequence)

    return sequences


def create_swimxyz_split(
    sequences: List[SwimXYZSequence],
    split_ratios: Tuple[float, float, float],
    random_seed: int = 42
) -> Tuple[List[SwimXYZSequence], List[SwimXYZSequence], List[SwimXYZSequence]]:
    """Split sequences into train/val/test sets

    Args:
        sequences: List of sequences
        split_ratios: (train, val, test) ratios
        random_seed: Random seed for reproducibility

    Returns:
        (train, val, test) sequence lists
    """
    random.seed(random_seed)

    # Shuffle sequences
    shuffled = sequences.copy()
    random.shuffle(shuffled)

    train_ratio, val_ratio, _ = split_ratios
    n_total = len(shuffled)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)

    train = shuffled[:n_train]
    val = shuffled[n_train:n_train + n_val]
    test = shuffled[n_train + n_val:]

    return train, val, test


def save_swimxyz_split(
    train: List[SwimXYZSequence],
    val: List[SwimXYZSequence],
    test: List[SwimXYZSequence],
    output_dir: Path
):
    """Save SwimXYZ split to JSON files

    Args:
        train, val, test: Sequence lists
        output_dir: Output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, sequences in [("train", train), ("val", val), ("test", test)]:
        output_file = output_dir / f"{split_name}_sequences.json"

        # Convert to serializable format (without full annotation data to save space)
        data = []
        for seq in sequences:
            data.append({
                "video_path": seq.video_path,
                "style": seq.style,
                "view": seq.view,
                "num_frames": seq.num_frames,
                "keypoint_names": seq.keypoint_names,
                "has_2d_cam": seq.annotations_2d_cam is not None,
                "has_2d_pelvis": seq.annotations_2d_pelvis is not None,
                "has_3d_cam": seq.annotations_3d_cam is not None,
                "has_3d_pelvis": seq.annotations_3d_pelvis is not None,
            })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {split_name}: {len(sequences)} sequences -> {output_file}")


def generate_swimxyz_metadata(
    sequences: List[SwimXYZSequence],
    style: str,
    output_file: Path
):
    """Generate metadata for SwimXYZ dataset

    Args:
        sequences: All sequences
        style: Swimming style
        output_file: Output file path
    """
    # Collect statistics
    views: Dict[str, int] = defaultdict(int)
    total_frames = 0
    keypoint_names: List[str] = []

    for seq in sequences:
        views[seq.view] += 1
        total_frames += seq.num_frames
        if not keypoint_names and seq.keypoint_names:
            keypoint_names = seq.keypoint_names

    metadata = {
        "dataset": "SwimXYZ",
        "style": style,
        "format": "csv_semicolon",
        "num_sequences": len(sequences),
        "total_frames": total_frames,
        "views": dict(views),
        "num_keypoints": len(keypoint_names),
        "keypoint_names": keypoint_names,
        "annotation_types": ["2D_cam", "2D_pelvis", "3D_cam", "3D_pelvis"],
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved metadata: {output_file}")


def prepare_swimxyz_dataset(
    data_dir: Path,
    style: str,
    split_ratios: Tuple[float, float, float]
) -> bool:
    """Prepare SwimXYZ dataset for training

    SwimXYZ uses custom CSV format (semicolon-separated) with:
    - 2D_cam.txt: 2D keypoints in camera coordinates
    - 2D_pelvis.txt: 2D keypoints relative to pelvis
    - 3D_cam.txt: 3D keypoints in camera coordinates
    - 3D_pelvis.txt: 3D keypoints relative to pelvis

    Args:
        data_dir: Data directory
        style: Swimming style
        split_ratios: Train/val/test split ratios

    Returns:
        True if successful
    """
    logger.info(f"Preparing SwimXYZ {style} dataset...")

    # Paths
    annotations_dir = data_dir / "swimxyz" / "annotations" / f"{style.capitalize()}_labels"
    processed_dir = data_dir / "swimxyz" / "processed" / style

    if not annotations_dir.exists():
        logger.error(f"Annotations directory not found: {annotations_dir}")
        logger.info("Run download_dataset.py first to download annotations")
        return False

    # Find all sequences with annotations
    logger.info("Scanning for annotation files...")
    sequences = find_swimxyz_sequences(annotations_dir, style)

    if not sequences:
        logger.error(f"No annotation files found in {annotations_dir}")
        return False

    logger.info(f"Found {len(sequences)} video sequences")

    # Calculate total frames
    total_frames = sum(seq.num_frames for seq in sequences)
    logger.info(f"Total frames: {total_frames}")

    # Create train/val/test split
    train, val, test = create_swimxyz_split(sequences, split_ratios)
    logger.info(f"Split: train={len(train)}, val={len(val)}, test={len(test)}")

    # Save splits
    save_swimxyz_split(train, val, test, processed_dir)

    # Generate metadata
    generate_swimxyz_metadata(sequences, style, processed_dir / "metadata.json")

    logger.info(f"Dataset prepared: {processed_dir}")
    return True


def prepare_coco_dataset(
    data_dir: Path,
    dataset_name: str,
    split_ratios: Tuple[float, float, float]
) -> bool:
    """Prepare COCO-format dataset for training (generic)

    Args:
        data_dir: Data directory
        dataset_name: Name of the dataset
        split_ratios: Train/val/test split ratios

    Returns:
        True if successful
    """
    logger.info(f"Preparing {dataset_name} dataset (COCO format)...")

    annotations_dir = data_dir / dataset_name / "annotations"
    processed_dir = data_dir / dataset_name / "processed"

    if not annotations_dir.exists():
        logger.error(f"Annotations directory not found: {annotations_dir}")
        return False

    # Find annotation files
    annotation_files = list(annotations_dir.glob("*.json"))

    if not annotation_files:
        logger.error(f"No JSON annotation files found in {annotations_dir}")
        return False

    logger.info(f"Found {len(annotation_files)} annotation files")

    # Load and merge
    merged_images: List[Dict] = []
    merged_annotations: List[Dict] = []
    categories = None

    for ann_file in annotation_files:
        anns = load_coco_annotations(ann_file)
        if not anns:
            continue

        is_valid, issues = validate_annotations(anns)
        if not is_valid:
            logger.warning(f"Validation issues in {ann_file.name}: {issues}")

        merged_images.extend(anns.get('images', []))
        merged_annotations.extend(anns.get('annotations', []))

        if categories is None and 'categories' in anns:
            categories = anns['categories']

    merged = {
        'images': merged_images,
        'annotations': merged_annotations,
        'categories': categories or [],
        'info': {'description': f'{dataset_name} dataset', 'version': '1.0'}
    }

    logger.info(f"Total: {len(merged_images)} images, {len(merged_annotations)} annotations")

    # Split and save
    train_anns, val_anns, test_anns = create_train_val_test_split(merged, split_ratios)
    save_split_annotations(train_anns, val_anns, test_anns, processed_dir)
    generate_dataset_metadata(merged, dataset_name, processed_dir / "metadata.json")

    logger.info(f"Dataset prepared: {processed_dir}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Prepare datasets for training")

    parser.add_argument("--dataset", type=str, choices=["swimxyz"], default="swimxyz",
                        help="Dataset to prepare")
    parser.add_argument("--style", type=str, choices=["freestyle", "backstroke", "breaststroke", "butterfly"],
                        help="Swimming style")
    parser.add_argument("--all-styles", action="store_true",
                        help="Prepare all styles")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                        help="Data directory")
    parser.add_argument("--split", type=str, default="0.7/0.15/0.15",
                        help="Train/val/test split ratios (e.g., 0.7/0.15/0.15)")

    args = parser.parse_args()

    # Parse split ratios
    split_parts = args.split.split('/')
    if len(split_parts) != 3:
        logger.error("Invalid split format. Use: train/val/test (e.g., 0.7/0.15/0.15)")
        return 1

    split_ratios = tuple(float(x) for x in split_parts)

    if args.all_styles:
        styles = ["freestyle", "backstroke", "breaststroke", "butterfly"]
    elif args.style:
        styles = [args.style]
    else:
        logger.error("Specify --style or --all-styles")
        return 1

    # Prepare datasets
    all_success = True
    for style in styles:
        if not prepare_swimxyz_dataset(args.data_dir, style, split_ratios):
            all_success = False

    if all_success:
        logger.info("All datasets prepared successfully!")
        return 0
    else:
        logger.error("Some datasets failed to prepare")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# DATA SOURCES DOCUMENTATION
# =============================================================================
#
# SwimXYZ Dataset
# ---------------
# Paper: "SwimXYZ: A Large-Scale Dataset for Swimming Motion Capture"
# URL: https://arxiv.org/abs/2310.04360
# Website: https://g-fiche.github.io/research-pages/swimxyz/
# Zenodo: https://zenodo.org/record/8399376
#
# Format: Custom CSV (semicolon-separated)
# Files per sequence:
#   - 2D_cam.txt: 2D keypoints in camera pixel coordinates
#   - 2D_pelvis.txt: 2D keypoints normalized to pelvis origin
#   - 3D_cam.txt: 3D keypoints in camera coordinate system
#   - 3D_pelvis.txt: 3D keypoints normalized to pelvis origin
#
# Header format: "Keypoint.x;Keypoint.y;Keypoint.z;..."
# Data format: "value;value;value;..." (European decimal: comma -> dot)
#
# Keypoints (48 total):
#   Pelvis, Head, HeadNub, L/R Calf, L/R Clavicle, L/R Finger0-4,
#   L/R Foot, L/R Forearm, L/R Hand, L/R Thigh, L/R Heel, L/R Toe0-4,
#   L/R UpperArm, Neck, Spine, Spine1, Spine2, Ear_L/R, Eye_L/R, Nose
#
# Directory structure:
#   {Style}_labels/{Style}/{View}/{Swimmer}/{Water}/{Lighting}/{Speed}/{Position}/base/
#
# Views: Aerial, Front, Side_above_water, Side_underwater, Side_water_level
#
# Size: ~6.7 GB annotations, ~293 GB videos (75 GB per style)
# License: Academic use
#
# =============================================================================
# COCO Format Reference (for other datasets)
# =============================================================================
#
# Standard COCO keypoint format:
# URL: https://cocodataset.org/#format-data
#
# JSON structure:
# {
#   "images": [{"id": int, "file_name": str, "width": int, "height": int}],
#   "annotations": [{"id": int, "image_id": int, "keypoints": [x,y,v,...]}],
#   "categories": [{"id": int, "keypoints": [...], "skeleton": [...]}]
# }
#
# Keypoint visibility: 0=not labeled, 1=labeled but not visible, 2=visible
#
# =============================================================================
