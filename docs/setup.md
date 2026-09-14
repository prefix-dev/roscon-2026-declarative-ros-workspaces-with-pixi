---
icon: lucide/download
---

# Before you start

Everything below runs at home on your own laptop.
Doing it in advance means you spend the workshop learning instead of downloading.

## 1. Install Pixi

=== "Linux & macOS"

    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
    ```

Open a new terminal and check the version.
You need 0.77 or newer:

```bash
pixi --version
```

!!! note "Windows C++ compilers"

    The C++ exercises need Visual Studio 2022 Build Tools with the C++ workload and a Windows SDK.
    Follow [Microsoft's installation instructions](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=msvc-170).
    Pixi activates these tools but doesn't install them for you.

## 2. Get the workshop material

```bash
git clone https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi.git
cd roscon-2026-declarative-ros-workspaces-with-pixi
```

## 3. Warm up your cache

!!! warning "This is the step that matters"

    The exercises use two ROS distributions and PyTorch.
    Downloading them at home means the workshop installs from your disk instead of over conference Wi-Fi.
    Expect this to take a while and to use several GB.
    Run it the evening before, not on the morning of.

```bash
pixi install --all --manifest-path solutions/01-ros-workspace/pixi.toml
```

`--all` fetches both the Lyrical and the Kilted environments, including PyTorch for your machine.
It does not download the packages for every other platform.

## 4. Check that it works

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

A window with a turtle should appear.
Close it, then check the second distro too:

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml -e kilted sim
```

If both worked, you are ready.

!!! note "Interested in Docker?"

    If you're interested in the Docker part of the workshop, make sure Docker is installed before you arrive.
    Get the installer for your platform from [Docker's download page](https://docs.docker.com/get-started/get-docker/).

## What you do not need

- No ROS installation.
  No `apt`, no `rosdep`, no `/opt/ros`.
  If you already have one it will not be used.
  Do check your `.bashrc` for a `source /opt/ros/<distro>/setup.bash` line and turn it off for the workshop: it sets ROS variables in every terminal, and those can shadow the Pixi environment.
- No `sudo` or virtual machine for the local ROS exercises.
- No GPU for the local exercises through the cross-platform solve.
  Running the CUDA computation in [Exercise 1.9](exercises/01-ros-workspace.md#19-run-it-on-a-real-gpu) does need an NVIDIA GPU and a compatible driver; an Apple GPU cannot run CUDA.
  Use your own compatible Linux GPU machine or join the [Brev setup](brev.md) with the instructors to try it during the workshop.

## Bringing your own project

You are welcome to work on your own ROS workspace instead of the example.
Have it checked out and building the way you build it today, and bring your `package.xml` files.
See [Migrating from rosdep & colcon](reference/migration.md) for the path we will follow.

!!! tip "Something not working?"

    Check [Troubleshooting](reference/troubleshooting.md) first.
    Still stuck?
    Grab one of us at the start of the session, or ask in the `#pixi` channel on [Discord](https://discord.gg/kKV8ZxyzY4).
