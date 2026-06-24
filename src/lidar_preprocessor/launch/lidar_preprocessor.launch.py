from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    input_topic = LaunchConfiguration("input_topic")
    downsampled_topic = LaunchConfiguration("downsampled_topic")
    ground_removed_topic = LaunchConfiguration("ground_removed_topic")
    preprocessed_topic = LaunchConfiguration("preprocessed_topic")
    voxel_leaf_size = LaunchConfiguration("voxel_leaf_size")
    ground_min_z = LaunchConfiguration("ground_min_z")
    ground_max_z = LaunchConfiguration("ground_max_z")

    return LaunchDescription(
        [
            DeclareLaunchArgument("input_topic", default_value="/points_raw"),
            DeclareLaunchArgument(
                "downsampled_topic",
                default_value="/lidar/points_downsampled",
            ),
            DeclareLaunchArgument(
                "ground_removed_topic",
                default_value="/lidar/points_ground_removed",
            ),
            DeclareLaunchArgument(
                "preprocessed_topic",
                default_value="/lidar/points_preprocessed",
            ),
            DeclareLaunchArgument("voxel_leaf_size", default_value="0.1"),
            DeclareLaunchArgument("ground_min_z", default_value="-0.2"),
            DeclareLaunchArgument("ground_max_z", default_value="0.2"),
            Node(
                package="lidar_preprocessor",
                executable="lidar_preprocessor_node",
                name="lidar_preprocessor_node",
                parameters=[
                    {
                        "input_topic": input_topic,
                        "downsampled_topic": downsampled_topic,
                        "ground_removed_topic": ground_removed_topic,
                        "preprocessed_topic": preprocessed_topic,
                        "voxel_leaf_size": ParameterValue(
                            voxel_leaf_size,
                            value_type=float,
                        ),
                        "ground_min_z": ParameterValue(
                            ground_min_z,
                            value_type=float,
                        ),
                        "ground_max_z": ParameterValue(
                            ground_max_z,
                            value_type=float,
                        ),
                    }
                ],
                output="screen",
            ),
        ]
    )
