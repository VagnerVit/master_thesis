"""SwimAth - Swimming Style Analysis Application
Entry point for the desktop application
"""

# Suppress third-party library warnings (must be before imports)
import os
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress TensorFlow INFO/WARNING/ERROR
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Suppress oneDNN messages
os.environ["GLOG_minloglevel"] = "3"  # Suppress glog (used by MediaPipe)
os.environ["ABSL_MIN_LOG_LEVEL"] = "3"  # Suppress absl warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
warnings.filterwarnings("ignore", message=".*SymbolDatabase.GetPrototype.*")

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from .ui.main_window import MainWindow
from .utils.logging_config import setup_logging, get_logger

# Setup logging (DEBUG for development)
import logging
log_dir = Path.home() / ".swimath" / "logs"
log_file = log_dir / "swimath.log"
setup_logging(level=logging.DEBUG, log_file=log_file, console=True)
logger = get_logger(__name__)


def main():
    """Main application entry point"""
    logger.info("Starting SwimAth application")

    # Create Qt application
    # Note: High DPI scaling is enabled by default in Qt6/PySide6
    app = QApplication(sys.argv)
    app.setApplicationName("SwimAth")
    app.setOrganizationName("SwimAth")
    app.setApplicationVersion("0.1.0")

    # Create main window
    window = MainWindow()
    window.show()

    logger.info("Application started successfully")

    # Run event loop
    exit_code = app.exec()

    logger.info(f"Application exited with code {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
