"""이미지 캡처 파라미터 계약 테스트입니다."""

from image_capture.parameters import ImageParameters
from image_capture.parameters import PARAMETER_SPECS
from image_capture.parameters import validate_image_parameters


def test_parameter_specs_keep_runtime_defaults():
    specs = {spec.name: spec for spec in PARAMETER_SPECS}

    assert specs['image_path'].default == ''
    assert specs['image_topic'].default == '/image/image_raw'
    assert specs['frame_id'].default == 'image_frame'
    assert specs['fps'].default == 1.0
    assert specs['fps'].value_type is float


def test_validate_image_parameters_corrects_non_positive_fps():
    warnings = []
    parameters = ImageParameters(
        image_path='/tmp/input.jpg',
        image_topic='/image/image_raw',
        frame_id='image_frame',
        fps=0.0,
    )

    validated = validate_image_parameters(parameters, warnings.append)

    assert validated.fps == 1.0
    assert warnings == ['fps must be positive; using 1.0']
