# Exercises

Work in these directories.
Each one starts where the previous exercise ended, so you can jump in anywhere.

| Directory | You start with | You end with |
| --- | --- | --- |
| `01-ros-workspace/` | An empty workspace with pre-written C++ and PyTorch nodes | ROS 2 running, your node built by colcon, two distros side by side, and a PyTorch node resolved for a GPU box and a Jetson |
| `02-ros-package/` | That workspace, trimmed to Jazzy, with colcon doing the building | Pixi building the C++ and a Python package from their `package.xml`, no sourcing, no `build/` directory, an edit-run loop |
| `03-collaboration/` | A working multi-platform workspace | CI green on every platform, and a Docker image to deploy |

The finished versions live in [`../solutions/`](../solutions/).
They are installed and smoke-tested on Linux, macOS and Windows on every commit, so if something here does not work, compare against those.

Instructions are on the [workshop site](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/).
