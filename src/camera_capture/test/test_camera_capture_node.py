from unittest.mock import Mock

from camera_capture.camera_capture_node import CameraCaptureNode


def make_node():
    node = object.__new__(CameraCaptureNode)
    node.frame_timer = None
    node.retry_timer = None
    node.capture = None
    node.destroy_timer = Mock()
    return node


def test_destroy_frame_timer_destroys_timer_and_clears_reference():
    node = make_node()
    timer = Mock()
    node.frame_timer = timer

    node._destroy_frame_timer()

    node.destroy_timer.assert_called_once_with(timer)
    assert node.frame_timer is None


def test_destroy_retry_timer_destroys_timer_and_clears_reference():
    node = make_node()
    timer = Mock()
    node.retry_timer = timer

    node._destroy_retry_timer()

    node.destroy_timer.assert_called_once_with(timer)
    assert node.retry_timer is None


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
