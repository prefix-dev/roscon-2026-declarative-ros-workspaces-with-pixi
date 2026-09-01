cmake_minimum_required(VERSION 3.16)
project(turtle_dancer)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(dance src/dance.cpp)
ament_target_dependencies(dance rclcpp geometry_msgs)

# Installing into lib/${PROJECT_NAME} is what makes `ros2 run` able to find it.
install(TARGETS dance DESTINATION lib/${PROJECT_NAME})

ament_package()
