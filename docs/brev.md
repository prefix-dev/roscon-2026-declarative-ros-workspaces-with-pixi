---
icon: lucide/cloud
---

# Brev fallback setup

Use this page only when a local laptop is not enough:

- you do not have access to an NVIDIA GPU for the CUDA run;
- your laptop cannot install the workshop environments in time;
- the room network is struggling and instructors ask the group to switch to prepared cloud machines.

If your laptop can run the setup in [Before you start](setup.md), stay local.
That is the default path for the workshop.
Brev is a fallback, not an extra prerequisite.

!!! warning "Wait for the instructor coupon"

    Do **not** create a Brev instance yet.
    Creating cloud GPU machines can use paid credits, and the workshop machines should be created with the coupon from the instructors.
    Wait until the instructors share the coupon and tell you which instance type to use.

## 1. Install the Brev CLI

Brev is the NVIDIA cloud development environment we can use for the fallback machines.
Install its CLI with Pixi:

```bash
pixi global install brev
brev --help
```

!!! note "Windows users"

    Brev supports Windows through WSL.
    Run the Brev CLI commands from your WSL Ubuntu terminal, not from PowerShell.

## 2. Create or log in to your Brev account

Create an account at <https://login.brev.nvidia.com/signin>, then log in from your terminal:

```bash
brev login
```

!!! warning "Wait for the coupon"

    Log in now, but do not create an instance yet.
    Wait until the instructors share the Brev coupon.

The CLI asks for your email address and opens a browser for authentication.
When login succeeds, you should see your Brev account in the browser.




Select the organization for the workshop:

```bash
brev org set 2026-ROSCon
```

## 3. Create the fallback instance

From the root of this workshop repository, run:

```bash
brev create "$(whoami)-roscon-pixi" \
  --startup-script @docs/code/brev/setup_brev.sh \
  --type massedcompute_L40S
```

The startup script installs Pixi, clones this repository onto the instance, and pre-downloads both ROS environments with PyTorch.
On a compatible NVIDIA GPU machine, the preferred CUDA platform selects the GPU build.
That means you can keep working even if the local room Wi-Fi is slow.

If you are not inside a fresh clone of the workshop repository, download the script first:

```bash
curl -sLO https://raw.githubusercontent.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi/main/docs/code/brev/setup_brev.sh
brev create "$(whoami)-roscon-pixi" \
  --startup-script @./setup_brev.sh \
  --type massedcompute_L40S
```

!!! tip "Choosing the instance type"

    Use the instance type announced by the instructors.
    For CUDA exercises it must have an NVIDIA GPU and a recent driver.
    If we only need a bandwidth fallback, a CPU instance may be enough.

## 4. Connect to the instance

Open it in VS Code:

```bash
brev open "$(whoami)-roscon-pixi" code
```

Or use a terminal:

```bash
brev shell "$(whoami)-roscon-pixi"
```

The repository is cloned here:

```bash
cd ~/roscon-2026-declarative-ros-workspaces-with-pixi
```

Check Pixi and the pre-warmed environment:

```bash
pixi --version
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml topics
```

For [Exercise 1's CUDA run](exercises/01-ros-workspace.md#19-run-it-on-a-real-gpu), the instance must have an NVIDIA GPU and a compatible driver.
Run this inside the Brev terminal, from the repository root:

```bash
nvidia-smi
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml --platform cuda-linux-64 cuda-check
```

Expect the GPU name, compute capability and `GPU result: 8.0`.
This executes a tensor operation on CUDA and exits; it fails rather than falling back to CPU.
If it fails, ask an instructor to check the instance type, driver and selected platform.

Then try the ROS node on the same device:

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml --platform cuda-linux-64 brain
```

Look for `thinking on: cuda`, then stop it with ++ctrl+c++.
The node publishes without a turtlesim window, so this works over SSH.
Return to [Exercise 1](exercises/01-ros-workspace.md#19-run-it-on-a-real-gpu) for the explanation and Jetson commands.

## 5. Know the limits

A Brev shell is excellent for dependency solving, CUDA checks and non-graphical ROS commands.
Graphical apps such as `turtlesim` are still easiest on your own laptop.
If the room switches fully to Brev, follow the instructor's live guidance for any GUI steps.

## 6. Clean up

When you are done, delete the instance so it stops using credits:

```bash
brev delete "$(whoami)-roscon-pixi"
```
