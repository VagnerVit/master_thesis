"""PDF export for swimming analysis results

Generates a formatted PDF report with:
- Title and metadata
- Score visualization
- Feedback sections (issues, positive, tips)

Usage:
    from src.export.pdf_exporter import export_to_pdf
    from src.analysis.feedback_generator import Feedback

    export_to_pdf(feedback, video_path, output_path)
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.analysis.feedback_generator import Feedback

logger = logging.getLogger(__name__)

APP_VERSION = "1.0.0"


def _get_score_color(score: float) -> colors.Color:
    """Get color based on score value"""
    if score >= 75:
        return colors.Color(0.2, 0.7, 0.3)  # Green
    elif score >= 50:
        return colors.Color(0.9, 0.7, 0.1)  # Yellow/Orange
    else:
        return colors.Color(0.8, 0.2, 0.2)  # Red


def _create_styles() -> dict:
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    custom_styles = {
        "Title": ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.Color(0.1, 0.3, 0.6),
        ),
        "Heading": ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.Color(0.2, 0.2, 0.2),
        ),
        "Body": ParagraphStyle(
            "CustomBody",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
        ),
        "Issue": ParagraphStyle(
            "Issue",
            parent=styles["Normal"],
            fontSize=10,
            leftIndent=10,
            bulletIndent=0,
        ),
        "Positive": ParagraphStyle(
            "Positive",
            parent=styles["Normal"],
            fontSize=10,
            leftIndent=10,
            textColor=colors.Color(0.2, 0.6, 0.3),
        ),
        "Tip": ParagraphStyle(
            "Tip",
            parent=styles["Normal"],
            fontSize=10,
            leftIndent=10,
            textColor=colors.Color(0.3, 0.3, 0.6),
        ),
        "Footer": ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.gray,
        ),
    }

    return custom_styles


def _build_score_table(score: float, score_label: str) -> Table:
    """Create score visualization table"""
    score_color = _get_score_color(score)

    data = [
        ["Celkové skóre", f"{score:.0f}/100"],
        ["Hodnocení", score_label],
    ]

    table = Table(data, colWidths=[6 * cm, 4 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.95, 0.95, 0.95)),
        ("TEXTCOLOR", (1, 0), (1, 0), score_color),
        ("FONTSIZE", (1, 0), (1, 0), 18),
        ("FONTSIZE", (0, 0), (0, -1), 11),
        ("FONTSIZE", (1, 1), (1, 1), 12),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
    ]))

    return table


def export_to_pdf(
    feedback: Feedback,
    video_path: str,
    output_path: Path,
    style: str = "freestyle",
    num_cycles: int = 0,
) -> None:
    """Export analysis results to PDF report

    Args:
        feedback: Feedback object from FeedbackGenerator
        video_path: Path to analyzed video
        output_path: Output path for PDF file
        style: Swimming style (default: freestyle)
        num_cycles: Number of stroke cycles analyzed
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = _create_styles()
    story: List = []

    # Title
    story.append(Paragraph("SwimAth - Analýza techniky", styles["Title"]))
    story.append(Spacer(1, 5 * mm))

    # Metadata
    timestamp = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M")
    video_name = Path(video_path).name
    meta_text = f"Video: {video_name}<br/>Styl: {style.capitalize()}<br/>Datum: {timestamp}"
    story.append(Paragraph(meta_text, styles["Body"]))
    story.append(Spacer(1, 10 * mm))

    # Score
    story.append(_build_score_table(feedback.score, feedback.score_label))
    story.append(Spacer(1, 10 * mm))

    # Summary
    story.append(Paragraph("Shrnutí", styles["Heading"]))
    story.append(Paragraph(feedback.summary, styles["Body"]))
    story.append(Spacer(1, 5 * mm))

    # Issues
    if feedback.messages:
        story.append(Paragraph("Zjištěné odchylky", styles["Heading"]))
        for msg in feedback.messages:
            severity_icon = "⚠️" if msg.severity == "severe" else "⚡"
            story.append(Paragraph(
                f"{severity_icon} {msg.message}",
                styles["Issue"]
            ))
        story.append(Spacer(1, 5 * mm))

    # Positive aspects
    if feedback.positive:
        story.append(Paragraph("Pozitivní aspekty", styles["Heading"]))
        for pos in feedback.positive:
            story.append(Paragraph(f"✓ {pos}", styles["Positive"]))
        story.append(Spacer(1, 5 * mm))

    # Tips
    if feedback.tips:
        story.append(Paragraph("Tipy na zlepšení", styles["Heading"]))
        for tip in feedback.tips:
            story.append(Paragraph(f"💡 {tip}", styles["Tip"]))
        story.append(Spacer(1, 5 * mm))

    # Footer
    story.append(Spacer(1, 15 * mm))
    footer_text = f"Vygenerováno aplikací SwimAth v{APP_VERSION}"
    story.append(Paragraph(footer_text, styles["Footer"]))

    doc.build(story)
    logger.info(f"Analysis exported to PDF: {output_path}")
