"""YOLO 탐지 변환 유틸리티 테스트입니다."""

from object_detector.yolo_detector import detections_from_ultralytics_result


class Boxes:
    """테스트용 Ultralytics boxes 대역입니다."""

    xyxy = [[10.0, 20.0, 50.0, 80.0]]
    conf = [0.75]
    cls = [1.0]


class Result:
    """테스트용 Ultralytics result 대역입니다."""

    boxes = Boxes()
    names = {1: 'person'}


def test_detections_from_ultralytics_result():
    detections = detections_from_ultralytics_result(Result())

    assert len(detections) == 1
    detection = detections[0]
    assert detection.class_id == 1
    assert detection.label == 'person'
    assert detection.confidence == 0.75
    assert detection.center_x == 30.0
    assert detection.center_y == 50.0
    assert detection.width == 40.0
    assert detection.height == 60.0
