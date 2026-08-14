---
icon: lucide/download
---

# Before you start

<!-- TODO(content): verify every command on Linux, macOS and Windows before the conference. -->

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
You need 0.73 or newer:

```bash
pixi --version
```

## 2. Get the workshop material

```bash
git clone https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi.git
cd roscon-2026-declarative-ros-workspaces-with-pixi
```

## 3. Warm up your cache

!!! warning "This is the step that matters"

    The exercises use two ROS distributions.
    Downloading them at home means the workshop installs from your disk instead of over conference Wi-Fi.
    Expect this to take a while and to use a couple of GB.
    Run it the evening before, not on the morning of.

```bash
pixi install --all --manifest-path solutions/01-ros-workspace/pixi.toml
```

`--all` is what fetches both the Jazzy and the Kilted environments.

<!-- TODO(content): state the measured download size per platform after a dry run. Installed size is
     ~1.7 GB per distro on osx-arm64; the compressed download is smaller and the two distros share
     their conda-forge dependencies, so the incremental cost of the second is well under 2x.
     Measure it properly and put a real number here. -->

<!-- TODO(logistics): decide what happens for attendees who arrive without having done this.
     Tracked in IMPLEMENTATION_PLAN.md Stage 5. -->

## 4. Check that it works

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

A window with a turtle should appear.
Close it, then check the second distro too:

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml -e kilted test
```

If both worked, you are ready.

## What you do not need

- No ROS installation.
  No `apt`, no `rosdep`, no `/opt/ros`.
  If you already have one it will not be used.
  Do check your `.bashrc` for a `source /opt/ros/<distro>/setup.bash` line and turn it off for the workshop: it sets ROS variables in every terminal, and those can shadow the Pixi environment.
- No `sudo`, no Docker, no virtual machine.
- No GPU.
  The CUDA parts of the workshop are declared and built without one; only running the result needs the hardware.

## Bringing your own project

You are welcome to work on your own ROS workspace instead of the example.
Have it checked out and building the way you build it today, and bring your `package.xml` files.
See [Migrating from rosdep & colcon](reference/migration.md) for the path we will follow.

!!! tip "Something not working?"

    Check [Troubleshooting](reference/troubleshooting.md) first.
    Still stuck?
    Grab one of us at the start of the session, or ask in the `#pixi` channel on [Discord](https://discord.gg/kKV8ZxyzY4).
