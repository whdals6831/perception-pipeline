#include <memory>
#include <string>

#include "pcl/filters/extract_indices.h"
#include "pcl/filters/voxel_grid.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "pcl/segmentation/progressive_morphological_filter.h"
#include "pcl_conversions/pcl_conversions.h"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "std_msgs/msg/bool.hpp"
#include "visualization_msgs/msg/marker.hpp"

class LidarPreprocessorNode : public rclcpp::Node
{
public:
  LidarPreprocessorNode()
  : Node("lidar_preprocessor_node")
  {
    input_topic_ = declare_parameter<std::string>("input_topic", "/points_raw");
    const auto preprocessed_topic =
      declare_parameter<std::string>("preprocessed_topic", "/lidar/points_preprocessed");
    const auto roi_alarm_topic =
      declare_parameter<std::string>("roi_alarm_topic", "/lidar/roi_alarm");
    const auto roi_marker_topic =
      declare_parameter<std::string>("roi_marker_topic", "/lidar/roi_marker");
    enable_downsample_ = declare_parameter<bool>("enable_downsample", false);
    enable_ground_removal_ = declare_parameter<bool>("enable_ground_removal", false);
    enable_roi_alarm_ = declare_parameter<bool>("enable_roi_alarm", false);
    voxel_leaf_size_ = declare_parameter<double>("voxel_leaf_size", 0.1);
    max_window_size_ = declare_parameter<int>("max_window_size", 10);
    slope_ = declare_parameter<double>("slope", 1.0);
    initial_distance_ = declare_parameter<double>("initial_distance", 0.5);
    max_distance_ = declare_parameter<double>("max_distance", 50.0);
    roi_min_x_ = declare_parameter<double>("roi_min_x", -1.0);
    roi_max_x_ = declare_parameter<double>("roi_max_x", 1.0);
    roi_min_y_ = declare_parameter<double>("roi_min_y", -1.0);
    roi_max_y_ = declare_parameter<double>("roi_max_y", 1.0);
    roi_min_z_ = declare_parameter<double>("roi_min_z", -1.0);
    roi_max_z_ = declare_parameter<double>("roi_max_z", 1.0);
    roi_point_threshold_ = declare_parameter<int>("roi_point_threshold", 50);

    const auto qos = rclcpp::SensorDataQoS();
    preprocessed_pub_ =
      create_publisher<sensor_msgs::msg::PointCloud2>(preprocessed_topic, qos);
    roi_alarm_pub_ = create_publisher<std_msgs::msg::Bool>(roi_alarm_topic, qos);
    roi_marker_pub_ = create_publisher<visualization_msgs::msg::Marker>(roi_marker_topic, qos);
    subscription_ = create_subscription<sensor_msgs::msg::PointCloud2>(
      input_topic_, qos,
      [this](sensor_msgs::msg::PointCloud2::ConstSharedPtr msg) {
        process(msg);
      });
  }

private:
  using PointCloud = pcl::PointCloud<pcl::PointXYZ>;

  void process(const sensor_msgs::msg::PointCloud2::ConstSharedPtr msg)
  {
    auto input = std::make_shared<PointCloud>();
    pcl::fromROSMsg(*msg, *input);

    auto preprocessed = enable_downsample_ ? downsample(input) : input;
    if (enable_ground_removal_) {
      preprocessed = remove_ground(preprocessed);
    }
    publish(*preprocessed, msg->header, preprocessed_pub_);
    publish_roi_alarm(*preprocessed, msg->header);
  }

  PointCloud::Ptr downsample(const PointCloud::ConstPtr cloud) const
  {
    auto filtered = std::make_shared<PointCloud>();
    if (voxel_leaf_size_ <= 0.0) {
      *filtered = *cloud;
      return filtered;
    }

    pcl::VoxelGrid<pcl::PointXYZ> voxel_grid;
    voxel_grid.setInputCloud(cloud);
    voxel_grid.setLeafSize(voxel_leaf_size_, voxel_leaf_size_, voxel_leaf_size_);
    voxel_grid.filter(*filtered);
    return filtered;
  }

  PointCloud::Ptr remove_ground(const PointCloud::ConstPtr cloud) const
  {
    auto filtered = std::make_shared<PointCloud>();

    pcl::PointIndices::Ptr ground_indices(new pcl::PointIndices);
    pcl::ProgressiveMorphologicalFilter<pcl::PointXYZ> ground_filter;
    ground_filter.setInputCloud(cloud);
    ground_filter.setMaxWindowSize(max_window_size_);
    ground_filter.setSlope(static_cast<float>(slope_));
    ground_filter.setInitialDistance(static_cast<float>(initial_distance_));
    ground_filter.setMaxDistance(static_cast<float>(max_distance_));
    ground_filter.extract(ground_indices->indices);

    if (ground_indices->indices.empty()) {
      *filtered = *cloud;
      return filtered;
    }

    pcl::ExtractIndices<pcl::PointXYZ> extract;
    extract.setInputCloud(cloud);
    extract.setIndices(ground_indices);
    extract.setNegative(true);
    extract.filter(*filtered);
    return filtered;
  }

  void publish(
    const PointCloud & cloud,
    const std_msgs::msg::Header & header,
    const rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr & publisher) const
  {
    sensor_msgs::msg::PointCloud2 output;
    pcl::toROSMsg(cloud, output);
    output.header = header;
    publisher->publish(output);
  }

  void publish_roi_alarm(const PointCloud & cloud, const std_msgs::msg::Header & header) const
  {
    if (!enable_roi_alarm_) {
      return;
    }

    int count = 0;
    for (const auto & point : cloud.points) {
      if (
        point.x >= roi_min_x_ && point.x <= roi_max_x_ &&
        point.y >= roi_min_y_ && point.y <= roi_max_y_ &&
        point.z >= roi_min_z_ && point.z <= roi_max_z_)
      {
        ++count;
      }
    }

    std_msgs::msg::Bool alarm;
    alarm.data = count >= roi_point_threshold_;
    roi_alarm_pub_->publish(alarm);
    publish_roi_marker(header, alarm.data);
  }

  void publish_roi_marker(const std_msgs::msg::Header & header, const bool alarm) const
  {
    visualization_msgs::msg::Marker marker;
    marker.header = header;
    marker.ns = "lidar_roi";
    marker.id = 0;
    marker.type = visualization_msgs::msg::Marker::CUBE;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = (roi_min_x_ + roi_max_x_) / 2.0;
    marker.pose.position.y = (roi_min_y_ + roi_max_y_) / 2.0;
    marker.pose.position.z = (roi_min_z_ + roi_max_z_) / 2.0;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = roi_max_x_ - roi_min_x_;
    marker.scale.y = roi_max_y_ - roi_min_y_;
    marker.scale.z = roi_max_z_ - roi_min_z_;
    marker.color.r = alarm ? 1.0F : 0.0F;
    marker.color.g = alarm ? 0.0F : 1.0F;
    marker.color.b = 0.0F;
    marker.color.a = 0.25F;
    roi_marker_pub_->publish(marker);
  }

  std::string input_topic_;
  bool enable_downsample_;
  bool enable_ground_removal_;
  bool enable_roi_alarm_;
  double voxel_leaf_size_;
  int max_window_size_;
  double slope_;
  double initial_distance_;
  double max_distance_;
  double roi_min_x_;
  double roi_max_x_;
  double roi_min_y_;
  double roi_max_y_;
  double roi_min_z_;
  double roi_max_z_;
  int roi_point_threshold_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr preprocessed_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr roi_alarm_pub_;
  rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr roi_marker_pub_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LidarPreprocessorNode>());
  rclcpp::shutdown();
  return 0;
}
