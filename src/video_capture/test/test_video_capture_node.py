"""비디오 캡처 노드 리소스 관리 테스트입니다."""

from unittest.mock import Mock

import cv2

from video_capture.video_capture_node import DEFAULT_FPS
from video_capture.video_capture_node import VideoCaptureNode


def make_node():
    node = object.__new__(VideoCaptureNode)
    node.frame_timer = None
    node.capture = None
    node.destroy_timer = Mock()
    node.get_logger = Mock()
    node._try_shutdown = Mock()
    return node


def test_destroy_frame_timer_destroys_timer_and_clears_reference():
    node = make_node()
    timer = Mock()
    node.frame_timer = timer

    node._destroy_frame_timer()

    node.destroy_timer.assert_called_once_with(timer)
    assert node.frame_timer is None


def test_release_capture_destroys_frame_timer_and_releases_capture():
    node = make_node()
    timer = Mock()
    capture = Mock()
    node.frame_timer = timer
    node.capture = capture

    node._release_capture()

    node.destroy_timer.assert_called_once_with(timer)
    capture.release.assert_called_once_with()
    assert node.frame_timer is None
    assert node.capture is None


def test_effective_fps_uses_requested_fps_when_positive():
    node = make_node()
    node.requested_fps = 12.0
    node.capture = Mock()

    assert node._effective_fps() == 12.0
    node.capture.get.assert_not_called()


def test_effective_fps_uses_source_fps_when_requested_fps_is_zero():
    node = make_node()
    node.requested_fps = 0.0
    node.capture = Mock()
    node.capture.get.return_value = 24.0

    assert node._effective_fps() == 24.0
    node.capture.get.assert_called_once_with(cv2.CAP_PROP_FPS)


def test_effective_fps_falls_back_when_source_fps_is_unavailable():
    node = make_node()
    node.requested_fps = 0.0
    node.capture = Mock()
    node.capture.get.return_value = 0.0

    assert node._effective_fps() == DEFAULT_FPS
    node.get_logger.return_value.warn.assert_called_once_with(
        'Video FPS is unavailable; using %.1f' % DEFAULT_FPS
    )


def test_read_looped_frame_rewinds_and_reads_first_frame():
    node = make_node()
    frame = object()
    node.loop = True
    node.capture = Mock()
    node.capture.read.return_value = (True, frame)

    assert node._read_looped_frame() is frame
    node.capture.set.assert_called_once_with(cv2.CAP_PROP_POS_FRAMES, 0)


def test_read_looped_frame_shuts_down_when_loop_is_disabled():
    node = make_node()
    node.loop = False

    assert node._read_looped_frame() is None
    node._try_shutdown.assert_called_once_with()
