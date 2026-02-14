"""Reference template generator for swimming style analysis

Generates reference angle templates from SwimXYZ dataset by:
1. Loading all sequences for a swimming style
2. Computing joint angles for each frame
3. Aggregating statistics (mean, std, min, max)
4. Saving to JSON template file

Usage:
    python -m training.template_generator --style freestyle
    # Creates models/freestyle_template.json
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
from tqdm import tqdm

from .dataset_loader import SwimXYZDataset
from .angle_utils import (
    get_all_joint_angles,
    get_joint_names,
    compute_angle_statistics,
    JOINT_DEFINITIONS,
    KP,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_template(
    data_dir: Path,
    style: str,
    output_path: Path,
    max_sequences: int = 0,
    annotation_type: str = "2D_cam",
) -> Dict[str, Any]:
    """Generate reference template for a swimming style

    Args:
        data_dir: Root data directory
        style: Swimming style ("freestyle", "backstroke", etc.)
        output_path: Path to save JSON template
        max_sequences: Max sequences to process (0 = all)
        annotation_type: Annotation type to use

    Returns:
        Template dictionary
    """
    logger.info(f"Generating template for {style}...")

    # Load dataset (use full sequence, stride=sequence_length for no overlap)
    dataset = SwimXYZDataset(
        data_dir=data_dir,
        split="train",
        style=style,
        annotation_type=annotation_type,
        sequence_length=32,
        stride=32,
        cache_annotations=True,
    )

    if len(dataset) == 0:
        raise ValueError(f"No data found for style '{style}'")

    logger.info(f"Loaded {len(dataset)} samples from {len(dataset.sequences)} sequences")

    # Collect all angles
    joint_names = get_joint_names()
    all_angles: Dict[str, List[float]] = {name: [] for name in joint_names}
    view_angles: Dict[str, Dict[str, List[float]]] = {}

    num_samples = min(len(dataset), max_sequences) if max_sequences > 0 else len(dataset)

    for idx in tqdm(range(num_samples), desc="Computing angles"):
        sample = dataset[idx]
        keypoints = sample["keypoints"].numpy()  # [seq_len, num_keypoints, dims]
        view = sample["view"]

        if view not in view_angles:
            view_angles[view] = {name: [] for name in joint_names}

        for frame_idx in range(keypoints.shape[0]):
            frame_kpts = keypoints[frame_idx]  # [num_keypoints, dims]
            angles = get_all_joint_angles(frame_kpts)

            for joint_name, angle in angles.items():
                if angle > 0:  # Filter invalid angles
                    all_angles[joint_name].append(angle)
                    view_angles[view][joint_name].append(angle)

    # Compute statistics
    logger.info("Computing statistics...")

    joint_stats: Dict[str, Dict[str, float]] = {}
    for joint_name in joint_names:
        angles_array = np.array(all_angles[joint_name])
        if len(angles_array) > 0:
            stats = compute_angle_statistics(angles_array)
            joint_stats[joint_name] = stats.to_dict()

    # Per-view statistics
    view_stats: Dict[str, Dict[str, Dict[str, float]]] = {}
    for view, angles_dict in view_angles.items():
        view_stats[view] = {}
        for joint_name, angles_list in angles_dict.items():
            angles_array = np.array(angles_list)
            if len(angles_array) > 0:
                stats = compute_angle_statistics(angles_array)
                view_stats[view][joint_name] = stats.to_dict()

    # Build template
    template: Dict[str, Any] = {
        "style": style,
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "annotation_type": annotation_type,
        "num_samples": num_samples,
        "num_sequences": len(dataset.sequences),
        "total_frames_analyzed": sum(len(v) for v in all_angles.values()) // len(joint_names),
        "keypoint_format": "base",
        "num_keypoints": 48,
        "joint_definitions": {
            name: {"indices": list(indices)}
            for name, indices in JOINT_DEFINITIONS.items()
        },
        "joint_statistics": joint_stats,
        "view_statistics": view_stats,
        "thresholds": {
            "minor_deviation": 10.0,
            "moderate_deviation": 20.0,
            "severe_deviation": 30.0,
        },
    }

    # Save template
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)

    logger.info(f"Template saved to {output_path}")

    return template


def validate_template(template_path: Path) -> bool:
    """Validate a template file"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)

    required_keys = ["style", "joint_statistics", "joint_definitions"]
    for key in required_keys:
        if key not in template:
            logger.error(f"Missing required key: {key}")
            return False

    logger.info(f"Template valid: {template['style']}")
    logger.info(f"  Joints: {len(template['joint_statistics'])}")
    logger.info(f"  Views: {len(template.get('view_statistics', {}))}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate swimming style reference template")
    parser.add_argument("--style", type=str, default="freestyle",
                       help="Swimming style (freestyle, backstroke, breaststroke, butterfly)")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                       help="Data directory")
    parser.add_argument("--output", type=Path, default=None,
                       help="Output path (default: models/{style}_template.json)")
    parser.add_argument("--max-sequences", type=int, default=0,
                       help="Max sequences to process (0 = all)")
    parser.add_argument("--annotation-type", type=str, default="2D_cam",
                       help="Annotation type")
    parser.add_argument("--validate", type=Path, default=None,
                       help="Validate existing template")

    args = parser.parse_args()

    if args.validate:
        validate_template(args.validate)
        return

    output_path = args.output or Path("models") / f"{args.style}_template.json"

    generate_template(
        data_dir=args.data_dir,
        style=args.style,
        output_path=output_path,
        max_sequences=args.max_sequences,
        annotation_type=args.annotation_type,
    )


if __name__ == "__main__":
    main()
