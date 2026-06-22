"""카메라 캡처 파라미터 계약 테스트입니다."""

from camera_capture.parameters import CameraParameters
from camera_capture.parameters import PARAMETER_SPECS
from camera_capture.parameters import validate_camera_parameters


def test_parameter_specs_keep_runtime_defaults():
    specs = {spec.name: spec for spec in PARAMETER_SPECS}

    assert specs['camera_index'].default == 0
    assert specs['image_topic'].default == '/camera/image_raw'
    assert specs['frame_id'].default == 'camera_frame'
    assert specs['width'].default == 640
    assert specs['height'].default == 480
    assert specs['fps'].default == 30.0
    assert specs['retry_interval_sec'].default == 2.0
    assert specs['camera_index'].value_type is int
    assert specs['fps'].value_type is float


def test_validate_camera_parameters_corrects_timing_values():
    warnings = []
    parameters = CameraParameters(
        camera_index=0,
        image_topic='/camera/image_raw',
        frame_id='camera_frame',
        width=640,
        height=480,
        fps=0.0,
        retry_interval_sec=-1.0,
    )

    validated = validate_camera_parameters(parameters, warnings.append)

    assert validated.fps == 30.0
    assert validated.retry_interval_sec == 2.0
    assert warnings == [
        'fps must be positive; using 30.0',
        'retry_interval_sec must be positive; using 2.0',
    ]
