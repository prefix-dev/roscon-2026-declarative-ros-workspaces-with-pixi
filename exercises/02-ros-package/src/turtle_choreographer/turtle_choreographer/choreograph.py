"""Drive the turtlesim turtle in a figure of eight.

The Python half of a mixed-language workspace. Both this and the C++
`turtle_dancer` are built and installed by Pixi from their `package.xml`:

    ros2 run turtle_choreographer choreograph
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Choreographer(Node):
    def __init__(self) -> None:
        super().__init__("choreographer")
        self.declare_parameter("linear_speed", 1.5)
        self.declare_parameter("angular_speed", 1.2)
        self.declare_parameter("lobe_seconds", 4.0)

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.step)
        self.elapsed = 0.0
        self.direction = 1.0
        self.get_logger().info("Choreographing. Start `pixi run sim` to watch.")

    def step(self) -> None:
        lobe = self.get_parameter("lobe_seconds").value
        self.elapsed += 0.1
        if self.elapsed >= lobe:
            self.elapsed = 0.0
            self.direction *= -1.0

        twist = Twist()
        twist.linear.x = self.get_parameter("linear_speed").value
        twist.angular.z = self.get_parameter("angular_speed").value * self.direction
        self.publisher.publish(twist)


def main() -> None:
    rclpy.init()
    node = Choreographer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
