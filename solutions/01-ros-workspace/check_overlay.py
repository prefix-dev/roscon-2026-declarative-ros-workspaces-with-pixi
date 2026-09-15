"""Check the installed ROS overlay after building in the selected environment."""

import os
from pathlib import Path

import rclpy
import turtle_brain
from ament_index_python.packages import get_package_prefix
from ros2run.api import get_executable_path

workspace = Path(__file__).resolve().parent
environment = os.environ["PIXI_ENVIRONMENT_NAME"]
expected_distro = {"default": "lyrical", "kilted": "kilted"}[environment]
underlay = Path(os.environ["CONDA_PREFIX"]).resolve()
# Conda installs ROS under Library on Windows, but Python at the environment root.
ros_prefix = underlay / "Library" if os.name == "nt" else underlay
overlay = workspace / "install" / environment

assert os.environ["ROS_DISTRO"] == expected_distro, os.environ["ROS_DISTRO"]
assert Path(rclpy.__file__).resolve().is_relative_to(underlay), rclpy.__file__
assert Path(get_package_prefix("rclcpp")).resolve() == ros_prefix, get_package_prefix("rclcpp")
assert Path(turtle_brain.__file__).resolve().is_relative_to(overlay), turtle_brain.__file__

for package, executable in [("turtle_dancer", "dance"), ("turtle_brain", "brain")]:
    prefix = Path(get_package_prefix(package)).resolve()
    assert prefix.is_relative_to(overlay), (package, prefix, overlay)
    path = get_executable_path(package_name=package, executable_name=executable)
    assert path is not None, (package, executable)
    assert Path(path).resolve().is_relative_to(overlay), path
    print(f"{package} {executable}: {path}")

print(f"ROS distro: {os.environ['ROS_DISTRO']}")
print(f"rclpy: {rclpy.__file__}")
print(f"brain package: {turtle_brain.__file__}")
