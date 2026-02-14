"""Feedback widget for displaying swimming technique analysis results"""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPainter, QColor

from ..analysis.feedback_generator import Feedback, FeedbackMessage
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class ScoreCircle(QWidget):
    """Circular score indicator widget"""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._score: float = 0
        self.setMinimumSize(100, 100)
        self.setMaximumSize(100, 100)

    def set_score(self, score: float) -> None:
        self._score = score
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(60, 60, 60))
        painter.drawEllipse(rect)

        # Score arc
        color = self._get_score_color()
        painter.setBrush(color)

        span_angle = int(self._score * 360 / 100 * 16)
        painter.drawPie(rect, 90 * 16, -span_angle)

        # Inner circle (donut effect)
        inner_rect = rect.adjusted(15, 15, -15, -15)
        painter.setBrush(QColor(40, 40, 40))
        painter.drawEllipse(inner_rect)

        # Score text
        painter.setPen(QColor(255, 255, 255))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{int(self._score)}")

    def _get_score_color(self) -> QColor:
        if self._score >= 75:
            return QColor(76, 175, 80)  # Green
        elif self._score >= 50:
            return QColor(255, 193, 7)  # Yellow
        else:
            return QColor(244, 67, 54)  # Red


class FeedbackWidget(QWidget):
    """Widget for displaying analysis feedback"""

    analysis_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._init_ui()
        logger.info("Feedback widget initialized")

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Header with score
        header_layout = QHBoxLayout()

        self.score_circle = ScoreCircle()
        header_layout.addWidget(self.score_circle)

        score_info_layout = QVBoxLayout()
        self.score_label = QLabel("--")
        self.score_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #888;")
        score_info_layout.addWidget(self.score_label)

        self.style_label = QLabel("")
        self.style_label.setStyleSheet("font-size: 12px; color: #666;")
        score_info_layout.addWidget(self.style_label)

        self.cycles_label = QLabel("")
        self.cycles_label.setStyleSheet("font-size: 11px; color: #888;")
        score_info_layout.addWidget(self.cycles_label)
        score_info_layout.addStretch()

        header_layout.addLayout(score_info_layout)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Summary
        self.summary_label = QLabel("Nahrajte video a spusťte analýzu")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("font-size: 12px; padding: 5px; background: #2a2a2a; border-radius: 4px;")
        self.summary_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_layout.addWidget(self.summary_label)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # Issues group
        self.issues_group = QGroupBox("Zjištěné odchylky")
        self.issues_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.issues_layout = QVBoxLayout(self.issues_group)
        self.issues_layout.setSpacing(5)
        scroll_layout.addWidget(self.issues_group)

        # Positive group
        self.positive_group = QGroupBox("Pozitivní aspekty")
        self.positive_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.positive_layout = QVBoxLayout(self.positive_group)
        self.positive_layout.setSpacing(5)
        scroll_layout.addWidget(self.positive_group)

        # Tips group
        self.tips_group = QGroupBox("Tipy na zlepšení")
        self.tips_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.tips_layout = QVBoxLayout(self.tips_group)
        self.tips_layout.setSpacing(5)
        scroll_layout.addWidget(self.tips_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Loading indicator
        self.loading_label = QLabel("Analyzuji...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 14px; color: #888;")
        self.loading_label.setVisible(False)
        main_layout.addWidget(self.loading_label)

        self.setMinimumWidth(280)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Initial state
        self._set_empty_state()

    def _set_empty_state(self) -> None:
        self.score_circle.set_score(0)
        self.score_label.setText("--")
        self.style_label.setText("")
        self.cycles_label.setText("")
        self.issues_group.setVisible(False)
        self.positive_group.setVisible(False)
        self.tips_group.setVisible(False)

    def _clear_layout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def update_feedback(self, feedback: Feedback) -> None:
        """Update widget with analysis feedback

        Args:
            feedback: Feedback from FeedbackGenerator
        """
        logger.info(f"Updating feedback: score={feedback.score:.1f}")

        # Score
        self.score_circle.set_score(feedback.score)
        self.score_label.setText(feedback.score_label)

        # Cycles count
        if feedback.num_cycles > 0:
            self.cycles_label.setText(f"Cyklů: {feedback.num_cycles}")
        else:
            self.cycles_label.setText("")

        # Summary
        self.summary_label.setText(feedback.summary)

        # Issues
        self._clear_layout(self.issues_layout)
        if feedback.messages:
            self.issues_group.setVisible(True)
            for msg in feedback.messages:
                issue_widget = self._create_issue_widget(msg)
                self.issues_layout.addWidget(issue_widget)
        else:
            self.issues_group.setVisible(False)

        # Positive
        self._clear_layout(self.positive_layout)
        if feedback.positive:
            self.positive_group.setVisible(True)
            for text in feedback.positive:
                label = QLabel(f"✓ {text}")
                label.setWordWrap(True)
                label.setStyleSheet("color: #4CAF50; padding: 2px;")
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.positive_layout.addWidget(label)
        else:
            self.positive_group.setVisible(False)

        # Tips
        self._clear_layout(self.tips_layout)
        if feedback.tips:
            self.tips_group.setVisible(True)
            for i, tip in enumerate(feedback.tips, 1):
                label = QLabel(f"{i}. {tip}")
                label.setWordWrap(True)
                label.setStyleSheet("padding: 2px;")
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.tips_layout.addWidget(label)
        else:
            self.tips_group.setVisible(False)

        self.loading_label.setVisible(False)

    def _create_issue_widget(self, msg: FeedbackMessage) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        severity_colors = {
            "severe": "#F44336",
            "moderate": "#FF9800",
            "minor": "#2196F3",
        }
        color = severity_colors.get(msg.severity, "#888")
        frame.setStyleSheet(f"QFrame {{ border-left: 3px solid {color}; padding: 5px; background: #2a2a2a; }}")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 5, 5, 5)
        layout.setSpacing(2)

        severity_icons = {
            "severe": "⚠",
            "moderate": "●",
            "minor": "○",
        }
        icon = severity_icons.get(msg.severity, "•")

        message_label = QLabel(f"{icon} {msg.message}")
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"font-weight: bold; color: {color};")
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(message_label)

        if msg.tip:
            tip_label = QLabel(f"→ {msg.tip}")
            tip_label.setWordWrap(True)
            tip_label.setStyleSheet("color: #888; font-size: 11px;")
            tip_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            layout.addWidget(tip_label)

        return frame

    def set_loading(self, loading: bool) -> None:
        """Show/hide loading indicator

        Args:
            loading: True to show loading state
        """
        self.loading_label.setVisible(loading)
        if loading:
            self.summary_label.setText("Probíhá analýza techniky...")
            self._set_empty_state()

    def set_style(self, style: str) -> None:
        """Set detected swimming style

        Args:
            style: Swimming style name
        """
        style_names = {
            "freestyle": "Kraul",
            "backstroke": "Znak",
            "breaststroke": "Prsa",
            "butterfly": "Motýlek",
        }
        self.style_label.setText(style_names.get(style, style))

    def clear(self) -> None:
        """Clear all feedback content"""
        self._set_empty_state()
        self.summary_label.setText("Nahrajte video a spusťte analýzu")
        self._clear_layout(self.issues_layout)
        self._clear_layout(self.positive_layout)
        self._clear_layout(self.tips_layout)

    def show_error(self, message: str) -> None:
        """Display error message

        Args:
            message: Error message to display
        """
        self.loading_label.setVisible(False)
        self.summary_label.setText(f"Chyba: {message}")
        self.summary_label.setStyleSheet(
            "font-size: 12px; padding: 5px; background: #4a2020; border-radius: 4px; color: #F44336;"
        )
        self._set_empty_state()
