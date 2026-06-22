"""카메라 캡처 런타임 파라미터 계약입니다."""

from dataclasses import dataclass
from dataclasses import replace


@dataclass(frozen=True)
class ParameterSpec:
    """카메라 캡처 런타임이 노출하는 ROS 파라미터입니다."""

    name: str
    default: object
    value_type: type | None = None

    @property
    def launch_default(self):
        """런치 인자 기본값을 문자열로 반환합니다."""
        return str(self.default)


@dataclass(frozen=True)
class CameraParameters:
    """검증된 카메라 캡처 파라미터입니다."""

    camera_index: int
    image_topic: str
    frame_id: str
    width: int
    height: int
    fps: float
    retry_interval_sec: float


PARAMETER_SPECS = (
    ParameterSpec('camera_index', 0, int),
    ParameterSpec('image_topic', '/camera/image_raw'),
    ParameterSpec('frame_id', 'camera_frame'),
    ParameterSpec('width', 640, int),
    ParameterSpec('height', 480, int),
    ParameterSpec('fps', 30.0, float),
    ParameterSpec('retry_interval_sec', 2.0, float),
)


def declare_camera_parameters(node):
    """ROS 노드에 카메라 캡처 파라미터를 선언합니다."""
    for spec in PARAMETER_SPECS:
        node.declare_parameter(spec.name, spec.default)


def read_camera_parameters(node):
    """ROS 노드에서 카메라 캡처 파라미터를 읽고 검증합니다."""
    parameters = CameraParameters(
        camera_index=_integer_parameter(node, 'camera_index'),
        image_topic=_string_parameter(node, 'image_topic'),
        frame_id=_string_parameter(node, 'frame_id'),
        width=_integer_parameter(node, 'width'),
        height=_integer_parameter(node, 'height'),
        fps=_double_parameter(node, 'fps'),
        retry_interval_sec=_double_parameter(node, 'retry_interval_sec'),
    )
    return validate_camera_parameters(parameters, node.get_logger().warn)


def validate_camera_parameters(parameters, warn):
    """카메라 캡처 파라미터를 검증하고 보정된 값을 반환합니다."""
    if parameters.fps <= 0.0:
        warn('fps must be positive; using 30.0')
        parameters = replace(parameters, fps=30.0)
    if parameters.retry_interval_sec <= 0.0:
        warn('retry_interval_sec must be positive; using 2.0')
        parameters = replace(parameters, retry_interval_sec=2.0)
    return parameters


def _integer_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().integer_value


def _double_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().double_value


def _string_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().string_value
