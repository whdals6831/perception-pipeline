# AGENTS.md

## Module Context

`monitoring_fusion`은 `lidar_preprocessor`의 `RoiAlarmArray`와 `object_detector`의 `Detection2DArray`를 결합해 웹 표시용 JSON 알람을 `std_msgs/String`으로 발행하는 `ament_python` ROS 2 패키지다. 이 패키지는 센서 처리 자체가 아니라 시간 신선도, 위험 ROI, 탐지 label 조건을 조합하는 최종 판단 계층이다.

## Tech Stack & Constraints

- 런타임 의존성: `rclpy`, `lidar_preprocessor`, `std_msgs`, `vision_msgs`, `launch`, `launch_ros`.
- 입력 기본 토픽은 `/lidar/roi_alarm`과 `/detections`, 출력 기본 토픽은 `/monitoring/alarms`다.
- ROI 알람 구독은 `qos_profile_sensor_data`를 사용하고, detection 구독과 JSON 알람 발행은 기존 depth `10` 계약을 유지한다.
- `required_detection_labels`는 콤마 구분 문자열로 받고 비교 시 소문자로 정규화한다.
- 출력은 `json.dumps(..., ensure_ascii=False, separators=(',', ':'))` 형식의 compact JSON 문자열이다.

## Implementation Patterns

- 노드 엔트리 포인트: `monitoring_fusion.fusion_node:main`.
- 런치 파일 이름 패턴: `launch/*.launch.py`.
- 런치 파일은 `setup.py`의 `data_files`로 설치한다. 콘솔 엔트리 포인트는 `setup.cfg`를 통해 `lib/monitoring_fusion` 아래에 설치되어야 한다.
- 파라미터 기본값은 `monitoring_fusion/parameters.py`의 `PARAMETER_SPECS`와 런치 인자가 같은 값을 공유하게 유지한다.
- 순수 판단 로직은 `monitoring_alarm.py`에 두고, ROS 구독/발행과 메시지 보관은 `fusion_node.py`에 둔다.
- `danger_zone` ROI에 활성 알람이 있고 신선한 필수 label 탐지가 있으면 `red`, 활성 ROI만 있으면 `yellow`, 활성 ROI가 없으면 `green`으로 유지한다.
- ROI와 detection timestamp 차이가 `max_age_seconds`를 초과하면 `status`는 `stale`이고 detection match는 비운다.
- `vision_msgs` 버전별 `BoundingBox2D.center` 구조 차이를 고려한 center 값 추출 호환 로직을 유지한다.

## Testing Strategy

- 패키지 테스트 명령: `colcon test --packages-select monitoring_fusion --event-handlers console_direct+`
- 결과 확인: `colcon test-result --verbose`
- 판단 로직은 ROS 초기화 없이 `SimpleNamespace` fixture로 테스트한다.
- 파라미터 기본값, label 정규화, stale 판정, red/yellow/green level, JSON 인코딩 계약이 바뀌면 테스트를 함께 갱신한다.
- 기본 테스트가 실제 라이다, 카메라, YOLO 모델, 네트워크, GUI를 요구하지 않게 한다.

## Local Golden Rules

- 라이다 ROI 생성이나 YOLO 추론을 이 패키지에 섞지 않는다.
- `lidar_preprocessor.msg.RoiAlarmArray`와 `vision_msgs/Detection2DArray` 계약 변경 시 이 패키지의 변환/테스트를 같이 확인한다.
- `danger_zone`, `required_detection_labels`, `max_age_seconds` 의미를 바꾸면 운영 판단 기준 변경으로 취급하고 테스트 이름까지 명확히 갱신한다.
- 모니터링 이벤트 JSON에 필드를 추가할 수는 있지만 기존 `alarm`, `level`, `status`, `age_seconds`, `active_rois`, `matched_detections` 필드는 의도 없이 제거하지 않는다.
- timestamp가 없는 대체 이벤트나 wall-clock 추정 로직은 실제 소비자 요구가 생길 때만 추가한다.
