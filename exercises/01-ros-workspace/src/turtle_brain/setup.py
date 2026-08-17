from setuptools import setup

package_name = "turtle_brain"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Prefix.dev",
    maintainer_email="hi@prefix.dev",
    description="A minimal ROS 2 node that drives turtlesim using PyTorch.",
    license="BSD-3-Clause",
    entry_points={
        "console_scripts": [
            "brain = turtle_brain.brain:main",
        ],
    },
)
