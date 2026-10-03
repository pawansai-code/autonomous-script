import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DronePublisher(Node):

    def __init__(self):
        super().__init__('drone_publisher')

        self.publisher = self.create_publisher(
            String,
            '/drone/status',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

    def publish_status(self):

        msg = String()

        msg.data = 'hey pawan, im tej...'

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published: {msg.data}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = DronePublisher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()