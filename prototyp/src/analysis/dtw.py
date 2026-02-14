"""Dynamic Time Warping (DTW) implementation for sequence comparison

DTW aligns two temporal sequences of potentially different lengths,
finding the optimal alignment that minimizes the total distance.

Used for comparing swimmer's stroke cycles against reference templates.
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional

import numpy as np
from scipy.spatial.distance import cdist


@dataclass
class DTWResult:
    """Result of DTW alignment"""
    distance: float
    normalized_distance: float
    path: List[Tuple[int, int]]
    cost_matrix: np.ndarray


def dtw_distance(
    seq1: np.ndarray,
    seq2: np.ndarray,
    metric: str = "euclidean",
    window: Optional[int] = None,
) -> DTWResult:
    """Compute DTW distance between two sequences

    Args:
        seq1: First sequence [n, features]
        seq2: Second sequence [m, features]
        metric: Distance metric ('euclidean', 'cosine', 'manhattan')
        window: Sakoe-Chiba band width (None = no constraint)

    Returns:
        DTWResult with distance, path, and cost matrix
    """
    n, m = len(seq1), len(seq2)

    # Compute pairwise distances
    dist_matrix = cdist(seq1, seq2, metric=metric)

    # Initialize cost matrix
    cost = np.full((n + 1, m + 1), np.inf)
    cost[0, 0] = 0

    # Fill cost matrix with optional window constraint
    for i in range(1, n + 1):
        j_start = 1 if window is None else max(1, i - window)
        j_end = m + 1 if window is None else min(m + 1, i + window + 1)

        for j in range(j_start, j_end):
            cost[i, j] = dist_matrix[i - 1, j - 1] + min(
                cost[i - 1, j],      # insertion
                cost[i, j - 1],      # deletion
                cost[i - 1, j - 1],  # match
            )

    # Backtrack to find optimal path
    path = []
    i, j = n, m
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        argmin = np.argmin([
            cost[i - 1, j - 1],
            cost[i - 1, j],
            cost[i, j - 1],
        ])
        if argmin == 0:
            i, j = i - 1, j - 1
        elif argmin == 1:
            i = i - 1
        else:
            j = j - 1

    path.reverse()

    total_distance = cost[n, m]
    normalized_distance = total_distance / len(path) if path else 0.0

    return DTWResult(
        distance=float(total_distance),
        normalized_distance=float(normalized_distance),
        path=path,
        cost_matrix=cost[1:, 1:],  # Remove padding
    )


def dtw_similarity(
    seq1: np.ndarray,
    seq2: np.ndarray,
    metric: str = "euclidean",
) -> float:
    """Compute DTW-based similarity score (0-1, higher = more similar)

    Args:
        seq1: First sequence [n, features]
        seq2: Second sequence [m, features]
        metric: Distance metric

    Returns:
        Similarity score between 0 and 1
    """
    result = dtw_distance(seq1, seq2, metric=metric)

    # Convert distance to similarity using exponential decay
    max_dist = np.max(cdist(seq1, seq2, metric=metric))
    if max_dist < 1e-8:
        return 1.0

    similarity = np.exp(-result.normalized_distance / max_dist)
    return float(np.clip(similarity, 0.0, 1.0))


def align_sequences(
    seq1: np.ndarray,
    seq2: np.ndarray,
    metric: str = "euclidean",
) -> Tuple[np.ndarray, np.ndarray]:
    """Align two sequences using DTW

    Args:
        seq1: First sequence [n, features]
        seq2: Second sequence [m, features]

    Returns:
        (aligned_seq1, aligned_seq2) with same length
    """
    result = dtw_distance(seq1, seq2, metric=metric)

    aligned1 = np.array([seq1[i] for i, j in result.path])
    aligned2 = np.array([seq2[j] for i, j in result.path])

    return aligned1, aligned2


def compute_frame_deviations(
    user_seq: np.ndarray,
    reference_seq: np.ndarray,
    metric: str = "euclidean",
) -> np.ndarray:
    """Compute per-frame deviations after DTW alignment

    Args:
        user_seq: User's keypoint sequence [n, features]
        reference_seq: Reference template sequence [m, features]

    Returns:
        Deviation array [len(path)] with distance at each aligned frame
    """
    result = dtw_distance(user_seq, reference_seq, metric=metric)

    deviations = np.array([
        np.linalg.norm(user_seq[i] - reference_seq[j])
        for i, j in result.path
    ])

    return deviations


def find_best_match_window(
    long_seq: np.ndarray,
    short_seq: np.ndarray,
    stride: int = 1,
) -> Tuple[int, float]:
    """Find the window in long_seq that best matches short_seq

    Useful for finding stroke cycles in continuous video.

    Args:
        long_seq: Long sequence to search [n, features]
        short_seq: Short pattern to find [m, features]
        stride: Search stride

    Returns:
        (best_start_index, best_distance)
    """
    n, m = len(long_seq), len(short_seq)

    if m > n:
        return 0, float("inf")

    best_start = 0
    best_dist = float("inf")

    for start in range(0, n - m + 1, stride):
        window = long_seq[start:start + m]
        result = dtw_distance(window, short_seq)

        if result.normalized_distance < best_dist:
            best_dist = result.normalized_distance
            best_start = start

    return best_start, best_dist
