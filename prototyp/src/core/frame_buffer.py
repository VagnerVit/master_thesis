"""Thread-safe frame buffer for video processing pipeline"""

import queue
import threading
from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Frame:
    """Frame data with metadata"""
    data: np.ndarray
    frame_number: int
    timestamp: float  # seconds
    processed: bool = False


class FrameBuffer:
    """Thread-safe FIFO buffer for video frames

    Manages frame queue between video decoder thread and pose estimation thread.
    Implements backpressure by blocking when buffer is full.
    """

    def __init__(self, maxsize: int = 30):
        """Initialize frame buffer

        Args:
            maxsize: Maximum number of frames in buffer (0 = unlimited)
        """
        self._queue: queue.Queue[Optional[Frame]] = queue.Queue(maxsize=maxsize)
        self._lock = threading.Lock()
        self._closed = False
        self._total_frames = 0
        self._dropped_frames = 0

    def put(self, frame: Frame, block: bool = True, timeout: Optional[float] = None) -> bool:
        """Add frame to buffer

        Args:
            frame: Frame to add
            block: If True, block until space available
            timeout: Maximum time to wait (None = forever)

        Returns:
            True if frame added, False if buffer is closed or timeout

        Raises:
            ValueError: If buffer is closed
        """
        with self._lock:
            if self._closed:
                raise ValueError("Cannot put to closed buffer")

        try:
            self._queue.put(frame, block=block, timeout=timeout)
            with self._lock:
                self._total_frames += 1
            return True
        except queue.Full:
            with self._lock:
                self._dropped_frames += 1
            return False

    def get(self, block: bool = True, timeout: Optional[float] = None) -> Optional[Frame]:
        """Get frame from buffer

        Args:
            block: If True, block until frame available
            timeout: Maximum time to wait (None = forever)

        Returns:
            Frame or None if buffer is closed and empty

        Raises:
            queue.Empty: If timeout expires
        """
        try:
            frame = self._queue.get(block=block, timeout=timeout)
            return frame
        except queue.Empty:
            return None

    def close(self) -> None:
        """Close buffer (no more frames can be added)"""
        with self._lock:
            self._closed = True
        # Put None sentinel to wake up consumers
        try:
            self._queue.put(None, block=False)
        except queue.Full:
            pass

    def is_closed(self) -> bool:
        """Check if buffer is closed"""
        with self._lock:
            return self._closed

    def qsize(self) -> int:
        """Get approximate number of frames in buffer"""
        return self._queue.qsize()

    def empty(self) -> bool:
        """Check if buffer is empty"""
        return self._queue.empty()

    def full(self) -> bool:
        """Check if buffer is full"""
        return self._queue.full()

    def get_stats(self) -> dict:
        """Get buffer statistics

        Returns:
            Dictionary with stats (total_frames, dropped_frames, current_size)
        """
        with self._lock:
            return {
                "total_frames": self._total_frames,
                "dropped_frames": self._dropped_frames,
                "current_size": self.qsize(),
                "drop_rate": (
                    self._dropped_frames / (self._total_frames + self._dropped_frames)
                    if (self._total_frames + self._dropped_frames) > 0
                    else 0.0
                ),
            }

    def clear(self) -> None:
        """Clear all frames from buffer"""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    def __len__(self) -> int:
        """Get number of frames in buffer"""
        return self.qsize()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
