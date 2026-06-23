# AGENTS.md

## Module Context

`video_capture`는 로컬 비디오 파일에서 프레임을 읽어 `sensor_msgs/Image`로 발행하는 `ament_python` ROS 2 패키지다. 카메라 하드웨어 없이 `object_detector`에 테스트/데모 입력을 공급하는 역할을 담당한다.

## Tech Stack & Constraints

- 런타임 의존성: `rclpy`, `sensor_msgs`, `cv_bridge`, `python3-opencv`, `launch`, `launch_ros`.
- 비디오 이미지 발행에는 측정된 변경 사유가 없다면 `qos_profile_sensor_data`를 사용한다.
- 비디오 입력 설정은 ROS 파라미터와 런치 인자로 유지한다.
- 기본 이미지 토픽은 `/video/image_raw`로 유지한다. `object_detector` 연결은 `input_image_topic` 파라미터로 명시한다.
- 로컬 비디오 파일 경로나 샘플 영상 파일을 저장소에 하드코딩하거나 커밋하지 않는다.

## Implementation Patterns

- 노드 엔트리 포인트: `video_capture.video_capture_node:main`.
- 런치 파일 이름 패턴: `launch/*.launch.py`.
- 런치 파일은 `setup.py`의 `data_files`로 설치한다. 콘솔 엔트리 포인트는 `setup.cfg`를 통해 `lib/video_capture` 아래에 설치되어야 한다.
- 파라미터 기본값은 `video_capture/parameters.py`의 `PARAMETER_SPECS`와 런치 인자가 같은 값을 공유하게 유지한다.
- OpenCV 프레임은 `CvBridge().cv2_to_imgmsg(frame, encoding='bgr8')`로 변환하고 timestamp와 `frame_id`를 모두 설정한다.
- `fps=0.0`은 비디오 파일 FPS 사용을 의미한다. 비디오 FPS를 읽지 못하면 명시된 fallback 값을 사용한다.

## Testing Strategy

- 패키지 테스트 명령: `colcon test --packages-select video_capture --event-handlers console_direct+`
- 결과 확인: `colcon test-result --verbose`
- 전체 `rclpy` 초기화가 필요 없으면 mock으로 ROS 리소스 관리 로직을 격리해 테스트한다.
- EOF 반복 재생, FPS 선택, 타이머 정리, 캡처 해제 경로가 바뀌면 해당 동작 테스트를 추가한다.
- 기본 테스트가 실제 비디오 파일, 카메라 장치, GUI, 네트워크를 요구하지 않게 한다.

## Local Golden Rules

- `video_path`가 비어 있거나 열 수 없으면 에러 로그 후 종료하는 계약을 유지한다.
- 기본 EOF 동작은 반복 재생이다. `loop` 계약을 바꾸면 파라미터 테스트와 노드 테스트를 함께 갱신한다.
- 노드를 파괴하거나 오류로 종료하기 전에 `cv2.VideoCapture`를 해제한다.
- 기존 프레임 타이머는 교체나 종료 전에 destroy하고 객체 참조를 비운다.
- 유효한 ROS timestamp와 frame ID 없이 프레임을 발행하지 않는다.
