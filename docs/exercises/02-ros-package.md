---
icon: lucide/zap
---

# Exercise 2: CUDA, PyTorch and a Jetson

!!! plain "30 minutes, hands-on"

    **Work in:** `exercises/02-ros-package/` &middot; **Solution:** `solutions/02-ros-package/` &middot; **After:** [CUDA](../explainers/cuda.md)

    **Goal:** add PyTorch on CUDA to your workspace, solve it for every platform including a Jetson from your own laptop, and run it on a real GPU.

<!-- TODO(content): the TOML below is hand-written but verified against pixi 0.76.2 (all commands
     run, all `pixi list` output below is real). Once solutions/02-ros-package is rebuilt as the
     CUDA/PyTorch/Jetson workspace, replace these blocks with `--8<--` section includes from that
     manifest. -->

This time there is a `pixi.toml` waiting for you: a fresh workspace with `conda-forge` and the three laptop platforms, nothing else.
You add the GPU work: PyTorch on CUDA.
You can declare and solve a GPU environment from a laptop that has no GPU, even a Mac, and only install it where the hardware is.

## 2.1 Add PyTorch with CUDA

PyTorch's GPU build needs CUDA, and Pixi only picks a CUDA build for a platform it knows has a GPU.
You saw why in [CUDA](../explainers/cuda.md): the `__cuda` virtual package.
You tell Pixi a platform has a GPU by declaring a named platform with a CUDA version.

!!! exercise "Your turn"

    1. Add a platform named `cuda-linux-64`: a `linux-64` variant that declares CUDA 12.
       Hint: `pixi workspace platform add --help`.
    2. Add the `robostack-jazzy` channel and `ros-jazzy-ros-base`, like in Exercise 1.
    3. Add PyTorch in the manifest, by hand: the GPU build where CUDA is present, the CPU build everywhere else.
       Hint: a dependency can be conditional on a virtual package, with `when = "__cuda"`.
    4. Add a `gpu-check` task that prints `torch.cuda.is_available()`.
    5. Inspect what the GPU platform would get, without installing anything.
       Hint: `pixi list --platform` takes any platform from your manifest, and a package name to filter on.

??? success "Solution"

    ```bash
    # 1
    pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
    # 2
    pixi workspace channel add --prepend https://prefix.dev/robostack-jazzy
    pixi add ros-jazzy-ros-base
    ```

    3: in the manifest:

    ```toml title="exercises/02-ros-package/pixi.toml"
    [dependencies]
    # GPU build where CUDA is present, CPU build everywhere else.
    pytorch-gpu = { version = ">=2.5", when = "__cuda" }
    pytorch = ">=2.5"
    ```

    ```bash
    # 4
    pixi task add gpu-check "python -c 'import torch; print(torch.cuda.is_available())'"
    # 5
    pixi list --platform cuda-linux-64 pytorch
    ```

    ```
    Name         Version  Build                                Size  Kind   Source
    pytorch      2.12.0   cuda129_mkl_py312_h6997aeb_300  24.79 MiB  conda  https://prefix.dev/conda-forge
    pytorch-gpu  2.12.0   cuda129_mkl_h0d04637_300        57.02 KiB  conda  https://prefix.dev/conda-forge
    ```

    Pixi resolved the CUDA build of PyTorch for that platform.
    Solving is not installing, so this works on any laptop in the room.

    Resulting `pixi.toml` file:

    ```toml title="exercises/02-ros-package/pixi.toml" hl_lines="3 4 8 11 12 13"
    [workspace]
    name = "02-ros-package"
    channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]
    platforms = ["linux-64", "osx-arm64", "win-64", { name = "cuda-linux-64", platform = "linux-64", cuda = "12" }]
    version = "0.1.0"

    [tasks]
    gpu-check = "python -c 'import torch; print(torch.cuda.is_available())'"

    [dependencies]
    ros-jazzy-ros-base = ">=0.11.0,<0.12"
    pytorch-gpu = { version = ">=2.5", when = "__cuda" }
    pytorch = ">=2.5"
    ```

## 2.2 Every platform, one workspace

Your teammates are not all on a GPU box.
The starter already declares `linux-64`, `osx-arm64` and `win-64`, so the same manifest serves them too.

!!! exercise "Your turn"

    1. Inspect what your colleague on Windows would get.
    2. Compare it with what the GPU box gets.

??? success "Solution"

    ```bash
    # 1
    pixi list --platform win-64 pytorch
    # 2
    pixi list --platform cuda-linux-64 pytorch
    ```

    On Windows there is no `__cuda`, so the CPU fallback wins:

    ```
    Name     Version  Build                            Size  Kind   Source
    pytorch  2.12.0   cpu_mkl_py312_ha8331fa_100  22.13 MiB  conda  https://prefix.dev/conda-forge
    ```

## 2.3 Target a Jetson

A Jetson is `linux-aarch64` with CUDA.
That is just another platform, so you add it the same way, with its own CUDA version.

!!! exercise "Your turn"

    1. Add a platform named `jetson`: `linux-aarch64` with CUDA 13 and glibc 2.38.
    2. Solve the robot's environment from your laptop and inspect it.

!!! note "We assume JetPack 7.2 or newer"

    JetPack 7.2 and up ship CUDA 13, so that is what we target here.
    On an older JetPack the CUDA version is different (JetPack 6 ships CUDA 12.6), so match `cuda` to what your robot actually runs.
    The same goes for `glibc`: match it to the OS image on the robot.

??? success "Solution"

    ```bash
    # 1
    pixi workspace platform add jetson=linux-aarch64 --cuda 13 --glibc 2.38
    # 2
    pixi list --platform jetson pytorch
    ```

    ```
    Name         Version  Build                                    Size  Kind   Source
    pytorch      2.12.0   cuda130_generic_py312_hb6f7e9f_200  24.23 MiB  conda  https://prefix.dev/conda-forge
    pytorch-gpu  2.12.0   cuda129_generic_hda344be_200        57.28 KiB  conda  https://prefix.dev/conda-forge
    ```

    That is a complete CUDA environment for a machine you are not sitting at.
    You solve on your laptop and install on the Jetson.

    Resulting platform list:

    ```toml title="exercises/02-ros-package/pixi.toml"
    platforms = ["linux-64", "osx-arm64", "win-64", { name = "cuda-linux-64", platform = "linux-64", cuda = "12" }, { name = "jetson", platform = "linux-aarch64", cuda = "13", glibc = "2.38" }]
    ```

## 2.4 Run it on a real GPU

<!-- TODO(content): the GPU payoff on a cloud instance (Brev launchable, link TBD;
     see IMPLEMENTATION_PLAN.md Stage 5). Moved here from Exercise 3.

     Two paths, both written and tested:
       * GPU box: install the environment, `pixi run gpu-check` prints True, run the node.
       * Laptop only: solve and inspect, as in the steps above. Nobody is blocked.

     Kick off the instance at the START of the session so provisioning is not on the clock. -->

## Check your work

```bash
pixi run gpu-check                # on a GPU box: torch sees CUDA
pixi list --platform jetson       # a Jetson environment, resolved from your laptop
```

On a GPU box `gpu-check` prints `True`.
On a laptop the Jetson environment still resolves; installing it is the only part that needs the robot.

## Going further

<!-- TODO(content):
     - Add rerun or another GPU-accelerated tool alongside PyTorch.
     - Pin an exact CUDA version and re-solve; look at what moved in the lockfile.
     - `pixi list --platform jetson` versus `--platform cuda-linux-64`: spot the aarch64 builds.
-->

!!! note "With your own workspace"

    <!-- TODO(content): add a CUDA platform variant to their existing workspace and a GPU
         dependency they actually use, then solve for it. If they have a robot, add its platform
         and cross-solve for it from the laptop in front of them. -->

---

Next: [Collaboration, CI/CD & Docker](../explainers/collaboration.md).
