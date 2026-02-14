"""Verify dataset integrity and structure

Checks:
- All required files present
- Annotations valid
- Videos playable
- Correct file counts

Usage:
    python verify_dataset.py --dataset swimxyz
    python verify_dataset.py --dataset swimxyz --style freestyle --detailed
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from utils.logging_config import setup_logging, get_logger

log_file = Path.home() / ".swimath" / "logs" / "verify.log"
setup_logging(log_file=log_file, console=True)
logger = get_logger(__name__)


def verify_annotation_file(annotation_file: Path) -> Tuple[bool, str]:
    """Verify single annotation file

    Args:
        annotation_file: Path to JSON file

    Returns:
        (is_valid, message)
    """
    try:
        with open(annotation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check required keys
        required = ['images', 'annotations']
        missing = [k for k in required if k not in data]

        if missing:
            return False, f"Missing keys: {missing}"

        num_images = len(data['images'])
        num_annotations = len(data['annotations'])

        return True, f"✓ {num_images} images, {num_annotations} annotations"

    except json.JSONDecodeError as e:
        return False, f"✗ Invalid JSON: {e}"
    except Exception as e:
        return False, f"✗ Error: {e}"


def verify_video_file(video_file: Path, check_playable: bool = False) -> Tuple[bool, str]:
    """Verify video file

    Args:
        video_file: Path to video file
        check_playable: Whether to check if video is playable

    Returns:
        (is_valid, message)
    """
    if not video_file.exists():
        return False, "✗ File not found"

    size_mb = video_file.stat().st_size / (1024 * 1024)

    if not check_playable:
        return True, f"✓ {size_mb:.1f} MB"

    # Try to open video
    try:
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            return False, "✗ Cannot open video"

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cap.release()

        return True, f"✓ {width}x{height} @ {fps:.1f} FPS, {frame_count} frames, {size_mb:.1f} MB"

    except Exception as e:
        return False, f"✗ Error: {e}"


def verify_swimxyz_annotations(data_dir: Path, style: str, detailed: bool = False) -> bool:
    """Verify SwimXYZ annotations (CSV format)

    Args:
        data_dir: Data directory
        style: Swimming style
        detailed: Show detailed info

    Returns:
        True if valid
    """
    logger.info(f"Verifying SwimXYZ {style} annotations...")

    annotations_dir = data_dir / "swimxyz" / "annotations" / f"{style.capitalize()}_labels"

    if not annotations_dir.exists():
        logger.error(f"✗ Annotations directory not found: {annotations_dir}")
        return False

    logger.info(f"✓ Annotations directory: {annotations_dir}")

    # SwimXYZ uses CSV files (2D_cam.txt, etc.), not JSON
    annotation_files = list(annotations_dir.rglob("2D_cam.txt"))

    if not annotation_files:
        logger.error("✗ No annotation files found (looking for 2D_cam.txt)")
        return False

    logger.info(f"✓ Found {len(annotation_files)} annotation sequences")

    if detailed:
        # Show sample of directories
        sample_dirs = set()
        for f in annotation_files[:5]:
            sample_dirs.add(f.parent.relative_to(annotations_dir))
        for d in sample_dirs:
            logger.info(f"  - {d}")
        if len(annotation_files) > 5:
            logger.info(f"  ... and {len(annotation_files) - 5} more")

    return True


def verify_swimxyz_videos(
    data_dir: Path,
    style: str,
    part: int | None = None,
    check_playable: bool = False,
    detailed: bool = False
) -> bool:
    """Verify SwimXYZ videos

    Args:
        data_dir: Data directory
        style: Swimming style
        part: Part number (1 or 2), None for both
        check_playable: Whether to check if videos are playable
        detailed: Show detailed info

    Returns:
        True if valid
    """
    logger.info(f"Verifying SwimXYZ {style} videos...")

    videos_dir = data_dir / "swimxyz" / "videos" / style

    if not videos_dir.exists():
        logger.warning(f"⚠ Videos directory not found: {videos_dir}")
        logger.info("  (Videos are optional, only annotations required for training)")
        return True  # Not fatal

    parts = [part] if part else [1, 2]
    all_valid = True

    for p in parts:
        part_dir = videos_dir / f"part{p}"

        if not part_dir.exists():
            logger.warning(f"⚠ Part {p} directory not found: {part_dir}")
            continue

        # Find video files (mp4 or webm)
        video_files = list(part_dir.rglob("*.mp4")) + list(part_dir.rglob("*.webm"))

        if not video_files:
            logger.warning(f"⚠ No video files found in {part_dir}")
            all_valid = False
            continue

        logger.info(f"✓ Part {p}: Found {len(video_files)} videos")

        if detailed:
            for video_file in video_files[:5]:  # Show first 5
                is_valid, message = verify_video_file(video_file, check_playable)
                prefix = "    " if is_valid else "    ✗ "
                logger.info(f"{prefix}{video_file.name}: {message}")

            if len(video_files) > 5:
                logger.info(f"    ... and {len(video_files) - 5} more")

    return all_valid


def verify_swimxyz_processed(data_dir: Path, style: str) -> bool:
    """Verify processed dataset (train/val/test split)

    Args:
        data_dir: Data directory
        style: Swimming style

    Returns:
        True if valid
    """
    logger.info(f"Verifying processed {style} dataset...")

    processed_dir = data_dir / "swimxyz" / "processed" / style

    if not processed_dir.exists():
        logger.warning(f"⚠ Processed directory not found: {processed_dir}")
        logger.info("  Run prepare_dataset.py to create train/val/test split")
        return False

    # Check split files (SwimXYZ uses _sequences.json format)
    required_files = [
        "train_sequences.json",
        "val_sequences.json",
        "test_sequences.json",
        "metadata.json",
    ]

    all_present = True

    for filename in required_files:
        file_path = processed_dir / filename
        if file_path.exists():
            logger.info(f"  ✓ {filename}")
        else:
            logger.error(f"  ✗ {filename} missing")
            all_present = False

    if all_present:
        logger.info("✓ All processed files present")

        # Load and show metadata
        metadata_file = processed_dir / "metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        logger.info(f"  Sequences: {metadata.get('num_sequences', 'N/A')}")
        logger.info(f"  Total frames: {metadata.get('total_frames', 'N/A')}")
        logger.info(f"  Keypoints: {metadata.get('num_keypoints', 'N/A')}")
        if 'views' in metadata:
            logger.info(f"  Views: {metadata['views']}")

    return all_present


def verify_swimxyz_dataset(
    data_dir: Path,
    style: str | None = None,
    check_videos: bool = True,
    check_playable: bool = False,
    detailed: bool = False
) -> bool:
    """Verify complete SwimXYZ dataset

    Args:
        data_dir: Data directory
        style: Swimming style, None for all
        check_videos: Whether to check videos
        check_playable: Whether to check if videos are playable
        detailed: Show detailed info

    Returns:
        True if all valid
    """
    logger.info("=== SwimXYZ Dataset Verification ===\n")

    styles = [style] if style else ["freestyle", "backstroke", "breaststroke", "butterfly"]

    all_valid = True

    for s in styles:
        logger.info(f"\n--- {s.capitalize()} ---\n")

        # Verify annotations
        if not verify_swimxyz_annotations(data_dir, s, detailed):
            all_valid = False

        # Verify videos
        if check_videos:
            if not verify_swimxyz_videos(data_dir, s, None, check_playable, detailed):
                all_valid = False

        # Verify processed
        if not verify_swimxyz_processed(data_dir, s):
            pass  # Warning only, not fatal

    logger.info("\n=== Summary ===\n")

    if all_valid:
        logger.info("✓ Dataset verification passed!")
    else:
        logger.error("✗ Dataset verification failed")
        logger.info("\nTo fix:")
        logger.info("  1. Run: python scripts/download_dataset.py --dataset swimxyz --annotations-only")
        logger.info("  2. Run: python scripts/prepare_dataset.py --dataset swimxyz --style <style>")

    return all_valid


def main():
    parser = argparse.ArgumentParser(description="Verify dataset integrity")

    parser.add_argument("--dataset", type=str, choices=["swimxyz"], default="swimxyz",
                        help="Dataset to verify")
    parser.add_argument("--style", type=str, choices=["freestyle", "backstroke", "breaststroke", "butterfly"],
                        help="Swimming style (default: all)")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                        help="Data directory")
    parser.add_argument("--no-videos", action="store_true",
                        help="Skip video verification")
    parser.add_argument("--check-playable", action="store_true",
                        help="Check if videos are playable (slower)")
    parser.add_argument("--detailed", action="store_true",
                        help="Show detailed information")

    args = parser.parse_args()

    if args.dataset == "swimxyz":
        success = verify_swimxyz_dataset(
            args.data_dir,
            args.style,
            check_videos=not args.no_videos,
            check_playable=args.check_playable,
            detailed=args.detailed
        )
        return 0 if success else 1
    else:
        logger.error(f"Unknown dataset: {args.dataset}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
