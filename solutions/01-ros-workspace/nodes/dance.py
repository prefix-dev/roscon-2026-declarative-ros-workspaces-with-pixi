"""Drive the turtlesim turtle in a circle.

A plain script, run with `pixi run dance`. In Exercise 2 this becomes a real
ROS package that Pixi builds and installs.
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Dancer(Node):
    def __init__(self) -> None:
        super().__init__("dancer")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.step)
        self.get_logger().info("Dancing. Start `pixi run sim` to watch.")

    def step(self) -> None:
        twist = Twist()
        twist.linear.x = 1.0
        twist.angular.z = 0.8
        self.publisher.publish(twist)


def main() -> None:
    rclpy.init()
    node = Dancer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
