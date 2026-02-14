"""Stroke analysis for swimming technique evaluation

Analyzes swimming strokes using MediaPipe keypoints directly:
1. Detecting stroke cycles (arm entry-to-entry)
2. Computing joint angles per frame
3. Comparing with reference ranges from biomechanics literature
4. Generating deviations for feedback

Usage:
    from src.analysis.stroke_analyzer import StrokeAnalyzer

    analyzer = StrokeAnalyzer()
    results = analyzer.analyze(mediapipe_keypoints)  # [N, 33, 3]
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from scipy.signal import find_peaks

from .mediapipe_angles import (
    MP,
    JOINT_NAMES,
    FREESTYLE_REFERENCE,
    JointReference,
    get_all_joint_angles,
    evaluate_angle,
)
from ..utils.logging_config import get_logger

logger = get_logger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models"
DEFAULT_REFERENCE_PATH = MODELS_DIR / "freestyle_reference.json"

# Supported swimming styles
SUPPORTED_STYLES = ["freestyle", "backstroke", "breaststroke", "butterfly"]


@dataclass
class StrokeCycle:
    """Detected stroke cycle"""
    start_frame: int
    end_frame: int
    duration_frames: int
    dominant_arm: str  # "left" or "right"
    peak_frame: int


@dataclass
class JointDeviation:
    """Deviation of a joint angle from optimal range"""
    joint_name: str
    actual_angle: float
    expected_min: float
    expected_max: float
    deviation: float
    severity: str  # "minor", "moderate", "severe"
    frame: int


@dataclass
class CycleAnalysis:
    """Analysis of a single stroke cycle"""
    cycle: StrokeCycle
    joint_angles: Dict[str, np.ndarray]
    mean_angles: Dict[str, float]
    score: float
    deviations: List[JointDeviation]


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    style: str
    num_cycles: int
    cycles: List[CycleAnalysis]
    overall_score: float
    major_issues: List[str]
    summary: Dict[str, float] = field(default_factory=dict)


class StrokeAnalyzer:
    """Analyzes swimming stroke technique using MediaPipe keypoints"""

    def __init__(self, reference_path: Optional[Path] = None):
        """Initialize analyzer

        Args:
            reference_path: Path to reference JSON (optional, uses defaults if not provided)
        """
        self.reference: Dict[str, JointReference] = dict(FREESTYLE_REFERENCE)
        self.thresholds = {
            "minor_deviation": 10.0,
            "moderate_deviation": 20.0,
            "severe_deviation": 30.0,
        }

        if reference_path and reference_path.exists():
            self.load_reference(reference_path)

    def load_reference(self, reference_path: Path):
        """Load reference values from JSON"""
        with open(reference_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "joints" in data:
            for joint_name, values in data["joints"].items():
                self.reference[joint_name] = JointReference(
                    optimal_min=values["optimal_min"],
                    optimal_max=values["optimal_max"],
                    name_cs=values.get("name_cs", joint_name),
                )

        if "thresholds" in data:
            self.thresholds.update(data["thresholds"])

        logger.info(f"Loaded reference: {data.get('style', 'unknown')}")

    def _load_style_reference(self, style: str) -> None:
        """Load reference values for specific swimming style

        Args:
            style: Swimming style name
        """
        style_lower = style.lower()
        if style_lower not in SUPPORTED_STYLES:
            logger.warning(f"Unknown style '{style}', using freestyle reference")
            style_lower = "freestyle"

        reference_path = MODELS_DIR / f"{style_lower}_reference.json"
        if reference_path.exists():
            self.load_reference(reference_path)
        else:
            logger.warning(f"Reference not found: {reference_path}, using defaults")

    def detect_stroke_cycles(
        self,
        keypoints: np.ndarray,
        min_cycle_frames: int = 20,
        max_cycle_frames: int = 120,
    ) -> List[StrokeCycle]:
        """Detect stroke cycles from MediaPipe keypoint sequence

        Uses peaks in wrist Y-coordinate (arm entry points).

        Args:
            keypoints: MediaPipe keypoints [num_frames, 33, 3]
            min_cycle_frames: Minimum frames per cycle
            max_cycle_frames: Maximum frames per cycle

        Returns:
            List of detected stroke cycles
        """
        num_frames = keypoints.shape[0]

        # Get wrist positions from MediaPipe
        left_wrist_y = keypoints[:, MP.LEFT_WRIST, 1]
        right_wrist_y = keypoints[:, MP.RIGHT_WRIST, 1]

        cycles: List[StrokeCycle] = []

        for wrist_y, arm_name in [(left_wrist_y, "left"), (right_wrist_y, "right")]:
            # Smooth signal
            smoothed = np.convolve(wrist_y, np.ones(5) / 5, mode="same")

            # Determine prominence based on coordinate scale
            max_val = np.max(np.abs(smoothed)) if len(smoothed) > 0 else 1.0
            prominence = 0.05 if max_val <= 1.0 else 10

            logger.debug(f"{arm_name} wrist Y: min={smoothed.min():.3f}, max={smoothed.max():.3f}, "
                        f"range={smoothed.max()-smoothed.min():.3f}, prominence={prominence}")

            # Find peaks (minima for entry points - hand at highest point)
            peaks, _ = find_peaks(
                -smoothed,
                distance=min_cycle_frames,
                prominence=prominence,
            )

            logger.debug(f"{arm_name} wrist: found {len(peaks)} peaks at frames {peaks.tolist()[:10]}...")

            for i in range(len(peaks) - 1):
                start = peaks[i]
                end = peaks[i + 1]
                duration = end - start

                if min_cycle_frames <= duration <= max_cycle_frames:
                    cycles.append(StrokeCycle(
                        start_frame=start,
                        end_frame=end,
                        duration_frames=duration,
                        dominant_arm=arm_name,
                        peak_frame=start,
                    ))

        cycles.sort(key=lambda c: c.start_frame)
        return cycles

    def analyze_cycle(
        self,
        keypoints: np.ndarray,
        cycle: StrokeCycle,
    ) -> CycleAnalysis:
        """Analyze a single stroke cycle

        Args:
            keypoints: Full MediaPipe keypoint sequence [N, 33, 3]
            cycle: Stroke cycle to analyze

        Returns:
            CycleAnalysis with joint angles and deviations
        """
        cycle_kpts = keypoints[cycle.start_frame:cycle.end_frame]
        num_frames = cycle_kpts.shape[0]

        # Compute joint angles for each frame
        joint_angles: Dict[str, np.ndarray] = {
            name: np.zeros(num_frames) for name in JOINT_NAMES
        }

        for frame_idx in range(num_frames):
            angles = get_all_joint_angles(cycle_kpts[frame_idx])
            for joint_name, angle in angles.items():
                joint_angles[joint_name][frame_idx] = angle

        # Compute mean angles
        mean_angles = {
            name: float(np.mean(angles[angles > 0])) if np.any(angles > 0) else 0.0
            for name, angles in joint_angles.items()
        }

        # Compare with reference ranges
        deviations: List[JointDeviation] = []
        total_deviation = 0.0
        num_joints_checked = 0

        for joint_name, mean_angle in mean_angles.items():
            if mean_angle <= 0 or joint_name not in self.reference:
                continue

            ref = self.reference[joint_name]
            severity, deviation = evaluate_angle(joint_name, mean_angle, self.reference)

            num_joints_checked += 1

            if severity != "ok":
                total_deviation += deviation
                deviations.append(JointDeviation(
                    joint_name=joint_name,
                    actual_angle=mean_angle,
                    expected_min=ref.optimal_min,
                    expected_max=ref.optimal_max,
                    deviation=deviation,
                    severity=severity,
                    frame=cycle.start_frame + num_frames // 2,
                ))

        # Cycle score: 100 - penalty for deviations
        if num_joints_checked > 0:
            avg_deviation = total_deviation / num_joints_checked
            cycle_score = max(0, min(100, 100 - avg_deviation * 2))
        else:
            cycle_score = 50.0

        return CycleAnalysis(
            cycle=cycle,
            joint_angles=joint_angles,
            mean_angles=mean_angles,
            score=cycle_score,
            deviations=deviations,
        )

    def analyze(
        self,
        keypoints: np.ndarray,
        style: str = "freestyle",
    ) -> AnalysisResult:
        """Analyze full MediaPipe keypoint sequence

        Args:
            keypoints: MediaPipe keypoints [num_frames, 33, 3]
            style: Swimming style name

        Returns:
            AnalysisResult with all cycle analyses
        """
        # Load style-specific reference if available
        self._load_style_reference(style)

        # Detect cycles
        cycles = self.detect_stroke_cycles(keypoints)
        logger.info(f"Detected {len(cycles)} stroke cycles")

        # Analyze each cycle
        cycle_analyses: List[CycleAnalysis] = []
        for cycle in cycles:
            analysis = self.analyze_cycle(keypoints, cycle)
            cycle_analyses.append(analysis)

        # Aggregate results
        all_deviations: List[JointDeviation] = []
        total_score = 0.0

        for i, ca in enumerate(cycle_analyses):
            all_deviations.extend(ca.deviations)
            total_score += ca.score
            if i < 3:
                logger.debug(f"Cycle {i}: score={ca.score:.1f}, "
                           f"mean_angles={list(ca.mean_angles.items())[:3]}...")

        # Find major issues
        deviation_counts: Dict[str, int] = {}
        for dev in all_deviations:
            key = f"{dev.joint_name}_{dev.severity}"
            deviation_counts[key] = deviation_counts.get(key, 0) + 1

        major_issues = [
            key for key, count in deviation_counts.items()
            if "severe" in key or count > len(cycles) // 2
        ]

        # Overall score
        if cycle_analyses:
            overall_score = total_score / len(cycle_analyses)
            logger.debug(f"Score calculation: num_cycles={len(cycle_analyses)}, "
                        f"avg_score={overall_score:.1f}")
        else:
            overall_score = 0.0

        # Summary statistics
        summary = {}
        for joint_name in JOINT_NAMES:
            angles = [ca.mean_angles.get(joint_name, 0) for ca in cycle_analyses]
            valid_angles = [a for a in angles if a > 0]
            if valid_angles:
                summary[f"{joint_name}_mean"] = float(np.mean(valid_angles))
                summary[f"{joint_name}_std"] = float(np.std(valid_angles))

        return AnalysisResult(
            style=style,
            num_cycles=len(cycles),
            cycles=cycle_analyses,
            overall_score=overall_score,
            major_issues=major_issues,
            summary=summary,
        )

    def get_deviation_summary(self, result: AnalysisResult) -> Dict[str, List[str]]:
        """Get summary of deviations by severity"""
        summary: Dict[str, List[str]] = {
            "severe": [],
            "moderate": [],
            "minor": [],
        }

        seen = set()
        for cycle in result.cycles:
            for dev in cycle.deviations:
                key = f"{dev.joint_name}_{dev.severity}"
                if key not in seen:
                    seen.add(key)
                    summary[dev.severity].append(dev.joint_name)

        return summary
