"""Czech feedback generator for swimming technique analysis

Generates human-readable feedback in Czech language based on
stroke analysis results.

Usage:
    from src.analysis.feedback_generator import FeedbackGenerator

    generator = FeedbackGenerator()
    feedback = generator.generate(analysis_result)
    print(feedback.summary)
    for tip in feedback.tips:
        print(tip)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .stroke_analyzer import AnalysisResult, JointDeviation, CycleAnalysis, StrokeCycle


# Czech translation of joint names
JOINT_NAMES_CS = {
    "left_elbow": "levý loket",
    "right_elbow": "pravý loket",
    "left_shoulder": "levé rameno",
    "right_shoulder": "pravé rameno",
    "left_knee": "levé koleno",
    "right_knee": "pravé koleno",
    "left_hip": "levý kyčel",
    "right_hip": "pravý kyčel",
    "body_alignment": "držení těla",
    "left_arm_extension": "natažení levé paže",
    "right_arm_extension": "natažení pravé paže",
}

# Severity translations
SEVERITY_CS = {
    "severe": "závažná",
    "moderate": "střední",
    "minor": "mírná",
}

# Direction phrases
DIRECTION_CS = {
    "too_high": "příliš vysoko",
    "too_low": "příliš nízko",
    "too_bent": "příliš ohnutý",
    "too_straight": "příliš natažený",
    "too_narrow": "příliš úzký",
    "too_wide": "příliš široký",
}


@dataclass
class FeedbackMessage:
    """Single feedback message"""
    severity: str
    joint: str
    message: str
    tip: Optional[str] = None


@dataclass
class Feedback:
    """Complete feedback for analysis"""
    summary: str
    score: float
    score_label: str
    num_cycles: int = 0
    cycles: List[StrokeCycle] = field(default_factory=list)
    messages: List[FeedbackMessage] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    positive: List[str] = field(default_factory=list)


class FeedbackGenerator:
    """Generates Czech feedback from analysis results"""

    # Feedback templates (using optimal range format)
    TEMPLATES = {
        "elbow_too_bent": "{joint} příliš ohnutý ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
        "elbow_too_straight": "{joint} nedostatečně ohnutý ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
        "shoulder_angle": "{joint} mimo optimální rozsah ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
        "knee_too_bent": "{joint} příliš ohnuté ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
        "knee_ok": "{joint} v pořádku ({actual:.0f}°)",
        "hip_angle": "{joint} mimo optimální rozsah ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
        "generic": "{joint} - {severity} odchylka ({actual:.0f}°, optimum {min:.0f}-{max:.0f}°)",
    }

    # Tips for common issues
    TIPS = {
        "left_elbow": [
            "Při záběru levou rukou udržujte loket výše",
            "Zaměřte se na vysoký loket během fáze tahu",
        ],
        "right_elbow": [
            "Při záběru pravou rukou udržujte loket výše",
            "Zkuste cvičení s pádly pro lepší cit pro pozici lokte",
        ],
        "left_shoulder": [
            "Zlepšete rotaci těla pro efektivnější záběr",
            "Protahujte ramena před a po tréninku",
        ],
        "right_shoulder": [
            "Soustřeďte se na symetrii záběru obou rukou",
            "Přidejte rotační cviky do rozcvičky",
        ],
        "left_knee": [
            "Konejte uvolněně z kyčlí, ne z kolen",
            "Zkuste cvičení s ploutvemi pro lepší kopání",
        ],
        "right_knee": [
            "Udržujte kolena uvolněná při kopání",
            "Zaměřte se na rytmus kopání 6 kopů na jeden záběr",
        ],
        "body_alignment": [
            "Udržujte tělo v jedné linii - hlava, páteř, nohy",
            "Dívejte se na dno bazénu, ne dopředu",
            "Posilujte core pro lepší stabilitu",
        ],
    }

    # Score labels
    SCORE_LABELS = {
        90: "Výborná technika",
        75: "Dobrá technika",
        60: "Průměrná technika",
        40: "Technika potřebuje zlepšení",
        0: "Technika vyžaduje výrazné zlepšení",
    }

    def __init__(self, language: str = "cs"):
        """Initialize generator

        Args:
            language: Output language ("cs" for Czech)
        """
        self.language = language

    def generate(self, result: AnalysisResult) -> Feedback:
        """Generate feedback from analysis result

        Args:
            result: AnalysisResult from StrokeAnalyzer

        Returns:
            Feedback with summary, messages, and tips
        """
        # Get score label
        score_label = "Nedostatek dat"
        for threshold, label in sorted(self.SCORE_LABELS.items(), reverse=True):
            if result.overall_score >= threshold:
                score_label = label
                break

        # Generate summary
        summary = self._generate_summary(result)

        # Generate messages for deviations
        messages: List[FeedbackMessage] = []
        tips_set: set = set()

        for cycle in result.cycles:
            for dev in cycle.deviations:
                msg = self._deviation_to_message(dev)
                if msg:
                    messages.append(msg)

                    # Add relevant tips
                    if dev.joint_name in self.TIPS:
                        for tip in self.TIPS[dev.joint_name]:
                            tips_set.add(tip)

        # Deduplicate messages by joint
        seen_joints: set = set()
        unique_messages: List[FeedbackMessage] = []
        for msg in messages:
            if msg.joint not in seen_joints:
                seen_joints.add(msg.joint)
                unique_messages.append(msg)

        # Sort by severity
        severity_order = {"severe": 0, "moderate": 1, "minor": 2}
        unique_messages.sort(key=lambda m: severity_order.get(m.severity, 3))

        # Generate positive feedback
        positive = self._generate_positive(result, seen_joints)

        return Feedback(
            summary=summary,
            score=result.overall_score,
            score_label=score_label,
            num_cycles=result.num_cycles,
            cycles=[c.cycle for c in result.cycles],
            messages=unique_messages,
            tips=list(tips_set)[:5],  # Max 5 tips
            positive=positive,
        )

    def _generate_summary(self, result: AnalysisResult) -> str:
        """Generate summary text"""
        if result.num_cycles == 0:
            return "Nepodařilo se detekovat žádné cykly tahu. Zkuste delší video."

        cycle_text = f"Analyzováno {result.num_cycles} cyklů tahu"

        if result.overall_score >= 75:
            quality = "Celková technika je dobrá"
        elif result.overall_score >= 50:
            quality = "Technika má prostor pro zlepšení"
        else:
            quality = "Doporučujeme zaměřit se na základy techniky"

        severe_count = sum(
            1 for c in result.cycles
            for d in c.deviations if d.severity == "severe"
        )

        if severe_count > 0:
            issues = f"Nalezeno {severe_count} závažných odchylek"
        else:
            issues = "Žádné závažné odchylky"

        return f"{cycle_text}. {quality}. {issues}."

    def _deviation_to_message(self, dev: JointDeviation) -> Optional[FeedbackMessage]:
        """Convert deviation to feedback message"""
        joint_cs = JOINT_NAMES_CS.get(dev.joint_name, dev.joint_name)
        severity_cs = SEVERITY_CS.get(dev.severity, dev.severity)

        # Select template based on joint type and direction
        if "elbow" in dev.joint_name:
            if dev.actual_angle < dev.expected_min:
                template = self.TEMPLATES["elbow_too_bent"]
            else:
                template = self.TEMPLATES["elbow_too_straight"]
        elif "shoulder" in dev.joint_name:
            template = self.TEMPLATES["shoulder_angle"]
        elif "knee" in dev.joint_name:
            template = self.TEMPLATES["knee_too_bent"]
        elif "hip" in dev.joint_name:
            template = self.TEMPLATES["hip_angle"]
        else:
            template = self.TEMPLATES["generic"]

        message = template.format(
            joint=joint_cs.capitalize(),
            severity=severity_cs,
            actual=dev.actual_angle,
            min=dev.expected_min,
            max=dev.expected_max,
        )

        return FeedbackMessage(
            severity=dev.severity,
            joint=dev.joint_name,
            message=message,
            tip=self.TIPS.get(dev.joint_name, [""])[0] if dev.joint_name in self.TIPS else None,
        )

    def _generate_positive(
        self,
        result: AnalysisResult,
        problem_joints: set
    ) -> List[str]:
        """Generate positive feedback for good aspects"""
        positive: List[str] = []

        all_joints = set(JOINT_NAMES_CS.keys())
        good_joints = all_joints - problem_joints

        if "body_alignment" in good_joints:
            positive.append("Dobré držení těla ve vodě")

        if "left_elbow" in good_joints and "right_elbow" in good_joints:
            positive.append("Správná technika záběru lokty")

        if "left_shoulder" in good_joints and "right_shoulder" in good_joints:
            positive.append("Dobrá rotace ramen")

        if "left_knee" in good_joints and "right_knee" in good_joints:
            positive.append("Efektivní kopání z kyčlí")

        if result.num_cycles >= 5:
            # Check consistency
            if result.summary:
                stds = [v for k, v in result.summary.items() if k.endswith("_std")]
                if stds and sum(stds) / len(stds) < 10:
                    positive.append("Konzistentní technika napříč cykly")

        return positive[:3]  # Max 3 positive points

    def format_for_display(self, feedback: Feedback) -> str:
        """Format feedback for text display

        Returns:
            Formatted multi-line string
        """
        lines = []

        # Header
        lines.append(f"=== ANALÝZA PLAVECKÉ TECHNIKY ===")
        lines.append(f"Skóre: {feedback.score:.0f}/100 ({feedback.score_label})")
        lines.append("")

        # Summary
        lines.append(feedback.summary)
        lines.append("")

        # Issues
        if feedback.messages:
            lines.append("--- Zjištěné odchylky ---")
            for msg in feedback.messages:
                severity_icon = {"severe": "❌", "moderate": "⚠️", "minor": "ℹ️"}.get(
                    msg.severity, "•"
                )
                lines.append(f"{severity_icon} {msg.message}")
            lines.append("")

        # Positive
        if feedback.positive:
            lines.append("--- Pozitivní aspekty ---")
            for p in feedback.positive:
                lines.append(f"✅ {p}")
            lines.append("")

        # Tips
        if feedback.tips:
            lines.append("--- Tipy na zlepšení ---")
            for i, tip in enumerate(feedback.tips, 1):
                lines.append(f"{i}. {tip}")

        return "\n".join(lines)
