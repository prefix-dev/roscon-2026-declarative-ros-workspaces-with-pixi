---
icon: lucide/cpu
---

# CUDA

!!! abstract "30 minutes, presented"

    **Slides:** [CUDA](../slides/) &middot; **Followed by:** [Exercise 2](../exercises/02-ros-package.md)

    By the end of this block you should understand how Pixi decides whether your machine can run a CUDA build, and how to declare CUDA in your workspace so a GPU-accelerated ROS node installs the same way everywhere.

GPU's are notoriously difficult to get working, doing this in combination with ROS makes things even more complicated.
You need a specific CUDA version, matching drivers, and a toolkit that agrees with your ROS packages.
Pixi comes with some features to help you manage CUDA dependencies.


Pixi can't control every CUDA related dependency, it needs the NVIDIA driver to be installed on the machine.
On Ubuntu, you can install the NVIDIA driver with:

```bash
sudo apt install nvidia-driver-535 # Your driver version may be different, check your system settings
```

When you can run `nvidia-smi` and see your GPU, you can use Pixi to install the right CUDA toolkit and libraries for your ROS packages.

## Virtual packages

Pixi needs to know what your machine can actually do before it solves which dependencies to install.
It learns that through virtual packages: not real packages you install, but facts about the system.

As Pixi requires to solve all dependencies for all potential systems we're going to define a virtual platform in the `pixi.toml` file, and then declare a virtual package for CUDA.

We'll define a platform with more information than the standard `linux-64` platform, and then declare a virtual package for CUDA 12.

You can run `pixi workspace platform add cuda-linux-64=linux-64 --cuda 12` to add this platform to your workspace, or just declare it in the `pixi.toml` file:

```toml title="pixi.toml"
[workspace]
platforms = [{name = "cuda-linux-64", platform = "linux-64", cuda = "12"}]
channels = ["conda-forge"]
```

When you then add packages that require CUDA, Pixi will be able to solve the environment and select the right packages.

```toml title="pixi.toml"
[dependencies]
pytorch-gpu = ">=2.10"

[tasks]
test = "python -c 'import torch; print(torch.cuda.is_available())'"
```

## Special configuration for your cuda machines

Pixi supports target specific configuration, this also works for cuda specific platforms.

- Use the `[target."cuda-*"]` table to define target specific configuration, this requires the platforms to have name that starts with `cuda-`.
- Conditional dependencies: `pytorch = { version = ">=2.10", when = "__cuda > 12" }` this allows you to depend on a package only when the environment is running in a CUDA machine.

```toml title="pixi.toml"
[workspace]
platforms = [
  {name = "cuda-linux-64", platform = "linux-64", cuda = "12"},
  {name = "cuda-win-64", platform = "win-64", cuda = "12"},
  "osx-arm64",
]
channels = ["conda-forge"]

[dependencies]
python = ">=3.12"
# Conditional dependency:
pytorch-gpu = { version = ">=2.10", when = "__cuda > 12" }
pytorch = ">=2.10" # fallback for non-cuda machines like osx-arm64

# Only run this task on a CUDA machine, otherwise it will be skipped
[target."cuda-*".tasks]
start = "echo 'Starting on a CUDA machine'"

[tasks]
start = "echo 'Starting on a non-CUDA machine'"
```


## Jetson and other robots

<!-- TODO(content):
     - linux-aarch64 vs. the Jetson's CUDA and L4T reality.
     - `[system-requirements]` for the robot, not for the laptop.
     - Cross-solving on your laptop for hardware you do not have in front of you.
     - Shipping to the robot: pixi on device, or `pixi-pack`.
       NOTE: pixi-pack --platform takes the conda subdir, so `pixi-pack --platform linux-aarch64`,
       NOT the named platform `jetson` (verified pixi-pack 0.7.10; see pixi-pack-named-platforms memory).
-->
