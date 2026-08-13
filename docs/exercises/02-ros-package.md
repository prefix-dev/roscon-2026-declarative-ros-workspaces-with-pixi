---
icon: lucide/zap
---

# Exercise 2: CUDA, PyTorch and a Jetson

!!! plain "30 minutes, hands-on"

    **Work in:** `exercises/02-ros-package/` &middot; **Solution:** `solutions/02-ros-package/` &middot; **After:** [CUDA](../explainers/cuda.md)

    **Goal:** add PyTorch on CUDA to your workspace, solve it for every platform including a Jetson from your own laptop, and run it on a real GPU.

<!-- TODO(content): the TOML below is hand-written for the docs-first pass. Once
     solutions/02-ros-package is rebuilt as the CUDA/PyTorch/Jetson workspace,
     replace these blocks with `--8<--` section includes from that manifest, and
     confirm the conditional-dependency syntax solves. -->

You have a ROS workspace from Exercise 1.
Now you add GPU work to it: PyTorch on CUDA.
The part that makes this workshop-friendly is that you can declare and solve a GPU environment from a laptop that has no GPU, even a Mac, and only install it where the hardware is.

## Step 1: Add PyTorch with CUDA

PyTorch's GPU build needs CUDA, and Pixi only picks a CUDA build for a platform it knows has a GPU.
You saw why in [CUDA](../explainers/cuda.md): the `__cuda` virtual package.
You tell Pixi a platform has a GPU by giving it a CUDA version.

Add the CUDA platform, the ROS channel, the packages, and a check task:

```bash
pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
pixi workspace channel add robostack-jazzy
pixi add ros-jazzy-ros-base pytorch-gpu
pixi task add gpu-check "python -c 'import torch; print(torch.cuda.is_available())'"
```

Solve it and look, without a GPU and without installing anything:

```bash
pixi list --platform cuda-linux-64
```

Pixi resolves the CUDA build of PyTorch for that platform.
Solving is not installing, so this works on any laptop in the room.

## Step 2: Every platform, one workspace

Your teammates are not all on a GPU box.
Add the ordinary platforms next to the CUDA one:

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```

The GPU build cannot install on those, so make it conditional and add a CPU fallback.
Edit `[dependencies]`:

```toml title="pixi.toml"
[dependencies]
# GPU build where CUDA is present, CPU build everywhere else.
pytorch-gpu = { version = ">=2.5", when = "__cuda" }
pytorch = ">=2.5"
```

Now inspect what each machine would get, all from where you are sitting:

```bash
pixi list --platform win-64          # your colleague on Windows: CPU build
pixi list --platform cuda-linux-64   # the GPU box: CUDA build
```

## Step 3: Target a Jetson

A Jetson is `linux-aarch64` with CUDA.
That is just another platform, so you add it the same way, with its own CUDA version:

```bash
pixi workspace platform add jetson=linux-aarch64 --cuda 13
```

!!! note "We assume JetPack 7.2 or newer"

    JetPack 7.2 and up ship CUDA 13, so that is what we target here.
    On an older JetPack the CUDA version is different (JetPack 6 ships CUDA 12.6), so match `cuda` to what your robot actually runs.

Solve the robot's environment from your laptop:

```bash
pixi list --platform jetson
```

That is a complete CUDA environment for a machine you are not sitting at.
You solve on your laptop and install on the Jetson.

## Step 4: Run it on a real GPU

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
On a laptop the Jetson environment still resolves, which is the point.

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
