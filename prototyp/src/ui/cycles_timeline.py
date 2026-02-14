"""Timeline widget for visualizing detected stroke cycles"""

from typing import List, Optional

from PySide6.QtWidgets import QWidget, QToolTip
from PySide6.QtCore import Qt, Signal, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QMouseEvent

from ..analysis.stroke_analyzer import StrokeCycle
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class CyclesTimelineWidget(QWidget):
    """Widget that displays stroke cycles on a timeline

    Cycles are shown as colored rectangles. Clicking on a cycle
    emits a signal with the frame number to seek to.
    """

    cycle_clicked = Signal(int)  # Frame number to seek to

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._cycles: List[StrokeCycle] = []
        self._total_frames: int = 0
        self._current_frame: int = 0
        self._cycle_rects: List[tuple[QRect, StrokeCycle]] = []

        self.setMinimumHeight(30)
        self.setMaximumHeight(40)
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def set_total_frames(self, total: int) -> None:
        """Set total number of frames in video

        Args:
            total: Total frame count
        """
        self._total_frames = max(1, total)
        self._update_cycle_rects()
        self.update()

    def update_cycles(self, cycles: List[StrokeCycle]) -> None:
        """Update displayed cycles

        Args:
            cycles: List of detected stroke cycles
        """
        self._cycles = cycles
        self._update_cycle_rects()
        self.update()
        logger.info(f"Timeline updated with {len(cycles)} cycles")

    def set_current_frame(self, frame: int) -> None:
        """Set current playback position

        Args:
            frame: Current frame number
        """
        self._current_frame = frame
        self.update()

    def clear(self) -> None:
        """Clear all cycles from timeline"""
        self._cycles = []
        self._cycle_rects = []
        self._current_frame = 0
        self.update()

    def _update_cycle_rects(self) -> None:
        """Recalculate rectangle positions for cycles"""
        self._cycle_rects = []
        if not self._cycles or self._total_frames <= 0:
            return

        width: int = self.width() - 4
        height: int = self.height() - 8

        for cycle in self._cycles:
            x: int = int(2 + (cycle.start_frame / self._total_frames) * width)
            w: int = max(4, int((cycle.duration_frames / self._total_frames) * width))
            rect = QRect(x, 4, w, height)
            self._cycle_rects.append((rect, cycle))

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width: int = self.width()
        height: int = self.height()

        # Background
        painter.fillRect(0, 0, width, height, QColor(45, 45, 45))

        # Timeline track
        track_rect = QRect(2, height // 2 - 2, width - 4, 4)
        painter.fillRect(track_rect, QColor(60, 60, 60))

        if not self._cycles or self._total_frames <= 0:
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.rect(), Qt.AlignCenter, "Žádné cykly")
            return

        # Draw cycles
        left_color = QColor(66, 165, 245)   # Blue for left arm
        right_color = QColor(239, 83, 80)   # Red for right arm

        for rect, cycle in self._cycle_rects:
            color = left_color if cycle.dominant_arm == "left" else right_color
            painter.fillRect(rect, color)

            # Border
            painter.setPen(QPen(color.darker(120), 1))
            painter.drawRect(rect)

        # Current position marker
        if self._total_frames > 0:
            pos_x: int = int(2 + (self._current_frame / self._total_frames) * (width - 4))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawLine(pos_x, 0, pos_x, height)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_cycle_rects()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return

        pos = event.position().toPoint()

        # Check if clicked on a cycle
        for rect, cycle in self._cycle_rects:
            if rect.contains(pos):
                self.cycle_clicked.emit(cycle.peak_frame)
                logger.debug(f"Cycle clicked: frame {cycle.peak_frame}")
                return

        # Click on empty area - seek to that position
        if self._total_frames > 0:
            frame: int = int((pos.x() - 2) / (self.width() - 4) * self._total_frames)
            frame = max(0, min(frame, self._total_frames - 1))
            self.cycle_clicked.emit(frame)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position().toPoint()

        for rect, cycle in self._cycle_rects:
            if rect.contains(pos):
                arm_text = "levá" if cycle.dominant_arm == "left" else "pravá"
                tooltip = (
                    f"Cyklus: {arm_text} paže\n"
                    f"Snímky: {cycle.start_frame}-{cycle.end_frame}\n"
                    f"Délka: {cycle.duration_frames} snímků"
                )
                QToolTip.showText(event.globalPosition().toPoint(), tooltip, self)
                return

        QToolTip.hideText()
