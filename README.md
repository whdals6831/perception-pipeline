# Bridge-Pipeline

### Node 실행 방법
``` bash
# 카메라 & YOLO
ros2 launch camera_capture camera_capture.launch.py
ros2 launch object_detector yolo_detector.launch.py input_image_topic:=/camera/image_raw model_paths:=yolo11n.pt

# 라이다 & ROI
ros2 launch seyond start.py lidar_ip:=192.168.1.13
ros2 launch lidar_preprocessor lidar_preprocessor.launch.py input_topic:=/iv_points enable_roi_alarm:=true

# 모니터링 화면 알람
ros2 launch monitoring_fusion monitoring_fusion.launch.py
ros2 topic echo /monitoring/alarms
```

<br>

### Foxglove 실행 방법 
- UI : https://studio.foxglove.dev
``` bash
git clone https://github.com/foxglove/foxglove-sdk
cd foxglove-sdk/ros

make

source install/local_setup.bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765
```