"""로컬에 연결된 카메라 프레임을 ROS 이미지로 발행합니다."""

import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class CameraCaptureNode(Node):
    """OpenCV VideoCapture에서 프레임을 가져와 발행합니다."""

    def __init__(self):
        super().__init__('camera_capture')

        self.declare_parameter('camera_index', 0)
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('frame_id', 'camera_frame')
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('fps', 30.0)
        self.declare_parameter('retry_interval_sec', 2.0)

        self.camera_index = (
            self.get_parameter('camera_index').get_parameter_value()
            .integer_value
        )
        self.image_topic = (
            self.get_parameter('image_topic').get_parameter_value()
            .string_value
        )
        self.frame_id = (
            self.get_parameter('frame_id').get_parameter_value()
            .string_value
        )
        self.width = (
            self.get_parameter('width').get_parameter_value().integer_value
        )
        self.height = (
            self.get_parameter('height').get_parameter_value()
            .integer_value
        )
        self.fps = (
            self.get_parameter('fps').get_parameter_value().double_value
        )
        self.retry_interval_sec = (
            self.get_parameter('retry_interval_sec').get_parameter_value()
            .double_value
        )

        if self.fps <= 0.0:
            self.get_logger().warn('fps must be positive; using 30.0')
            self.fps = 30.0
        if self.retry_interval_sec <= 0.0:
            self.get_logger().warn(
                'retry_interval_sec must be positive; using 2.0'
            )
            self.retry_interval_sec = 2.0

        self.bridge = CvBridge()
        self.capture = None
        self.warned_read_failure = False
        self.frame_timer = None
        self.retry_timer = None
        self.publisher = self.create_publisher(
            Image,
            self.image_topic,
            qos_profile_sensor_data,
        )

        self.get_logger().info(
            'Publishing camera %d to %s at %dx%d %.1f fps'
            % (
                self.camera_index,
                self.image_topic,
                self.width,
                self.height,
                self.fps,
            )
        )
        self._open_capture()

    def destroy_node(self):
        """노드를 종료하기 전에 카메라를 해제합니다."""
        self._release_capture()
        super().destroy_node()

    def _open_capture(self):
        self._destroy_retry_timer()

        self._release_capture()
        self.capture = cv2.VideoCapture(self.camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.width))
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.height))
        self.capture.set(cv2.CAP_PROP_FPS, float(self.fps))

        if not self.capture.isOpened():
            self.get_logger().error(
                'Failed to open camera index %d; retrying in %.1f seconds'
                % (self.camera_index, self.retry_interval_sec)
            )
            self._release_capture()
            self._schedule_retry()
            return

        self.warned_read_failure = False
        period_sec = 1.0 / self.fps
        self.frame_timer = self.create_timer(period_sec, self._publish_frame)
        self.get_logger().info('Camera opened')

    def _publish_frame(self):
        if self.capture is None or not self.capture.isOpened():
            self._handle_read_failure('Camera is not open')
            return

        success, frame = self.capture.read()
        if not success or frame is None:
            self._handle_read_failure('Failed to read frame from camera')
            return

        self.warned_read_failure = False
        message = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        message.header.stamp = self.get_clock().now().to_msg()
        message.header.frame_id = self.frame_id
        self.publisher.publish(message)

    def _handle_read_failure(self, message):
        if not self.warned_read_failure:
            self.get_logger().warn(
                '%s; retrying in %.1f seconds'
                % (message, self.retry_interval_sec)
            )
            self.warned_read_failure = True

        self._release_capture()
        self._schedule_retry()

    def _schedule_retry(self):
        if self.retry_timer is None:
            self.retry_timer = self.create_timer(
                self.retry_interval_sec,
                self._open_capture,
            )

    def _release_capture(self):
        self._destroy_frame_timer()
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def _destroy_frame_timer(self):
        if self.frame_timer is not None:
            self.destroy_timer(self.frame_timer)
            self.frame_timer = None

    def _destroy_retry_timer(self):
        if self.retry_timer is not None:
            self.destroy_timer(self.retry_timer)
            self.retry_timer = None


def main(args=None):
    """카메라 캡처 노드를 시작합니다."""
    rclpy.init(args=args)
    node = CameraCaptureNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
