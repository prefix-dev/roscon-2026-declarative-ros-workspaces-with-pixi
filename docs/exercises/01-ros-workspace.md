---
icon: lucide/play
---

# Exercise 1 — Your first ROS 2 workspace

!!! exercise "30 minutes, hands-on"

    **Work in:** `exercises/01-ros-workspace/` &middot;
    **Solution:** `solutions/01-ros-workspace/` &middot;
    **After:** [Pixi in 30 minutes](../explainers/pixi-introduction.md)

    **Goal:** a `pixi.toml` and `pixi.lock` that give you a running ROS 2 turtlesim on your laptop,
    with no ROS installed on the machine.

<!-- TODO(content): fill in the steps. Every command must be verified on Linux, macOS and Windows.
     Target: a comfortable 30 minutes, so roughly 4 steps with slack. -->

## Step 1 — Initialize a workspace

<!-- TODO(content): pixi init, look at the generated manifest, add the RoboStack channel.
     Explain channel order while they wait for nothing (this step is instant). -->

## Step 2 — Install ROS 2

<!-- TODO(content): pixi add ros-jazzy-ros-base ros-jazzy-turtlesim.
     While it downloads: show them pixi.lock, and `pixi list`.
     Then `pixi run ros2 topic list` — no sourcing, no /opt/ros. -->

## Step 3 — Turn the commands into tasks

<!-- TODO(content): [tasks] sim, teleop. depends-on. Why this replaces the team README. -->

## Step 4 — Make the turtle move

<!-- TODO(content): a small Python node in the workspace that publishes to /turtle1/cmd_vel,
     run via a task. Keep it plain `pixi run` — becoming a *package* is Exercise 2. -->

## Check your work

<!-- TODO(content): the one command that proves it, plus expected output. -->

```bash
pixi run sim
```

## Going further

<!-- TODO(content):
     - Add rviz2 and look at it.
     - Add a second environment without the GUI packages.
     - Delete .pixi/ and watch `pixi install` rebuild it from the lockfile.
-->

!!! note "With your own workspace"

    <!-- TODO(content): pixi init in an existing repo, add the channel, add the ROS distro
         metapackage that matches what they use today. -->

---

Next: [Packages, virtual packages & CUDA](../explainers/packaging-and-cuda.md).
