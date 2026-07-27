# Solutions

The finished version of each exercise. Every one is a standalone Pixi workspace, installed and
smoke-tested on Linux, macOS and Windows on every commit, so these are never stale.

| Directory | Shows |
| --- | --- |
| `01-ros-workspace/` | ROS 2 Jazzy from RoboStack, tasks, five platforms, no ROS on the machine |
| `02-ros-package/` | A ROS package built by the `pixi-build-ros` backend, plus a CUDA platform variant |
| `03-collaboration/` | Every platform, a named Jetson target, a lockfile gate, Docker and publishing |

Run any of them from the repository root:

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

Or from inside the directory:

```bash
cd solutions/01-ros-workspace
pixi run sim
```

Re-solve all of them after a manifest change:

```bash
pixi run lock-solutions
```
