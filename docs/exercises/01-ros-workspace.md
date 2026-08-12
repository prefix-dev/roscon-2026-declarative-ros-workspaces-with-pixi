---
icon: lucide/play
---

# Exercise 1: Your first ROS 2 workspace

!!! exercise "30 minutes, hands-on"

    **Work in:** `exercises/01-ros-workspace/` &middot; **Solution:** `solutions/01-ros-workspace/` &middot; **After:** [Pixi in 30 minutes](../explainers/pixi-introduction.md)

    **Goal:** a `pixi.toml` and `pixi.lock` that give you a running ROS 2 turtlesim, a custom node of your own, and the same workspace targeting two ROS distributions.

You are in `exercises/01-ros-workspace/`.
There is a `src/turtle_dancer/` package already, but no `pixi.toml` yet.
You create it in Step 1.
By the end you have ROS 2 running, your own node built, and the same workspace targeting two ROS distributions.

## Step 1: Initialize a workspace

Create the manifest right where you are:

```bash
pixi init
```

That writes a `pixi.toml` next to `src/`.
Open it: a `[workspace]` table with your current platform and `conda-forge` as the only channel.
That is enough here, you work on your own machine.
Declaring the other platforms so it runs everywhere is [Exercise 3](03-collaboration.md).

## Step 2: Install ROS 2

ROS packages live on a RoboStack channel, not on `conda-forge`.
Add it:

```bash
pixi workspace channel add robostack-jazzy
```

Now add ROS itself, plus turtlesim to have something to look at:

```bash
pixi add ros-jazzy-ros-base ros-jazzy-turtlesim
```

A `pixi.lock` appears next to the manifest.
Run `pixi list` to see what landed in the environment, then check that ROS runs:

```bash
pixi run ros2 topic list
```

## Step 3: Turn the commands into tasks

Give the commands you will reuse a name, in the manifest:

```bash
pixi task add sim "ros2 run turtlesim turtlesim_node"
pixi task add teleop "ros2 run turtlesim turtle_teleop_key"
pixi task add topics "ros2 topic list"
```

Now open two terminals and drive the turtle:

```bash
pixi run sim        # a turtle appears
pixi run teleop     # click this terminal, use the arrow keys
```

## Step 4: Build your own node with colcon

`src/turtle_dancer/` is a small ROS 2 C++ package, written for you already.
You do not have to type it, it is here so you have something to build.

Building it needs a toolchain and the ROS libraries it includes.
Add them:

```bash
pixi add ros-jazzy-rclcpp ros-jazzy-geometry-msgs \
         colcon-common-extensions cxx-compiler cmake ninja
```

Build the workspace:

```bash
pixi run colcon build
```

Now try to run your node:

```bash
pixi run ros2 run turtle_dancer dance
# Package 'turtle_dancer' not found
```

That is expected.
colcon built the node into `install/`, and `ros2` finds it once the colcon overlay is on your path.
You can source that overlay by hand every time, or let Pixi do it with an activation script that runs whenever the environment activates.

The overlay has a different filename on Windows, so pick your platform:

=== "Unix (Linux, macOS)"

    ```toml title="pixi.toml"
    [target.unix.activation]
    scripts = ["install/setup.sh"]
    ```

=== "Windows"

    ```toml title="pixi.toml"
    [target.win-64.activation]
    scripts = ["install/setup.bat"]
    ```

The script only exists after the first `colcon build`, so Pixi warns until then.
Wrap the build and the run into tasks:

```bash
pixi task add build "colcon build"
pixi task add dance "ros2 run turtle_dancer dance" --depends-on build
```

```bash
pixi run sim      # in one terminal
pixi run dance    # in another: the turtle starts dancing
```

colcon left `build/`, `install/`, and `log/` directories behind.
Exercise 2 hands the build to Pixi and the overlay activation goes away.

## Step 5: Two ROS distros, one workspace

To add a second ROS distribution, you wrap what you have in a feature, then add another one next to it.

A feature is a named bundle of channels and dependencies.
An environment is a combination of features that Pixi installs.
Move your Jazzy setup into a `[feature.jazzy]` block, then add a `[feature.kilted]` next to it.
The new feature is the same as Jazzy except for the channel and the `ros-kilted` package prefix.

```toml title="pixi.toml"
--8<-- "solutions/01-ros-workspace/pixi.toml:kilted"
```

Then declare which features make up which environment:

```toml title="pixi.toml"
--8<-- "solutions/01-ros-workspace/pixi.toml:environments"
```

Run each distro:

```bash
pixi run sim            # turtlesim on Jazzy
pixi run sim-kilted     # the same workspace, on Kilted
```

Your `pixi.toml` now has the same features, environments, and tasks as the solution.
The `-kilted` suffix on the tasks is only there because a task name that exists in two environments makes `pixi run <task>` ambiguous.

??? "The full `pixi.toml`"

    ```toml title="solutions/01-ros-workspace/pixi.toml"
    --8<-- "solutions/01-ros-workspace/pixi.toml"
    ```

## Check your work

```bash
pixi run topics          # ROS is alive
pixi run dance           # your node drives the turtle
pixi run test-kilted     # ...and the same workspace runs a different distro
```

You should see a list of `/turtle1/...` topics, a dancing turtle, and `ros: kilted ok`.

## Going further

Finished early? Try these.

- Add a viewer with `pixi add ros-jazzy-rviz2`, then `pixi run rviz2`.
- Delete the `.pixi/` folder, run `pixi install`, and watch the environment rebuild from the lockfile.

!!! note "With your own workspace"

    Doing this on your own ROS project is the same steps.
    Run `pixi init` in the repo, `pixi workspace channel add robostack-<your-distro>`, and add the `ros-<your-distro>-*` packages you depend on.
    Then get `colcon build` running inside the Pixi environment, like Step 4.
    This is where Exercise 2 picks up.

---

Next: [CUDA](../explainers/cuda.md).
