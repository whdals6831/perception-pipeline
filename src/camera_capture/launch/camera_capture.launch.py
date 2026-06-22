"""카메라 캡처 노드를 실행합니다."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    """camera_capture 실행 설명을 생성합니다."""
    camera_index = LaunchConfiguration('camera_index')
    image_topic = LaunchConfiguration('image_topic')
    frame_id = LaunchConfiguration('frame_id')
    width = LaunchConfiguration('width')
    height = LaunchConfiguration('height')
    fps = LaunchConfiguration('fps')
    retry_interval_sec = LaunchConfiguration('retry_interval_sec')

    return LaunchDescription([
        DeclareLaunchArgument('camera_index', default_value='0'),
        DeclareLaunchArgument(
            'image_topic',
            default_value='/camera/image_raw',
        ),
        DeclareLaunchArgument('frame_id', default_value='camera_frame'),
        DeclareLaunchArgument('width', default_value='640'),
        DeclareLaunchArgument('height', default_value='480'),
        DeclareLaunchArgument('fps', default_value='30.0'),
        DeclareLaunchArgument('retry_interval_sec', default_value='2.0'),
        Node(
            package='camera_capture',
            executable='camera_capture_node',
            name='camera_capture',
            output='screen',
            parameters=[{
                'camera_index': ParameterValue(camera_index, value_type=int),
                'image_topic': image_topic,
                'frame_id': frame_id,
                'width': ParameterValue(width, value_type=int),
                'height': ParameterValue(height, value_type=int),
                'fps': ParameterValue(fps, value_type=float),
                'retry_interval_sec': ParameterValue(
                    retry_interval_sec,
                    value_type=float,
                ),
            }],
        ),
    ])
