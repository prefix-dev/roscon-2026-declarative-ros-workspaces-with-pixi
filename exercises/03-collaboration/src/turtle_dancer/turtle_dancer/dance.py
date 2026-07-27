"""Drive the turtlesim turtle in a circle.

The same node as in Exercise 1, now installed as a ROS entry point:

    ros2 run turtle_dancer dance
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Dancer(Node):
    def __init__(self) -> None:
        super().__init__("dancer")
        self.declare_parameter("linear_speed", 1.0)
        self.declare_parameter("angular_speed", 0.8)
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.step)
        self.get_logger().info("Dancing. Start `pixi run sim` to watch.")

    def step(self) -> None:
        twist = Twist()
        twist.linear.x = self.get_parameter("linear_speed").value
        twist.angular.z = self.get_parameter("angular_speed").value
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
