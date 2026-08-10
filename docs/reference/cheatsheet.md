---
icon: lucide/terminal
---

# Command cheat sheet

Every command links to its page in the [Pixi documentation](https://pixi.prefix.dev/latest/).

<!-- TODO(content): trim to what the exercises use, then verify every line. A cheat sheet with a
     command that does not exist is worse than no cheat sheet. -->

## Workspace

| Command | What it does |
| --- | --- |
| [`pixi init`](https://pixi.prefix.dev/latest/reference/cli/pixi/init/) | Create a `pixi.toml` in the current directory |
| [`pixi workspace channel add <channel>`](https://pixi.prefix.dev/latest/reference/cli/pixi/workspace/channel/add/) | Add a channel |
| [`pixi workspace platform add <platform>`](https://pixi.prefix.dev/latest/reference/cli/pixi/workspace/platform/add/) | Add a platform |
| [`pixi add <package>`](https://pixi.prefix.dev/latest/reference/cli/pixi/add/) | Add a dependency and update the lockfile |
| [`pixi add --pypi <package>`](https://pixi.prefix.dev/latest/concepts/conda_pypi/) | Add a dependency from PyPI |
| [`pixi remove <package>`](https://pixi.prefix.dev/latest/reference/cli/pixi/remove/) | Remove a dependency |

## Running things

| Command | What it does |
| --- | --- |
| [`pixi run <task>`](https://pixi.prefix.dev/latest/reference/cli/pixi/run/) | Run a task from `[tasks]` |
| [`pixi run <command>`](https://pixi.prefix.dev/latest/reference/cli/pixi/run/) | Run any command inside the environment |
| [`pixi shell`](https://pixi.prefix.dev/latest/reference/cli/pixi/shell/) | Open a shell with the environment activated |
| [`pixi run -e <env> <task>`](https://pixi.prefix.dev/latest/workspace/multi_environment/) | Run in a specific environment |
| [`pixi task list`](https://pixi.prefix.dev/latest/reference/cli/pixi/task/list/) | List the available tasks |

## Environments and locking

| Command | What it does |
| --- | --- |
| [`pixi install`](https://pixi.prefix.dev/latest/reference/cli/pixi/install/) | Install the environment from the lockfile |
| [`pixi lock`](https://pixi.prefix.dev/latest/reference/cli/pixi/lock/) | Update the lockfile without installing |
| [`pixi lock --check`](https://pixi.prefix.dev/latest/reference/cli/pixi/lock/) | Fail if the lockfile is out of date. Use this in CI |
| [`pixi update <package>`](https://pixi.prefix.dev/latest/reference/cli/pixi/update/) | Update one package to the newest allowed version |
| [`pixi list`](https://pixi.prefix.dev/latest/reference/cli/pixi/list/) | Show what is installed |
| [`pixi tree <package>`](https://pixi.prefix.dev/latest/reference/cli/pixi/tree/) | Show why a package is in the environment |
| [`pixi clean`](https://pixi.prefix.dev/latest/reference/cli/pixi/clean/) | Remove `.pixi/` |

## Inspecting

| Command | What it does |
| --- | --- |
| [`pixi info`](https://pixi.prefix.dev/latest/reference/cli/pixi/info/) | Versions, cache locations, and the virtual packages your machine reports ([field by field](https://pixi.prefix.dev/latest/advanced/explain_info_command/)) |
| [`pixi search <package>`](https://pixi.prefix.dev/latest/reference/cli/pixi/search/) | Search the configured channels |
| [`pixi list --platform <platform>`](https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/) | What would be installed on another platform |

## Building

| Command | What it does |
| --- | --- |
| [`pixi build`](https://pixi.prefix.dev/latest/build/getting_started/) | Build the `[package]` in this workspace into a `.conda` file |
| [`pixi publish`](https://pixi.prefix.dev/latest/reference/cli/pixi/publish/) | Build and upload the package to a channel |

The ROS build backend that turns a `package.xml` into a conda package is
[`pixi-build-ros`](https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/).

## RoboStack channels

| ROS distribution | Channel |
| --- | --- |
| Jazzy (LTS) | [`https://prefix.dev/robostack-jazzy`](https://prefix.dev/channels/robostack-jazzy) |
| Humble (LTS) | [`https://prefix.dev/robostack-humble`](https://prefix.dev/channels/robostack-humble) |
| Kilted | [`https://prefix.dev/robostack-kilted`](https://prefix.dev/channels/robostack-kilted) |
| Noetic (ROS 1) | [`https://prefix.dev/robostack-noetic`](https://prefix.dev/channels/robostack-noetic) |

<!-- TODO(content): add the distributions we leave out, or say explicitly that this is a subset. -->

## Reading further

| Topic | Page |
| --- | --- |
| Every field in `pixi.toml` | [Manifest reference](https://pixi.prefix.dev/latest/reference/pixi_manifest/) |
| All commands and flags | [CLI reference](https://pixi.prefix.dev/latest/reference/cli/pixi/) |
| What the lockfile guarantees | [Lockfile](https://pixi.prefix.dev/latest/workspace/lock_file/) |
| Features, environments, and solve groups | [Multi environment](https://pixi.prefix.dev/latest/workspace/multi_environment/) |
| Task dependencies, inputs, and outputs | [Advanced tasks](https://pixi.prefix.dev/latest/workspace/advanced_tasks/) |
| Building your own ROS packages | [Build a ROS package](https://pixi.prefix.dev/latest/build/ros/) |
| Pixi for robotics, start to finish | [Robotics](https://pixi.prefix.dev/latest/robotics/) and the [ROS 2 tutorial](https://pixi.prefix.dev/latest/tutorials/ros2/) |
