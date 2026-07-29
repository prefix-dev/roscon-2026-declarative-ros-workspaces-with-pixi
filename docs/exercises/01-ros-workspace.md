---
icon: lucide/play
---

# Exercise 1 — Your first ROS 2 workspace

!!! exercise "30 minutes, hands-on"

    **Work in:** `exercises/01-ros-workspace/` &middot;
    **Solution:** `solutions/01-ros-workspace/` &middot;
    **After:** [Pixi in 30 minutes](../explainers/pixi-introduction.md)

    **Goal:** a `pixi.toml` and `pixi.lock` that give you a running ROS 2 turtlesim and a custom node
    of your own, with no ROS installed on the machine &mdash; and the same workspace targeting two ROS
    distributions at once.

<!-- TODO(content): fill in the steps. Budget is ~24 min of content in the 30 min slot; the C++ node
     is provided pre-written, which is what buys the slack. Verify every command on Linux, macOS and
     Windows. -->

## Step 1 — Initialize a workspace

<!-- TODO(content): pixi init, read the generated manifest, add the RoboStack channel.
     This step is instant, so it is the place to explain channel order while nothing is downloading. -->

## Step 2 — Install ROS 2

<!-- TODO(content): pixi add ros-jazzy-ros-base ros-jazzy-turtlesim.
     While it installs: show pixi.lock and `pixi list`.
     Then `pixi run ros2 topic list` — no sourcing, no /opt/ros, no sudo. -->

## Step 3 — Turn the commands into tasks

<!-- TODO(content): [tasks] sim and teleop. Run them in two terminals and drive the turtle.
     Point out that this replaces the paragraph of shell commands in every team README. -->

## Step 4 — Build your own node, the way you do it today

<!-- TODO(content): src/turtle_dancer is provided — read it, do not type it.
     Add colcon-common-extensions + cxx-compiler + cmake + ninja, then `colcon build`.

     Then the moment this exercise exists for:

         $ pixi run ros2 run turtle_dancer dance
         Package 'turtle_dancer' not found

     ...until you source install/setup.bash. Note the build/ install/ log/ directories that
     appeared. Exercise 2 deletes all of it. Verified: colcon build takes ~8s. -->

## Step 5 — Two ROS distros, one workspace

<!-- TODO(content): the payoff slide made real. A second feature with the robostack-kilted channel
     and ros-kilted-* packages, as its own environment:

         pixi run sim              # ROS_DISTRO=jazzy
         pixi run sim-kilted       # ROS_DISTRO=kilted

     Both installed, both working, switchable instantly. Show the diff between the two features:
     a channel and a package prefix, nothing else. That is what a distro migration costs here.

     Prefetched at home, so this step does not download anything in the room. -->

## Check your work

```bash
pixi run topics          # ROS is alive
pixi run dance           # your node drives the turtle
pixi run test-kilted     # ...and the same workspace runs a different distro
```

<!-- TODO(content): show the expected output of each. -->

## Going further

<!-- TODO(content):
     - Add rviz2 and look at it.
     - Delete .pixi/ and watch `pixi install` rebuild it from the lockfile.
     - `pixi list --platform win-64` — what your colleague on Windows would get.
-->

!!! note "With your own workspace"

    <!-- TODO(content): pixi init in an existing repo, add the RoboStack channel for the distro they
         use today, and get colcon building inside the Pixi environment. That alone is a shippable
         first step for a team, and it is exactly where Exercise 2 picks up. -->

---

Next: [Packages, virtual packages & CUDA](../explainers/packaging-and-cuda.md).
