from setuptools import find_packages, setup

package_name = "turtle_dancer"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Ruben Arts",
    maintainer_email="ruben@prefix.dev",
    description="Drive the turtlesim turtle in a circle",
    license="BSD-3-Clause",
    entry_points={
        "console_scripts": [
            f"dance = {package_name}.dance:main",
        ],
    },
)
