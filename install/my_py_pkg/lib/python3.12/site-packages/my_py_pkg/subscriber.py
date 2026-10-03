import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DroneSubscriber(Node):

    def __init__(self):
        super().__init__('drone_subscriber')

        self.subscription = self.create_subscription(
            String,
            '/drone/status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):

        self.get_logger().info(
            f'Received: {msg.data}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = DroneSubscriber()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()