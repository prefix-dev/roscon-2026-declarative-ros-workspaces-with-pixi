// Drive the turtlesim turtle in a circle.
//
// In Exercise 1 this is built by colcon, which means you have to source
// install/setup.bash before `ros2 run` can find it. Exercise 2 hands the build
// to Pixi and that step disappears.

#include <chrono>
#include <memory>

#include <geometry_msgs/msg/twist.hpp>
#include <rclcpp/rclcpp.hpp>

using namespace std::chrono_literals;

class Dancer : public rclcpp::Node
{
public:
  Dancer()
  : Node("dancer")
  {
    linear_speed_ = declare_parameter("linear_speed", 1.0);
    angular_speed_ = declare_parameter("angular_speed", 0.8);

    publisher_ = create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
    timer_ = create_wall_timer(100ms, [this]() {this->step();});

    RCLCPP_INFO(get_logger(), "Dancing. Start `pixi run sim` to watch.");
  }

private:
  void step()
  {
    geometry_msgs::msg::Twist twist;
    twist.linear.x = linear_speed_;
    twist.angular.z = angular_speed_;
    publisher_->publish(twist);
  }

  double linear_speed_;
  double angular_speed_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Dancer>());
  rclcpp::shutdown();
  return 0;
}
