# Solutions

The finished version of each exercise.
Every one is a standalone Pixi workspace, installed and smoke-tested on Linux, macOS and Windows on every commit, so these are never stale.

| Directory | Shows |
| --- | --- |
| `01-ros-workspace/` | ROS 2 from RoboStack on five platforms, tasks, a colcon-built C++ package, and Lyrical plus Kilted as two environments in one workspace |
| `02-ros-package/` | The same C++ package and a Python one, both built by the `pixi-build-ros` backend: no colcon, no sourcing, and a rebuild whenever a source file changes |
| `03-collaboration/` | Every platform, named `jetson` and `workstation-gpu` targets solved from a laptop, a lockfile gate, Docker and publishing |

Run any of them from the repository root:

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml -e kilted sim   # the same task, a different distro
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
