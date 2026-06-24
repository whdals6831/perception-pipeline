#include <memory>
#include <string>

#include "pcl/filters/voxel_grid.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "pcl_conversions/pcl_conversions.h"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"

class LidarPreprocessorNode : public rclcpp::Node
{
public:
  LidarPreprocessorNode()
  : Node("lidar_preprocessor_node")
  {
    input_topic_ = declare_parameter<std::string>("input_topic", "/points_raw");
    const auto downsampled_topic =
      declare_parameter<std::string>("downsampled_topic", "/lidar/points_downsampled");
    const auto ground_removed_topic =
      declare_parameter<std::string>("ground_removed_topic", "/lidar/points_ground_removed");
    const auto preprocessed_topic =
      declare_parameter<std::string>("preprocessed_topic", "/lidar/points_preprocessed");
    voxel_leaf_size_ = declare_parameter<double>("voxel_leaf_size", 0.1);
    ground_min_z_ = declare_parameter<double>("ground_min_z", -0.2);
    ground_max_z_ = declare_parameter<double>("ground_max_z", 0.2);

    const auto qos = rclcpp::SensorDataQoS();
    downsampled_pub_ =
      create_publisher<sensor_msgs::msg::PointCloud2>(downsampled_topic, qos);
    ground_removed_pub_ =
      create_publisher<sensor_msgs::msg::PointCloud2>(ground_removed_topic, qos);
    preprocessed_pub_ =
      create_publisher<sensor_msgs::msg::PointCloud2>(preprocessed_topic, qos);
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

    const auto downsampled = downsample(input);
    const auto ground_removed = remove_ground(input);
    const auto preprocessed = remove_ground(downsampled);

    publish(*downsampled, msg->header, downsampled_pub_);
    publish(*ground_removed, msg->header, ground_removed_pub_);
    publish(*preprocessed, msg->header, preprocessed_pub_);
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
    filtered->points.reserve(cloud->points.size());

    for (const auto & point : cloud->points) {
      const bool is_ground = ground_min_z_ <= point.z && point.z <= ground_max_z_;
      if (!is_ground) {
        filtered->points.push_back(point);
      }
    }

    filtered->width = static_cast<std::uint32_t>(filtered->points.size());
    filtered->height = 1;
    filtered->is_dense = false;
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

  std::string input_topic_;
  double voxel_leaf_size_;
  double ground_min_z_;
  double ground_max_z_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr downsampled_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr ground_removed_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr preprocessed_pub_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LidarPreprocessorNode>());
  rclcpp::shutdown();
  return 0;
}
