"""YOLO 탐지 ROS 메시지 변환 테스트입니다."""

from std_msgs.msg import Header

from object_detector.yolo_detector import Detection
from object_detector.yolo_detector_node import build_detection_array


def test_build_detection_array_sets_bbox_and_hypothesis():
    header = Header()
    header.frame_id = 'camera_frame'
    detection = Detection(
        class_id=1,
        label='person',
        confidence=0.9,
        x_min=10.0,
        y_min=20.0,
        x_max=50.0,
        y_max=80.0,
    )

    message = build_detection_array(header, [detection])

    assert message.header.frame_id == 'camera_frame'
    assert len(message.detections) == 1
    detection_message = message.detections[0]
    assert detection_message.bbox.center.position.x == 30.0
    assert detection_message.bbox.center.position.y == 50.0
    assert detection_message.bbox.size_x == 40.0
    assert detection_message.bbox.size_y == 60.0
    assert detection_message.results[0].hypothesis.class_id == 'person'
    assert detection_message.results[0].hypothesis.score == 0.9
