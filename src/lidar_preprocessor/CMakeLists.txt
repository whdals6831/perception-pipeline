cmake_minimum_required(VERSION 3.10)
if(POLICY CMP0148)
  cmake_policy(SET CMP0148 OLD)
endif()

project(lidar_preprocessor)

if(APPLE AND EXISTS "/usr/bin/install_name_tool")
  set(CMAKE_INSTALL_NAME_TOOL "/usr/bin/install_name_tool" CACHE FILEPATH "" FORCE)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(PCL REQUIRED COMPONENTS filters segmentation)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(pcl_conversions REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

set(Python_EXECUTABLE ${Python3_EXECUTABLE})
set(Python_INCLUDE_DIRS ${Python3_INCLUDE_DIRS})
set(Python_LIBRARIES ${Python3_LIBRARIES})
set(Python_NumPy_INCLUDE_DIRS ${Python3_NumPy_INCLUDE_DIRS})

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RoiAlarm.msg"
  "msg/RoiAlarmArray.msg"
  DEPENDENCIES std_msgs
)

add_executable(lidar_preprocessor_node src/lidar_preprocessor_node.cpp)
target_include_directories(lidar_preprocessor_node SYSTEM PRIVATE ${PCL_INCLUDE_DIRS})
ament_target_dependencies(
  lidar_preprocessor_node
  pcl_conversions
  rclcpp
  sensor_msgs
  std_msgs
  visualization_msgs
)
target_link_libraries(lidar_preprocessor_node ${PCL_LIBRARIES})
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(lidar_preprocessor_node "${cpp_typesupport_target}")

install(TARGETS
  lidar_preprocessor_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  config
  launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
