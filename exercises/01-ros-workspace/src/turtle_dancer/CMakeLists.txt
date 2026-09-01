cmake_minimum_required(VERSION 3.16)
project(turtle_dancer)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(dance src/dance.cpp)
# ROS CMake exports currently drag Python generator libraries into the link
# interface. They are not used by this C++ node, so let the platform linker
# drop unused dynamic libraries instead of requiring Python C API symbols.
if(APPLE)
  target_link_options(dance PRIVATE -Wl,-dead_strip_dylibs)
elseif(UNIX)
  target_link_options(dance PRIVATE -Wl,--as-needed)
endif()

target_link_libraries(dance PRIVATE
  rclcpp::rclcpp
  geometry_msgs::geometry_msgs__rosidl_typesupport_cpp
)

# Installing into lib/${PROJECT_NAME} is what makes `ros2 run` able to find it.
install(TARGETS dance DESTINATION lib/${PROJECT_NAME})

ament_package()
