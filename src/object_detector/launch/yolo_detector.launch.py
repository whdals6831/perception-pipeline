"""YOLO 객체 탐지 노드를 실행합니다."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    """object_detector 실행 설명을 생성합니다."""
    input_image_topic = LaunchConfiguration('input_image_topic')
    detections_topic = LaunchConfiguration('detections_topic')
    annotated_image_topic = LaunchConfiguration('annotated_image_topic')
    model_path = LaunchConfiguration('model_path')
    confidence_threshold = LaunchConfiguration('confidence_threshold')
    iou_threshold = LaunchConfiguration('iou_threshold')
    image_size = LaunchConfiguration('image_size')
    device = LaunchConfiguration('device')
    publish_annotated_image = LaunchConfiguration('publish_annotated_image')

    return LaunchDescription([
        DeclareLaunchArgument(
            'input_image_topic',
            default_value='/camera/image_raw',
        ),
        DeclareLaunchArgument('detections_topic', default_value='/detections'),
        DeclareLaunchArgument(
            'annotated_image_topic',
            default_value='/detections/image',
        ),
        DeclareLaunchArgument('model_path', default_value='yolo11n.pt'),
        DeclareLaunchArgument('confidence_threshold', default_value='0.25'),
        DeclareLaunchArgument('iou_threshold', default_value='0.7'),
        DeclareLaunchArgument('image_size', default_value='640'),
        DeclareLaunchArgument('device', default_value=''),
        DeclareLaunchArgument(
            'publish_annotated_image',
            default_value='true',
        ),
        Node(
            package='object_detector',
            executable='yolo_detector_node',
            name='yolo_detector',
            output='screen',
            parameters=[{
                'input_image_topic': input_image_topic,
                'detections_topic': detections_topic,
                'annotated_image_topic': annotated_image_topic,
                'model_path': model_path,
                'confidence_threshold': ParameterValue(
                    confidence_threshold,
                    value_type=float,
                ),
                'iou_threshold': ParameterValue(
                    iou_threshold,
                    value_type=float,
                ),
                'image_size': ParameterValue(image_size, value_type=int),
                'device': device,
                'publish_annotated_image': ParameterValue(
                    publish_annotated_image,
                    value_type=bool,
                ),
            }],
        ),
    ])
