"""Main window for SwimAth application"""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QStatusBar,
    QMenuBar, QMenu, QMessageBox, QProgressBar, QSplitter, QSlider
)
from PySide6.QtCore import Qt, QTimer, Signal

from PySide6.QtGui import QAction

from .video_player import VideoPlayer
from .feedback_widget import FeedbackWidget
from .analysis_worker import AnalysisWorker
from .cycles_timeline import CyclesTimelineWidget
from ..analysis.feedback_generator import Feedback
from ..export import export_to_json, export_to_pdf
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.current_video_path: Optional[Path] = None
        self._analysis_worker: Optional[AnalysisWorker] = None
        self._current_feedback: Optional[Feedback] = None
        self._video_duration: float = 0.0
        self._video_total_frames: int = 0
        self._slider_dragging: bool = False
        self._init_ui()
        self._connect_signals()

        logger.info("Main window initialized")

    def _init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("SwimAth - Swimming Style Analysis")
        self.setGeometry(100, 100, 1280, 720)

        # Create menu bar
        self._create_menu_bar()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Content splitter (video + feedback side by side)
        self.content_splitter = QSplitter(Qt.Horizontal)

        # Video player
        self.video_player = VideoPlayer()
        self.content_splitter.addWidget(self.video_player)

        # Feedback widget
        self.feedback_widget = FeedbackWidget()
        self.content_splitter.addWidget(self.feedback_widget)

        # Set splitter sizes (70% video, 30% feedback)
        self.content_splitter.setSizes([900, 380])
        self.content_splitter.setStretchFactor(0, 2)
        self.content_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.content_splitter)

        # Cycles timeline
        self.cycles_timeline = CyclesTimelineWidget()
        main_layout.addWidget(self.cycles_timeline)

        # Control panel
        control_layout = self._create_control_panel()
        main_layout.addLayout(control_layout)

        # Status bar
        self._create_status_bar()

    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open Video...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_video)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Analysis menu
        analysis_menu = menubar.addMenu("&Analysis")

        start_analysis_action = QAction("&Start Analysis", self)
        start_analysis_action.setShortcut("Ctrl+R")
        start_analysis_action.triggered.connect(self._on_start_analysis)
        analysis_menu.addAction(start_analysis_action)

        stop_analysis_action = QAction("St&op Analysis", self)
        stop_analysis_action.triggered.connect(self._on_stop_analysis)
        analysis_menu.addAction(stop_analysis_action)

        analysis_menu.addSeparator()

        # Export actions
        self.export_json_action = QAction("Export &JSON...", self)
        self.export_json_action.setShortcut("Ctrl+E")
        self.export_json_action.setEnabled(False)
        self.export_json_action.triggered.connect(self._on_export_json)
        analysis_menu.addAction(self.export_json_action)

        self.export_pdf_action = QAction("Export &PDF...", self)
        self.export_pdf_action.setShortcut("Ctrl+Shift+E")
        self.export_pdf_action.setEnabled(False)
        self.export_pdf_action.triggered.connect(self._on_export_pdf)
        analysis_menu.addAction(self.export_pdf_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_control_panel(self) -> QHBoxLayout:
        """Create control panel with buttons

        Returns:
            Control panel layout
        """
        layout = QHBoxLayout()

        # Open video button
        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self._on_open_video)
        layout.addWidget(self.open_button)

        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self._on_play)
        layout.addWidget(self.play_button)

        # Pause button
        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self._on_pause)
        layout.addWidget(self.pause_button)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._on_stop)
        layout.addWidget(self.stop_button)

        # Replay button
        self.replay_button = QPushButton("Replay")
        self.replay_button.setEnabled(False)
        self.replay_button.clicked.connect(self._on_replay)
        layout.addWidget(self.replay_button)

        # Seek slider
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setEnabled(False)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)
        self.seek_slider.setValue(0)
        self.seek_slider.setMinimumWidth(200)
        self.seek_slider.sliderPressed.connect(self._on_slider_pressed)
        self.seek_slider.sliderReleased.connect(self._on_slider_released)
        layout.addWidget(self.seek_slider)

        # Time label
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setMinimumWidth(80)
        layout.addWidget(self.time_label)

        # Frame counter (keypoints collected)
        self.frame_counter_label = QLabel("Framů: 0")
        self.frame_counter_label.setStyleSheet("color: #888; font-size: 11px;")
        self.frame_counter_label.setMinimumWidth(70)
        self.frame_counter_label.setToolTip("Počet framů s detekovanou pose pro analýzu")
        layout.addWidget(self.frame_counter_label)

        layout.addStretch()

        # Analyze full video button
        self.analyze_full_button = QPushButton("Analyzovat celé video")
        self.analyze_full_button.setEnabled(False)
        self.analyze_full_button.clicked.connect(self._on_analyze_full_video)
        self.analyze_full_button.setToolTip("Zpracuje celé video na pozadí a provede analýzu")
        layout.addWidget(self.analyze_full_button)

        # Start analysis button (for current frames)
        self.analyze_button = QPushButton("Analyzovat")
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self._on_start_analysis)
        self.analyze_button.setToolTip("Analyzovat dosud nasbírané framy")
        layout.addWidget(self.analyze_button)

        # Export button
        self.export_button = QPushButton("Export")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self._on_export_menu)
        layout.addWidget(self.export_button)

        return layout

    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _connect_signals(self):
        """Connect signals and slots"""
        self.video_player.video_opened.connect(self._on_video_opened)
        self.video_player.playback_state_changed.connect(self._on_playback_state_changed)
        self.video_player.video_progress.connect(self._on_video_progress)
        self.video_player.video_ended.connect(self._on_video_ended)

        # Cycles timeline
        self.cycles_timeline.cycle_clicked.connect(self._on_cycle_clicked)

    def _on_open_video(self):
        """Handle open video action"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            str(Path.home()),
            "Video Files (*.mp4 *.avi *.mov *.mkv *.webm);;All Files (*.*)"
        )

        if file_path:
            self.current_video_path = Path(file_path)
            logger.info(f"Opening video: {self.current_video_path}")

            success = self.video_player.open_video(self.current_video_path)

            if success:
                self.status_label.setText(f"Opened: {self.current_video_path.name}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to open video file:\n{self.current_video_path}"
                )
                logger.error(f"Failed to open video: {self.current_video_path}")

    def _on_video_opened(self, video_info: dict):
        """Handle video opened signal

        Args:
            video_info: Dictionary with video properties
        """
        logger.info(f"Video opened: {video_info}")

        # Store video info
        self._video_duration = video_info['duration']
        self._video_total_frames = video_info['total_frames']

        # Enable controls
        self.play_button.setEnabled(True)
        self.analyze_button.setEnabled(False)  # Enable after collecting frames
        self.analyze_full_button.setEnabled(True)
        self.seek_slider.setEnabled(True)
        self.seek_slider.setValue(0)

        # Reset frame counter
        self.frame_counter_label.setText("Framů: 0")

        # Reset and configure cycles timeline
        self.cycles_timeline.clear()
        self.cycles_timeline.set_total_frames(self._video_total_frames)

        # Update time label
        duration_str = self._format_time(self._video_duration)
        self.time_label.setText(f"0:00 / {duration_str}")

        # Update status
        self.status_label.setText(
            f"Video: {video_info['width']}x{video_info['height']}, "
            f"{video_info['fps']:.2f} FPS, {video_info['duration']:.2f}s"
        )

    def _on_playback_state_changed(self, state: str):
        """Handle playback state change

        Args:
            state: Playback state (playing, paused, stopped)
        """
        if state == "playing":
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.replay_button.setEnabled(False)
        elif state == "paused":
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.replay_button.setEnabled(True)

            # Auto-analyze on pause if frames collected
            keypoint_count = self.video_player.get_keypoint_count()
            if keypoint_count >= 30:  # Minimum frames for analysis
                logger.info(f"Auto-analyzing {keypoint_count} frames on pause")
                self._on_start_analysis()
        elif state == "stopped":
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.replay_button.setEnabled(True)

    def _on_play(self):
        """Handle play button"""
        logger.debug("Play button clicked")
        self.video_player.play()

    def _on_pause(self):
        """Handle pause button"""
        logger.debug("Pause button clicked")
        self.video_player.pause()

    def _on_stop(self):
        """Handle stop button"""
        logger.debug("Stop button clicked")
        self.video_player.stop()

    def _on_replay(self):
        """Handle replay button"""
        logger.debug("Replay button clicked")
        self.video_player.replay()

    def _on_video_progress(self, current_frame: int, total_frames: int):
        """Handle video progress update

        Args:
            current_frame: Current frame number
            total_frames: Total frames in video
        """
        if self._slider_dragging or total_frames == 0:
            return

        # Update slider
        position = int((current_frame / total_frames) * 1000)
        self.seek_slider.setValue(position)

        # Update time label
        if self._video_duration > 0:
            current_time = (current_frame / total_frames) * self._video_duration
            current_str = self._format_time(current_time)
            duration_str = self._format_time(self._video_duration)
            self.time_label.setText(f"{current_str} / {duration_str}")

        # Update cycles timeline position
        self.cycles_timeline.set_current_frame(current_frame)

        # Update frame counter
        keypoint_count = self.video_player.get_keypoint_count()
        self.frame_counter_label.setText(f"Framů: {keypoint_count}")
        if keypoint_count > 0:
            self.analyze_button.setEnabled(True)

    def _on_video_ended(self):
        """Handle video end"""
        logger.info("Video playback ended")
        self.replay_button.setEnabled(True)

    def _on_slider_pressed(self):
        """Handle slider press (start dragging)"""
        self._slider_dragging = True

    def _on_slider_released(self):
        """Handle slider release (seek to position)"""
        self._slider_dragging = False
        position = self.seek_slider.value() / 1000.0
        self.video_player.seek(position)

    def _on_cycle_clicked(self, frame: int):
        """Handle click on cycle in timeline

        Args:
            frame: Frame number to seek to
        """
        if self._video_total_frames > 0:
            position: float = frame / self._video_total_frames
            self.video_player.seek(position)
            logger.debug(f"Seeking to frame {frame} (position {position:.3f})")

    def _format_time(self, seconds: float) -> str:
        """Format seconds as M:SS or H:MM:SS

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        seconds = max(0, seconds)
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def _on_start_analysis(self):
        """Handle start analysis action"""
        if self.current_video_path is None:
            QMessageBox.warning(
                self,
                "Žádné video",
                "Nejprve otevřete video soubor."
            )
            return

        # Check if we have keypoints
        keypoints = self.video_player.get_collected_keypoints()
        if keypoints is None or len(keypoints) < 30:
            QMessageBox.warning(
                self,
                "Nedostatek dat",
                f"Přehrajte video pro sběr dat.\n"
                f"Sesbíráno snímků: {self.video_player.get_keypoint_count()}\n"
                f"Minimum: 30 snímků"
            )
            return

        # Cancel existing analysis
        if self._analysis_worker and self._analysis_worker.isRunning():
            self._analysis_worker.cancel()
            self._analysis_worker.wait(2000)

        logger.info(f"Starting analysis with {len(keypoints)} frames")
        self.status_label.setText("Probíhá analýza...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.analyze_button.setEnabled(False)
        self.feedback_widget.set_loading(True)

        # Start analysis worker
        self._analysis_worker = AnalysisWorker(keypoints, style="freestyle")
        self._analysis_worker.analysis_complete.connect(self._on_analysis_complete)
        self._analysis_worker.progress.connect(self._on_analysis_progress)
        self._analysis_worker.error.connect(self._on_analysis_error)
        self._analysis_worker.start()

    def _on_analyze_full_video(self):
        """Handle analyze full video action - processes entire video in background"""
        if self.current_video_path is None:
            QMessageBox.warning(
                self,
                "Žádné video",
                "Nejprve otevřete video soubor."
            )
            return

        # Cancel existing analysis
        if self._analysis_worker and self._analysis_worker.isRunning():
            self._analysis_worker.cancel()
            self._analysis_worker.wait(2000)

        logger.info(f"Starting full video analysis: {self.current_video_path}")
        self.status_label.setText("Zpracovávám celé video...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.analyze_button.setEnabled(False)
        self.analyze_full_button.setEnabled(False)
        self.feedback_widget.set_loading(True)

        # Import here to avoid circular imports
        from .full_video_worker import FullVideoAnalysisWorker

        # Start full video analysis worker
        self._analysis_worker = FullVideoAnalysisWorker(
            self.current_video_path,
            style="freestyle"
        )
        self._analysis_worker.analysis_complete.connect(self._on_analysis_complete)
        self._analysis_worker.progress.connect(self._on_analysis_progress)
        self._analysis_worker.status_update.connect(self._on_analysis_status_update)
        self._analysis_worker.error.connect(self._on_analysis_error)
        self._analysis_worker.start()

    def _on_stop_analysis(self):
        """Handle stop analysis action"""
        logger.info("Stopping analysis...")
        if self._analysis_worker and self._analysis_worker.isRunning():
            self._analysis_worker.cancel()
            self._analysis_worker.wait(2000)
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.analyze_full_button.setEnabled(True)
        self.status_label.setText("Analýza zastavena")

    def _on_analysis_complete(self, feedback: Feedback):
        """Handle analysis completion

        Args:
            feedback: Generated feedback from analysis
        """
        logger.info(f"Analysis complete: score={feedback.score:.1f}")
        self._current_feedback = feedback
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.analyze_full_button.setEnabled(True)
        self.export_button.setEnabled(True)
        self.export_json_action.setEnabled(True)
        self.export_pdf_action.setEnabled(True)
        self.status_label.setText(f"Analýza dokončena - Skóre: {feedback.score:.0f}/100")
        self.feedback_widget.update_feedback(feedback)

        # Update cycles timeline
        if feedback.cycles:
            self.cycles_timeline.update_cycles(feedback.cycles)

    def _on_analysis_progress(self, progress: int):
        """Handle analysis progress update

        Args:
            progress: Progress percentage (0-100)
        """
        self.progress_bar.setValue(progress)

    def _on_analysis_status_update(self, status: str):
        """Handle analysis status text update

        Args:
            status: Status message to display
        """
        self.status_label.setText(status)

    def _on_analysis_error(self, error_message: str):
        """Handle analysis error

        Args:
            error_message: Error description
        """
        logger.error(f"Analysis error: {error_message}")
        self.progress_bar.setVisible(False)
        self.analyze_button.setEnabled(True)
        self.analyze_full_button.setEnabled(True)
        self.status_label.setText("Chyba analýzy")
        self.feedback_widget.show_error(error_message)

    def _on_about(self):
        """Handle about action"""
        QMessageBox.about(
            self,
            "About SwimAth",
            "<h2>SwimAth v1.0.0</h2>"
            "<p>Swimming Style Analysis Application</p>"
            "<p>Analyze your swimming technique using computer vision and machine learning.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Real-time pose estimation (MediaPipe Pose)</li>"
            "<li>Style classification (99.67% accuracy)</li>"
            "<li>Personalized feedback in Czech</li>"
            "<li>Export to JSON/PDF</li>"
            "</ul>"
            "<p><b>Tech Stack:</b> Python, PySide6, OpenCV, MediaPipe, PyTorch</p>"
        )

    def _on_export_menu(self):
        """Show export options menu"""
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        menu.addAction(self.export_json_action)
        menu.addAction(self.export_pdf_action)
        menu.exec_(self.export_button.mapToGlobal(self.export_button.rect().bottomLeft()))

    def _on_export_json(self):
        """Export analysis results to JSON"""
        if self._current_feedback is None or self.current_video_path is None:
            QMessageBox.warning(self, "Export", "Nejprve spusťte analýzu.")
            return

        default_name = self.current_video_path.stem + "_analysis.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            str(self.current_video_path.parent / default_name),
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                export_to_json(
                    self._current_feedback,
                    str(self.current_video_path),
                    Path(file_path),
                    style="freestyle",
                    num_cycles=self._current_feedback.num_cycles,
                )
                self.status_label.setText(f"Exportováno: {Path(file_path).name}")
                logger.info(f"Exported to JSON: {file_path}")
            except Exception as e:
                logger.error(f"Export failed: {e}")
                QMessageBox.critical(self, "Chyba exportu", f"Export selhal:\n{e}")

    def _on_export_pdf(self):
        """Export analysis results to PDF"""
        if self._current_feedback is None or self.current_video_path is None:
            QMessageBox.warning(self, "Export", "Nejprve spusťte analýzu.")
            return

        default_name = self.current_video_path.stem + "_analysis.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF",
            str(self.current_video_path.parent / default_name),
            "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                export_to_pdf(
                    self._current_feedback,
                    str(self.current_video_path),
                    Path(file_path),
                    style="freestyle",
                    num_cycles=self._current_feedback.num_cycles,
                )
                self.status_label.setText(f"Exportováno: {Path(file_path).name}")
                logger.info(f"Exported to PDF: {file_path}")
            except Exception as e:
                logger.error(f"Export failed: {e}")
                QMessageBox.critical(self, "Chyba exportu", f"Export selhal:\n{e}")

    def closeEvent(self, event):
        """Handle window close event"""
        logger.info("Closing application...")
        if self._analysis_worker and self._analysis_worker.isRunning():
            self._analysis_worker.cancel()
            self._analysis_worker.wait(2000)
        self.video_player.cleanup()
        event.accept()
