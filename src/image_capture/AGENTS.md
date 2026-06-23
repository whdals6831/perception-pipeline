# AGENTS.md

## Module Context

`image_capture`는 로컬 정적 이미지 파일 하나를 읽어 같은 프레임을 `sensor_msgs/Image`로 반복 발행하는 `ament_python` ROS 2 패키지다. 카메라나 비디오 입력 없이 `object_detector`의 테스트/수동 입력 토픽으로 사용할 수 있는 이미지 소스를 제공한다.

## Tech Stack & Constraints

- 런타임 의존성: `rclpy`, `sensor_msgs`, `cv_bridge`, `python3-opencv`, `launch`, `launch_ros`.
- 이미지 발행에는 `qos_profile_sensor_data`를 사용한다.
- 입력 파일 경로는 ROS 파라미터 `image_path`와 런치 인자로만 받는다.
- 기본 발행 토픽은 `/image/image_raw`, 기본 frame ID는 `image_frame`, 기본 발행 속도는 `1.0 fps`다.
- 유효하지 않은 `image_path`나 읽을 수 없는 이미지는 에러 로그 후 실패 종료한다.

## Implementation Patterns

- 노드 엔트리 포인트: `image_capture.image_capture_node:main`.
- 런치 파일 이름 패턴: `launch/*.launch.py`.
- 런치 파일은 `setup.py`의 `data_files`로 설치한다. 콘솔 엔트리 포인트는 `setup.cfg`를 통해 `lib/image_capture` 아래에 설치되어야 한다.
- OpenCV 이미지는 `cv2.imread(image_path, cv2.IMREAD_COLOR)`로 읽고, `CvBridge().cv2_to_imgmsg(frame, encoding='bgr8')`로 변환한다.
- 발행 메시지에는 매 발행 시점의 timestamp와 `frame_id`를 설정한다.
- 런치 인자 기본값과 노드 파라미터 기본값은 `parameters.py`의 `PARAMETER_SPECS`를 단일 출처로 사용한다.

## Testing Strategy

- 패키지 테스트 명령: `colcon test --packages-select image_capture --event-handlers console_direct+`
- 결과 확인: `colcon test-result --verbose`
- 실제 파일 시스템 이미지나 ROS 초기화가 필요 없으면 mock으로 `cv2.imread`, bridge, clock, publisher, timer 정리 로직을 격리해 테스트한다.
- 파라미터 기본값, `fps` 검증, 이미지 읽기 실패, timestamp/frame ID 설정, 타이머 정리 동작을 유지한다.

## Local Golden Rules

- 여러 이미지 순회, 디렉토리 입력, 비디오 루프 기능을 이 패키지에 섞지 않는다. 그런 입력은 별도 요구사항으로 다룬다.
- `object_detector`의 기본 입력 토픽을 이 패키지 때문에 변경하지 않는다. 연결은 `input_image_topic:=/image/image_raw`로 명시한다.
- 이미지 파일 경로나 로컬 절대 경로를 기본값으로 하드코딩하지 않는다.
- 유효한 ROS timestamp와 frame ID 없이 이미지를 발행하지 않는다.
- 발행 주기나 토픽 기본값을 바꾸면 런치 기본값, 테스트, 루트 `AGENTS.md` 실행 예시를 함께 확인한다.
