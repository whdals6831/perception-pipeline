from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    input_topic = LaunchConfiguration("input_topic")
    preprocessed_topic = LaunchConfiguration("preprocessed_topic")
    roi_alarm_topic = LaunchConfiguration("roi_alarm_topic")
    roi_marker_topic = LaunchConfiguration("roi_marker_topic")
    enable_downsample = LaunchConfiguration("enable_downsample")
    enable_ground_removal = LaunchConfiguration("enable_ground_removal")
    enable_roi_alarm = LaunchConfiguration("enable_roi_alarm")
    voxel_leaf_size = LaunchConfiguration("voxel_leaf_size")
    max_window_size = LaunchConfiguration("max_window_size")
    slope = LaunchConfiguration("slope")
    initial_distance = LaunchConfiguration("initial_distance")
    max_distance = LaunchConfiguration("max_distance")
    roi_min_x = LaunchConfiguration("roi_min_x")
    roi_max_x = LaunchConfiguration("roi_max_x")
    roi_min_y = LaunchConfiguration("roi_min_y")
    roi_max_y = LaunchConfiguration("roi_max_y")
    roi_min_z = LaunchConfiguration("roi_min_z")
    roi_max_z = LaunchConfiguration("roi_max_z")
    roi_point_threshold = LaunchConfiguration("roi_point_threshold")

    return LaunchDescription(
        [
            DeclareLaunchArgument("input_topic", default_value="/points_raw"),
            DeclareLaunchArgument(
                "preprocessed_topic",
                default_value="/lidar/points_preprocessed",
            ),
            DeclareLaunchArgument("roi_alarm_topic", default_value="/lidar/roi_alarm"),
            DeclareLaunchArgument("roi_marker_topic", default_value="/lidar/roi_marker"),
            DeclareLaunchArgument("enable_downsample", default_value="false"),
            DeclareLaunchArgument("enable_ground_removal", default_value="false"),
            DeclareLaunchArgument("enable_roi_alarm", default_value="false"),
            DeclareLaunchArgument("voxel_leaf_size", default_value="0.1"),
            DeclareLaunchArgument("max_window_size", default_value="10"),
            DeclareLaunchArgument("slope", default_value="1.0"),
            DeclareLaunchArgument("initial_distance", default_value="0.5"),
            DeclareLaunchArgument("max_distance", default_value="50.0"),
            DeclareLaunchArgument("roi_min_x", default_value="-1.0"),
            DeclareLaunchArgument("roi_max_x", default_value="1.0"),
            DeclareLaunchArgument("roi_min_y", default_value="-1.0"),
            DeclareLaunchArgument("roi_max_y", default_value="1.0"),
            DeclareLaunchArgument("roi_min_z", default_value="-1.0"),
            DeclareLaunchArgument("roi_max_z", default_value="1.0"),
            DeclareLaunchArgument("roi_point_threshold", default_value="50"),
            Node(
                package="lidar_preprocessor",
                executable="lidar_preprocessor_node",
                name="lidar_preprocessor_node",
                parameters=[
                    {
                        "input_topic": input_topic,
                        "preprocessed_topic": preprocessed_topic,
                        "roi_alarm_topic": roi_alarm_topic,
                        "roi_marker_topic": roi_marker_topic,
                        "enable_downsample": ParameterValue(
                            enable_downsample,
                            value_type=bool,
                        ),
                        "enable_ground_removal": ParameterValue(
                            enable_ground_removal,
                            value_type=bool,
                        ),
                        "enable_roi_alarm": ParameterValue(
                            enable_roi_alarm,
                            value_type=bool,
                        ),
                        "voxel_leaf_size": ParameterValue(
                            voxel_leaf_size,
                            value_type=float,
                        ),
                        "max_window_size": ParameterValue(
                            max_window_size,
                            value_type=int,
                        ),
                        "slope": ParameterValue(
                            slope,
                            value_type=float,
                        ),
                        "initial_distance": ParameterValue(
                            initial_distance,
                            value_type=float,
                        ),
                        "max_distance": ParameterValue(
                            max_distance,
                            value_type=float,
                        ),
                        "roi_min_x": ParameterValue(
                            roi_min_x,
                            value_type=float,
                        ),
                        "roi_max_x": ParameterValue(
                            roi_max_x,
                            value_type=float,
                        ),
                        "roi_min_y": ParameterValue(
                            roi_min_y,
                            value_type=float,
                        ),
                        "roi_max_y": ParameterValue(
                            roi_max_y,
                            value_type=float,
                        ),
                        "roi_min_z": ParameterValue(
                            roi_min_z,
                            value_type=float,
                        ),
                        "roi_max_z": ParameterValue(
                            roi_max_z,
                            value_type=float,
                        ),
                        "roi_point_threshold": ParameterValue(
                            roi_point_threshold,
                            value_type=int,
                        ),
                    }
                ],
                output="screen",
            ),
        ]
    )
