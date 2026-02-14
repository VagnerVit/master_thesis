"""SwimAth training module

Contains dataset loaders, models, and training utilities for ML.
"""

from .dataset_loader import SwimXYZDataset, create_dataloaders
from .swimxyz_parser import parse_swimxyz_csv
from .angle_utils import (
    calculate_angle,
    get_all_joint_angles,
    get_joint_names,
    SwimXYZKeypoints,
)

__all__ = [
    "SwimXYZDataset",
    "create_dataloaders",
    "parse_swimxyz_csv",
    "calculate_angle",
    "get_all_joint_angles",
    "get_joint_names",
    "SwimXYZKeypoints",
]
