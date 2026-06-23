"""비디오 파일 캡처 런타임 파라미터 계약입니다."""

from dataclasses import dataclass
from dataclasses import replace


@dataclass(frozen=True)
class ParameterSpec:
    """비디오 캡처 런타임이 노출하는 ROS 파라미터입니다."""

    name: str
    default: object
    value_type: type | None = None

    @property
    def launch_default(self):
        """런치 인자 기본값을 문자열로 반환합니다."""
        if isinstance(self.default, bool):
            return str(self.default).lower()
        return str(self.default)


@dataclass(frozen=True)
class VideoParameters:
    """검증된 비디오 캡처 파라미터입니다."""

    video_path: str
    image_topic: str
    frame_id: str
    fps: float
    loop: bool


PARAMETER_SPECS = (
    ParameterSpec('video_path', ''),
    ParameterSpec('image_topic', '/video/image_raw'),
    ParameterSpec('frame_id', 'video_frame'),
    ParameterSpec('fps', 0.0, float),
    ParameterSpec('loop', True, bool),
)


def declare_video_parameters(node):
    """ROS 노드에 비디오 캡처 파라미터를 선언합니다."""
    for spec in PARAMETER_SPECS:
        node.declare_parameter(spec.name, spec.default)


def read_video_parameters(node):
    """ROS 노드에서 비디오 캡처 파라미터를 읽고 검증합니다."""
    parameters = VideoParameters(
        video_path=_string_parameter(node, 'video_path'),
        image_topic=_string_parameter(node, 'image_topic'),
        frame_id=_string_parameter(node, 'frame_id'),
        fps=_double_parameter(node, 'fps'),
        loop=_bool_parameter(node, 'loop'),
    )
    return validate_video_parameters(parameters, node.get_logger().warn)


def validate_video_parameters(parameters, warn):
    """비디오 캡처 파라미터를 검증하고 보정된 값을 반환합니다."""
    if parameters.fps < 0.0:
        warn('fps must be zero or positive; using 0.0')
        parameters = replace(parameters, fps=0.0)
    return parameters


def _bool_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().bool_value


def _double_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().double_value


def _string_parameter(node, name):
    return node.get_parameter(name).get_parameter_value().string_value
