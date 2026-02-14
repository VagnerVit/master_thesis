"""JSON export for swimming analysis results

Usage:
    from src.export.json_exporter import export_to_json
    from src.analysis.feedback_generator import Feedback

    export_to_json(feedback, video_path, output_path)
"""

import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from src.analysis.feedback_generator import Feedback, FeedbackMessage

logger = logging.getLogger(__name__)

APP_VERSION = "1.0.0"


def _feedback_to_dict(feedback: Feedback) -> Dict[str, Any]:
    """Convert Feedback dataclass to serializable dict"""
    return {
        "summary": feedback.summary,
        "score": feedback.score,
        "score_label": feedback.score_label,
        "issues": [
            {
                "severity": msg.severity,
                "joint": msg.joint,
                "message": msg.message,
                "tip": msg.tip,
            }
            for msg in feedback.messages
        ],
        "positive": feedback.positive,
        "tips": feedback.tips,
    }


def export_to_json(
    feedback: Feedback,
    video_path: str,
    output_path: Path,
    style: str = "freestyle",
    num_cycles: int = 0,
) -> None:
    """Export analysis results to JSON file

    Args:
        feedback: Feedback object from FeedbackGenerator
        video_path: Path to analyzed video
        output_path: Output path for JSON file
        style: Swimming style (default: freestyle)
        num_cycles: Number of stroke cycles analyzed
    """
    export_data = {
        "metadata": {
            "video_path": str(video_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "app_version": APP_VERSION,
        },
        "analysis": {
            "style": style,
            "score": feedback.score,
            "score_label": feedback.score_label,
            "summary": feedback.summary,
            "num_cycles": num_cycles,
        },
        "feedback": _feedback_to_dict(feedback),
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    logger.info(f"Analysis exported to JSON: {output_path}")


def load_from_json(json_path: Path) -> Dict[str, Any]:
    """Load analysis from JSON file

    Args:
        json_path: Path to JSON file

    Returns:
        Dict with analysis data
    """
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
