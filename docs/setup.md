---
icon: lucide/download
---

# Before you start

<!-- TODO(content): verify every command on Linux, macOS and Windows before the conference. -->

Everything below runs at home on your own laptop. Doing it in advance means you spend the workshop
learning instead of downloading.

## 1. Install Pixi

=== "Linux & macOS"

    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
    ```

Open a new terminal and check the version. You need 0.73 or newer:

```bash
pixi --version
```

## 2. Get the workshop material

```bash
git clone https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi.git
cd roscon-2026-declarative-ros-workspaces-with-pixi
```

## 3. Warm up your cache

This downloads the ROS 2 packages you will need, so the exercises install from disk instead of over
conference Wi-Fi.

```bash
pixi install --manifest-path solutions/01-ros-workspace/pixi.toml
```

<!-- TODO(content): decide whether to prefetch solutions 02 and 03 too, and note the download size
     per platform once measured. -->

## 4. Check that it works

```bash
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

A window with a turtle should appear. Close it; you are ready.

## What you do not need

- No ROS installation. No `apt`, no `rosdep`, no `/opt/ros`. If you already have one it will not get
  in the way, and it will not be used.
- No `sudo`, no Docker, no virtual machine.
- No GPU. The CUDA parts of the workshop are declared and built without one; only running the result
  needs the hardware.

## Bringing your own project

You are welcome to work on your own ROS workspace instead of the example. Have it checked out and
building the way you build it today, and bring your `package.xml` files. See
[Migrating from rosdep & colcon](reference/migration.md) for the path we will follow.

!!! tip "Something not working?"

    Check [Troubleshooting](reference/troubleshooting.md) first. Still stuck? Grab one of us at the
    start of the session, or ask in the `#pixi` channel on
    [Discord](https://discord.gg/kKV8ZxyzY4).
