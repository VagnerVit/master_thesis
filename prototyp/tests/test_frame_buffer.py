"""Unit tests for frame_buffer module"""

import pytest
import numpy as np
import time
import threading
import queue

from src.core.frame_buffer import FrameBuffer, Frame


def test_frame_buffer_basic_operations():
    """Test basic put/get operations"""
    buffer = FrameBuffer(maxsize=5)

    frame1 = Frame(
        data=np.zeros((100, 100, 3), dtype=np.uint8),
        frame_number=1,
        timestamp=0.033
    )

    # Put frame
    assert buffer.put(frame1, block=False) is True
    assert buffer.qsize() == 1

    # Get frame
    retrieved_frame = buffer.get(block=False)
    assert retrieved_frame is not None
    assert retrieved_frame.frame_number == 1
    assert buffer.qsize() == 0


def test_frame_buffer_capacity():
    """Test buffer capacity and blocking"""
    buffer = FrameBuffer(maxsize=2)

    frame1 = Frame(np.zeros((10, 10, 3)), 1, 0.0)
    frame2 = Frame(np.zeros((10, 10, 3)), 2, 0.0)
    frame3 = Frame(np.zeros((10, 10, 3)), 3, 0.0)

    # Fill buffer
    assert buffer.put(frame1, block=False) is True
    assert buffer.put(frame2, block=False) is True

    # Buffer should be full
    assert buffer.full() is True

    # Non-blocking put should fail
    assert buffer.put(frame3, block=False, timeout=0.1) is False

    # Get one frame
    buffer.get(block=False)

    # Now should be able to add
    assert buffer.put(frame3, block=False) is True


def test_frame_buffer_closed():
    """Test buffer close behavior"""
    buffer = FrameBuffer(maxsize=5)

    frame = Frame(np.zeros((10, 10, 3)), 1, 0.0)
    buffer.put(frame, block=False)

    # Close buffer
    buffer.close()
    assert buffer.is_closed() is True

    # Should not be able to put after close
    with pytest.raises(ValueError):
        buffer.put(frame, block=False)

    # Should still be able to get existing frames
    retrieved = buffer.get(block=False)
    assert retrieved is not None


def test_frame_buffer_stats():
    """Test statistics tracking"""
    buffer = FrameBuffer(maxsize=2)

    frame1 = Frame(np.zeros((10, 10, 3)), 1, 0.0)
    frame2 = Frame(np.zeros((10, 10, 3)), 2, 0.0)
    frame3 = Frame(np.zeros((10, 10, 3)), 3, 0.0)

    buffer.put(frame1, block=False)
    buffer.put(frame2, block=False)
    buffer.put(frame3, block=False)  # Should be dropped (buffer full)

    stats = buffer.get_stats()

    assert stats["total_frames"] == 2  # Only successfully added frames
    assert stats["dropped_frames"] == 1
    assert stats["drop_rate"] == pytest.approx(1/3)  # 1 dropped out of 3 attempts


def test_frame_buffer_thread_safety():
    """Test thread-safe operations"""
    buffer = FrameBuffer(maxsize=10)
    results = []

    def producer():
        for i in range(5):
            frame = Frame(np.zeros((10, 10, 3)), i, float(i))
            buffer.put(frame, block=True)
            time.sleep(0.01)
        buffer.close()

    def consumer():
        while True:
            try:
                frame = buffer.get(block=True, timeout=1.0)
                if frame is None:
                    break
                results.append(frame.frame_number)
            except queue.Empty:
                break

    # Start threads
    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    # Should have received all frames
    assert len(results) == 5
    assert results == list(range(5))


def test_frame_buffer_context_manager():
    """Test context manager protocol"""
    with FrameBuffer(maxsize=5) as buffer:
        frame = Frame(np.zeros((10, 10, 3)), 1, 0.0)
        buffer.put(frame, block=False)
        assert buffer.qsize() == 1

    # After exit, buffer should be closed
    assert buffer.is_closed() is True


def test_frame_buffer_clear():
    """Test clearing buffer"""
    buffer = FrameBuffer(maxsize=5)

    for i in range(3):
        frame = Frame(np.zeros((10, 10, 3)), i, float(i))
        buffer.put(frame, block=False)

    assert buffer.qsize() == 3

    buffer.clear()

    assert buffer.qsize() == 0
    assert buffer.empty() is True
