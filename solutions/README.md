# Solutions

The finished version of each exercise.
Every one is a standalone Pixi workspace, installed and smoke-tested on Linux, macOS and Windows on every commit, so these are never stale.

| Directory | Shows |
| --- | --- |
| `01-ros-workspace/` | Lyrical and Kilted, a colcon-built C++ node, a PyTorch brain, CPU/CUDA/Jetson platform resolutions, and a real CUDA computation |
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

To try CUDA, use an NVIDIA GPU with a compatible driver.
From `solutions/01-ros-workspace/` on a Linux GPU machine:

```bash
pixi run --platform cuda-linux-64 cuda-check
pixi run --platform cuda-linux-64 build
pixi run --platform cuda-linux-64 brain
```

`cuda-check` prints `GPU result: 8.0` and fails if CUDA is unavailable.
The initial build creates the colcon overlay before the next command activates it.
The `brain` task launches `ros2 run turtle_brain brain` and depends on `build` for subsequent changes.
It keeps running; stop it with Ctrl+C.
On the supported Jetson, use `--platform jetson` instead.
Without suitable hardware, follow the [Brev setup](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/brev/) with the instructors.

Re-solve all of them after a manifest change:

```bash
pixi run lock-solutions
```
