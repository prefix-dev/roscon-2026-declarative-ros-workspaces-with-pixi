cmake_minimum_required(VERSION 3.16)
project(turtle_dancer)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(dance src/dance.cpp)
target_link_libraries(dance rclcpp::rclcpp ${geometry_msgs_TARGETS})
# On macOS the ROS CMake targets also link the Python type-support libraries,
# which cannot load outside a Python interpreter. Drop what the node does not use.
if(APPLE)
  target_link_options(dance PRIVATE -Wl,-dead_strip_dylibs)
endif()

# Installing into lib/${PROJECT_NAME} is what makes `ros2 run` able to find it.
install(TARGETS dance DESTINATION lib/${PROJECT_NAME})

ament_package()
