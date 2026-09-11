---
icon: lucide/cpu
---

# CUDA

!!! abstract "30 minutes, presented"

    **Slides:** [CUDA](../slides/) &middot; **Followed by:** [Exercise 1](../exercises/01-ros-workspace.md)

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

| Virtual package | What it tells Pixi |
| --- | --- |
| `__cuda` | The maximum CUDA version supported by the installed NVIDIA driver. |
| `__glibc` | The version of the GNU C Library available on the system. |
| `__unix` | That the system is Unix-like, such as Linux or macOS. |
| `__osx` | The macOS version. |
| `__linux` | The Linux kernel version. |
| `__archspec` | The CPU architecture and supported instruction set, such as `x86_64_v3` or `aarch64`. |

Run `pixi info` to see the virtual packages detected on your machine.
For example, `__cuda` describes driver support, not the CUDA toolkit installed in your workspace, and `__archspec` describes the CPU, not the GPU.
See [Virtual packages in the conda ecosystem](https://prefix.dev/blog/virtual-packages-in-the-conda-ecosystem) for more background.

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

A Jetson has two architectures to account for: its ARM CPU and its NVIDIA GPU.
The CPU needs `linux-aarch64` packages, but that alone does not tell you whether their CUDA code can run on the GPU.
Jetson AGX Orin, Orin NX, and Orin Nano have GPU compute capability **8.7**, written as **`sm_87`** in CUDA compiler targets.
Other Jetson generations use different GPU architectures; check [NVIDIA's compute capability table](https://developer.nvidia.com/cuda/gpus) for your board.

CUDA packages need compatible GPU kernels as well as compatible CPU code.
Building kernels for `sm_87` gives Orin native GPU code to execute.
An ARM package built only for server GPUs can install successfully and detect CUDA, yet fail when your application actually launches a kernel.
Declaring `cuda = "12"` in Pixi describes driver compatibility; it does not rebuild a package to add missing GPU architectures.

### How the PyTorch feedstock handles Orin

Conda-forge builds both CPU and GPU PyTorch packages in [pytorch-cpu-feedstock](https://github.com/conda-forge/pytorch-cpu-feedstock).
Its [build script](https://github.com/conda-forge/pytorch-cpu-feedstock/blob/main/recipe/build.sh#L242-L266) selects GPU architectures through `TORCH_CUDA_ARCH_LIST`.
The Tegra build branch, used for Jetson Orin, sets:

```bash title="recipe/build.sh (Tegra branch)"
export TORCH_CUDA_ARCH_LIST="8.7+PTX"
```

`8.7` includes native `sm_87` kernels; `+PTX` also includes an intermediate representation that a compatible driver can compile at runtime.
This is a package **build setting**: setting it after installing PyTorch does not change the kernels already in the package.
The script also includes `8.7` in its CUDA 13.0 `linux-aarch64` architecture list, where there is no separate Tegra variant.

Jetson's system software matters too.
It uses the driver supplied through Jetson Linux / JetPack, rather than the desktop driver installation shown above.
For example, [JetPack 6.2.1 ships CUDA 12.6](https://docs.nvidia.com/jetson/jetpack/6.2.1/release-notes/index.html).
Choose package builds compatible with that stack and with your GPU; a newer CUDA build is not automatically suitable for an older JetPack installation.

### Check a real GPU operation

On the Jetson, save this as `check_gpu.py` and run it in your PyTorch environment with `pixi run python check_gpu.py`:

```python title="check_gpu.py"
import torch

if not torch.cuda.is_available():
    raise RuntimeError("PyTorch cannot access CUDA; check the driver and package build.")

print("GPU:", torch.cuda.get_device_name(0))
print("Compute capability:", torch.cuda.get_device_capability(0))
print("Architectures in this build:", torch.cuda.get_arch_list())

values = torch.ones(4, device="cuda")
result = (values * 2).sum()
print("GPU result:", result.item())  # Expected: 8.0
```

On Orin, expect compute capability `(8, 7)`.
The architecture list shows which native GPU targets the installed PyTorch build includes; the tensor operation checks that it can actually execute GPU work.
This catches the failure documented in [the feedstock's Orin support issue](https://github.com/conda-forge/pytorch-cpu-feedstock/issues/303): CUDA was detected, but the package lacked compatible kernels.
