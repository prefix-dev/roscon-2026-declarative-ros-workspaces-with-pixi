# Solutions

The finished version of each exercise.
Every one is a standalone Pixi workspace, installed and smoke-tested on Linux, macOS and Windows on every commit, so these are never stale.

| Directory | Shows |
| --- | --- |
| `01-ros-workspace/` | Lyrical and Kilted, a colcon-built C++ node, a PyTorch brain, CPU/CUDA/Jetson platform resolutions, and a real CUDA computation |
| `02-ros-package/` | The same C++ package and a Python one, both built by the `pixi-build-ros` backend: no colcon, no sourcing, and a rebuild whenever a source file changes |
| `03-collaboration/` | Prebuilt ROS 2 talker and listener binaries, named `jetson` and `workstation-gpu` targets solved from a laptop, a lockfile gate, Docker, and a workspace to pack and unpack |

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

Exercise 1 keeps colcon output in `build/<environment>`, `install/<environment>` and `log/<environment>`.
Build once in each environment before launching the local nodes:

```bash
pixi run -e default build
pixi run -e default test-overlay
pixi run -e kilted build
pixi run -e kilted test-overlay
pixi run -e default test-overlay
```

Run these commands outside an activated `pixi shell`.
Each new command activates only that environment's `local_setup` overlay.

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

For Exercise 3, follow the [pack and unpack solution](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/03-collaboration/#34-pack-the-environment) from `solutions/03-collaboration/` instead of the exercise directory.
It starts fresh with prebuilt packages rather than the local packages from Exercise 2.
The archive includes `demo_nodes_cpp`; after unpacking and activating, run `ros2 pkg executables demo_nodes_cpp`, then `ros2 run demo_nodes_cpp talker`.
The talker logs `Publishing: 'Hello World: N'` until you stop it with Ctrl+C.

Re-solve all of them after a manifest change:

```bash
pixi run lock-solutions
```
