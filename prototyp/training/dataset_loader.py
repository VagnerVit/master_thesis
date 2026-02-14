"""PyTorch Dataset for SwimXYZ keypoint sequences

Loads 2D/3D keypoint annotations from SwimXYZ dataset for training
style classifiers and stroke analyzers.

Usage:
    from training.dataset_loader import SwimXYZDataset, create_dataloaders

    # Single dataset
    train_ds = SwimXYZDataset(Path("data"), "train", "freestyle")
    sample = train_ds[0]  # {"keypoints": tensor, "style": str, "view": str}

    # DataLoaders for training
    train_loader, val_loader, test_loader = create_dataloaders(
        Path("data"), "freestyle", batch_size=32
    )
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Callable, Tuple, Any
from dataclasses import dataclass

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

from .swimxyz_parser import parse_swimxyz_csv, reshape_keypoints


@dataclass
class SampleInfo:
    """Metadata for a single training sample (sliding window)"""
    sequence_idx: int
    video_path: str
    style: str
    view: str
    start_frame: int
    end_frame: int
    num_keypoints: int


@dataclass
class CachedAnnotation:
    """Cached annotation data with metadata"""
    frames_data: np.ndarray
    dims: int


class SwimXYZDataset(Dataset):
    """PyTorch Dataset for SwimXYZ keypoint sequences

    Loads keypoint data using sliding windows over video sequences.
    Supports lazy loading with optional caching for memory efficiency.

    Attributes:
        data_dir: Root data directory
        split: Dataset split ("train", "val", "test")
        style: Swimming style ("freestyle", "backstroke", etc.)
        annotation_type: Type of annotation ("2D_cam", "3D_cam", etc.)
        sequence_length: Number of frames per sample
        stride: Sliding window stride
    """

    STYLE_TO_LABEL = {
        "freestyle": 0,
        "backstroke": 1,
        "breaststroke": 2,
        "butterfly": 3,
    }

    VIEW_TO_LABEL = {
        "Aerial": 0,
        "Front": 1,
        "Side_above_water": 2,
        "Side_underwater": 3,
        "Side_water_level": 4,
    }

    def __init__(
        self,
        data_dir: Path,
        split: str,
        style: str = "freestyle",
        annotation_type: str = "2D_cam",
        sequence_length: int = 32,
        stride: int = 16,
        transform: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        cache_annotations: bool = True,
        filter_keypoint_format: str = "base",
    ):
        """Initialize dataset

        Args:
            data_dir: Root data directory containing swimxyz/
            split: Dataset split - "train", "val", or "test"
            style: Swimming style
            annotation_type: Annotation type - "2D_cam", "3D_cam", "2D_pelvis", "3D_pelvis"
            sequence_length: Number of frames per sample
            stride: Sliding window stride (overlap = sequence_length - stride)
            transform: Optional transform function for keypoints
            cache_annotations: Whether to cache loaded CSV data in memory
            filter_keypoint_format: Filter sequences by keypoint format.
                Default "base" (48 kpts). Use "COCO" for COCO format (25 kpts, but has data issues).
                Use None to include all formats (may cause shape mismatches).
        """
        self.data_dir = Path(data_dir)
        self.split = split
        self.style = style
        self.annotation_type = annotation_type
        self.sequence_length = sequence_length
        self.stride = stride
        self.transform = transform

        self.annotations_dir = (
            self.data_dir / "swimxyz" / "annotations" / f"{style.capitalize()}_labels"
        )

        self.sequences = self._load_sequences(filter_keypoint_format)
        self.samples = self._create_sliding_windows()

        # Cache stores annotation data with detected dimensions
        self._cache: Optional[Dict[str, CachedAnnotation]] = {} if cache_annotations else None
        self._detected_dims: Optional[int] = None

    def _load_sequences(
        self,
        filter_keypoint_format: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Load sequence metadata from split JSON file"""
        split_file = (
            self.data_dir / "swimxyz" / "processed" / self.style / f"{self.split}_sequences.json"
        )

        if not split_file.exists():
            raise FileNotFoundError(
                f"Split file not found: {split_file}\n"
                f"Run: python scripts/prepare_dataset.py --dataset swimxyz --style {self.style}"
            )

        with open(split_file, 'r', encoding='utf-8') as f:
            sequences = json.load(f)

        # Filter by keypoint format if specified
        if filter_keypoint_format:
            sequences = [
                seq for seq in sequences
                if filter_keypoint_format.lower() in seq["video_path"].lower()
            ]

        # Filter sequences that have the requested annotation type
        ann_key = f"has_{self.annotation_type.lower()}"
        sequences = [seq for seq in sequences if seq.get(ann_key, False)]

        return sequences

    def _create_sliding_windows(self) -> List[SampleInfo]:
        """Create sliding window samples from all sequences"""
        samples: List[SampleInfo] = []

        for seq_idx, seq in enumerate(self.sequences):
            num_frames = seq["num_frames"]
            num_keypoints = len(seq["keypoint_names"])

            # Calculate number of windows
            if num_frames < self.sequence_length:
                continue

            num_windows = (num_frames - self.sequence_length) // self.stride + 1

            for window_idx in range(num_windows):
                start = window_idx * self.stride
                end = start + self.sequence_length

                samples.append(SampleInfo(
                    sequence_idx=seq_idx,
                    video_path=seq["video_path"],
                    style=seq["style"],
                    view=seq["view"],
                    start_frame=start,
                    end_frame=end,
                    num_keypoints=num_keypoints,
                ))

        return samples

    def _load_annotation(self, video_path: str, num_keypoints: int) -> Tuple[np.ndarray, int]:
        """Load and optionally cache annotation data

        Returns:
            (frames_data, dims_per_keypoint)
        """
        if self._cache is not None and video_path in self._cache:
            cached = self._cache[video_path]
            return cached.frames_data, cached.dims

        csv_path = self.annotations_dir / video_path / f"{self.annotation_type}.txt"
        _, frames_data, dims = parse_swimxyz_csv(csv_path)

        # Store detected dims for stats
        if self._detected_dims is None:
            self._detected_dims = dims

        if self._cache is not None:
            self._cache[video_path] = CachedAnnotation(frames_data, dims)

        return frames_data, dims

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        sample = self.samples[idx]

        # Load annotation data with auto-detected dimensions
        frames_data, dims = self._load_annotation(sample.video_path, sample.num_keypoints)

        # Extract window
        seq = frames_data[sample.start_frame:sample.end_frame]

        # Reshape to [seq_len, num_keypoints, dims]
        seq = reshape_keypoints(seq, sample.num_keypoints, dims)

        # Apply transform if provided
        if self.transform is not None:
            seq = self.transform(seq)

        # Convert to tensor
        keypoints = torch.from_numpy(seq.copy())

        return {
            "keypoints": keypoints,
            "style": sample.style,
            "style_label": self.STYLE_TO_LABEL.get(sample.style, -1),
            "view": sample.view,
            "view_label": self.VIEW_TO_LABEL.get(sample.view, -1),
            "video_path": sample.video_path,
            "start_frame": sample.start_frame,
        }

    def get_num_keypoints(self) -> int:
        """Get number of keypoints (varies by format: base=48, COCO=25)"""
        if not self.sequences:
            return 0
        return len(self.sequences[0]["keypoint_names"])

    def get_keypoint_names(self) -> List[str]:
        """Get keypoint names for first sequence"""
        if not self.sequences:
            return []
        return self.sequences[0]["keypoint_names"]

    def get_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        views: Dict[str, int] = {}
        total_frames = 0

        for seq in self.sequences:
            views[seq["view"]] = views.get(seq["view"], 0) + 1
            total_frames += seq["num_frames"]

        return {
            "split": self.split,
            "style": self.style,
            "annotation_type": self.annotation_type,
            "num_sequences": len(self.sequences),
            "num_samples": len(self.samples),
            "total_frames": total_frames,
            "sequence_length": self.sequence_length,
            "stride": self.stride,
            "views": views,
            "num_keypoints": self.get_num_keypoints(),
            "dims": self._detected_dims if self._detected_dims else 3,
        }


def create_multistyle_dataloaders(
    data_dir: Path,
    styles: List[str] = None,
    annotation_type: str = "2D_cam",
    sequence_length: int = 32,
    stride: int = 16,
    batch_size: int = 32,
    num_workers: int = 0,
    pin_memory: bool = True,
    **dataset_kwargs
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Create DataLoaders for multiple swimming styles

    Args:
        data_dir: Root data directory
        styles: List of styles (default: all 4 styles)
        annotation_type: Annotation type
        sequence_length: Frames per sample
        stride: Sliding window stride
        batch_size: Batch size
        num_workers: Number of data loading workers
        pin_memory: Pin memory for CUDA

    Returns:
        (train_loader, val_loader, test_loader)
    """
    from torch.utils.data import ConcatDataset

    if styles is None:
        styles = ["freestyle", "backstroke", "breaststroke", "butterfly"]

    train_datasets: List[SwimXYZDataset] = []
    val_datasets: List[SwimXYZDataset] = []
    test_datasets: List[SwimXYZDataset] = []

    for style in styles:
        common_args = {
            "data_dir": data_dir,
            "style": style,
            "annotation_type": annotation_type,
            "sequence_length": sequence_length,
            "stride": stride,
            **dataset_kwargs,
        }

        try:
            train_datasets.append(SwimXYZDataset(split="train", **common_args))
            val_datasets.append(SwimXYZDataset(split="val", **common_args))
            test_datasets.append(SwimXYZDataset(split="test", **common_args))
        except FileNotFoundError:
            print(f"Warning: Style '{style}' not found, skipping...")

    if not train_datasets:
        raise ValueError("No datasets found!")

    train_ds = ConcatDataset(train_datasets)
    val_ds = ConcatDataset(val_datasets)
    test_ds = ConcatDataset(test_datasets)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=True,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return train_loader, val_loader, test_loader


def create_dataloaders(
    data_dir: Path,
    style: str = "freestyle",
    annotation_type: str = "2D_cam",
    sequence_length: int = 32,
    stride: int = 16,
    batch_size: int = 32,
    num_workers: int = 0,
    pin_memory: bool = True,
    **dataset_kwargs
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Create train/val/test DataLoaders

    Args:
        data_dir: Root data directory
        style: Swimming style
        annotation_type: Annotation type
        sequence_length: Frames per sample
        stride: Sliding window stride
        batch_size: Batch size
        num_workers: Number of data loading workers
        pin_memory: Pin memory for CUDA
        **dataset_kwargs: Additional arguments for SwimXYZDataset

    Returns:
        (train_loader, val_loader, test_loader)
    """
    common_args = {
        "data_dir": data_dir,
        "style": style,
        "annotation_type": annotation_type,
        "sequence_length": sequence_length,
        "stride": stride,
        **dataset_kwargs,
    }

    train_ds = SwimXYZDataset(split="train", **common_args)
    val_ds = SwimXYZDataset(split="val", **common_args)
    test_ds = SwimXYZDataset(split="test", **common_args)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=True,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return train_loader, val_loader, test_loader
