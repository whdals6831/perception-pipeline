"""비디오 캡처 파라미터 계약 테스트입니다."""

from video_capture.parameters import PARAMETER_SPECS
from video_capture.parameters import VideoParameters
from video_capture.parameters import validate_video_parameters


def test_parameter_specs_keep_runtime_defaults():
    specs = {spec.name: spec for spec in PARAMETER_SPECS}

    assert specs['video_path'].default == ''
    assert specs['image_topic'].default == '/video/image_raw'
    assert specs['frame_id'].default == 'video_frame'
    assert specs['fps'].default == 0.0
    assert specs['loop'].default is True
    assert specs['fps'].value_type is float
    assert specs['loop'].value_type is bool


def test_validate_video_parameters_corrects_negative_fps():
    warnings = []
    parameters = VideoParameters(
        video_path='/tmp/input.mp4',
        image_topic='/video/image_raw',
        frame_id='video_frame',
        fps=-1.0,
        loop=True,
    )

    validated = validate_video_parameters(parameters, warnings.append)

    assert validated.fps == 0.0
    assert warnings == ['fps must be zero or positive; using 0.0']
