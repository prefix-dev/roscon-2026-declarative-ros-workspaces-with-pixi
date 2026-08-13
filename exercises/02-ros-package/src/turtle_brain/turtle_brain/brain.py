# A tiny ROS 2 node that drives the turtlesim turtle with PyTorch.
#
# Each tick it runs a small tensor computation to produce a velocity, on the GPU
# when one is available and on the CPU otherwise. The maths is throwaway on
# purpose. The point is that a normal ROS node can use PyTorch, and that the same
# package resolves for a laptop, a GPU box, or a Jetson.
#
# Run turtlesim in one terminal (`pixi run sim`) and this node in another.

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import torch


class TurtleBrain(Node):
    def __init__(self):
        super().__init__("turtle_brain")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.get_logger().info(f"turtle_brain is thinking on: {self.device}")

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.step_count = 0
        self.timer = self.create_timer(0.1, self.step)

    def step(self):
        # A small tensor op, just to exercise PyTorch on the selected device.
        t = torch.tensor([self.step_count * 0.1], device=self.device)
        linear = float(torch.cos(t).item())
        angular = float(torch.sin(t).item())
        self.step_count += 1

        twist = Twist()
        twist.linear.x = 2.0 * linear
        twist.angular.z = 2.0 * angular
        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleBrain()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
