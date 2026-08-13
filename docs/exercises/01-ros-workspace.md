---
icon: lucide/play
---

# Exercise 1: Your first ROS 2 workspace

!!! plain "30 minutes, hands-on"

    **Work in:** `exercises/01-ros-workspace/` &middot; **Solution:** `solutions/01-ros-workspace/` &middot; **After:** [Pixi in 30 minutes](../explainers/pixi-introduction.md)

    **Goal:** a `pixi.toml` and `pixi.lock` that give you a running ROS 2 turtlesim, a custom node of your own, and the same workspace targeting two ROS distributions.

This page is a series of small exercises.
Each one lists what to do, and the commands are folded away in a solution underneath.
Try it on your own first, the [cheat sheet](../reference/cheatsheet.md) helps with the command names, and open the solution when you are stuck.

!!! warning "Work inside the workshop repository"

    The exercises build on packages that ship in this repository, so start from the right directory:

    ```bash
    cd exercises/01-ros-workspace
    ```

    There is a `src/turtle_dancer/` package in there already, but no `pixi.toml` yet.
    Creating it is the first exercise.

## 1.1 Initialize a workspace

!!! exercise "Your turn"

    1. Create a Pixi manifest in this directory, with the Pixi CLI.
    2. Open `pixi.toml` and check which platforms and channels a new workspace starts with.

??? success "Solution"

    ```bash
    # 1
    pixi init
    # 2: open pixi.toml in your editor
    ```

    Resulting `pixi.toml` file (the author and platform are read from your machine):

    ```toml title="exercises/01-ros-workspace/pixi.toml"
    [workspace]
    authors = ["Jane Doe <jane.doe@example.com>"]
    channels = ["conda-forge"]
    name = "01-ros-workspace"
    platforms = ["osx-arm64"]
    version = "0.1.0"

    [tasks]

    [dependencies]
    ```

## 1.2 Install ROS 2

ROS packages live on a RoboStack channel, not on `conda-forge`.
A channel works like an apt source, except it is written down in your manifest.

!!! exercise "Your turn"

    1. Add the `https://prefix.dev/robostack-jazzy` channel, at a higher priority than `conda-forge`.
       Hint: `pixi workspace channel add --help`.
    2. Add `ros-jazzy-ros-base` and `ros-jazzy-turtlesim` as dependencies.
    3. Check what actually landed in the environment.
    4. Prove ROS runs by listing its topics.
       Hint: any command runs inside the environment with `pixi run <command>`, or open a shell inside it with `pixi shell`.

??? success "Solution"

    ```bash
    # 1
    pixi workspace channel add --prepend https://prefix.dev/robostack-jazzy
    # 2
    pixi add ros-jazzy-ros-base ros-jazzy-turtlesim
    # 3
    pixi list
    # 4
    pixi run ros2 topic list
    # or from a shell inside the environment:
    pixi shell
    ros2 topic list
    ```

    A `pixi.lock` appeared next to the manifest.
    It records every package that step 2 resolved, and `pixi run` installs from it before running anything.

    Resulting `pixi.toml` file:

    ```toml title="exercises/01-ros-workspace/pixi.toml" hl_lines="3 11 12"
    [workspace]
    authors = ["Jane Doe <jane.doe@example.com>"]
    channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]
    name = "01-ros-workspace"
    platforms = ["osx-arm64"]
    version = "0.1.0"

    [tasks]

    [dependencies]
    ros-jazzy-ros-base = ">=0.11.0,<0.12"
    ros-jazzy-turtlesim = ">=1.8.3,<2"
    ```

## 1.3 Turn the commands into tasks

Commands you reuse get a name in the manifest, so your teammates run them without knowing the full incantation.

!!! exercise "Your turn"

    1. Add a task `sim` that runs `ros2 run turtlesim turtlesim_node`.
    2. Add a task `teleop` for `ros2 run turtlesim turtle_teleop_key`, and a task `topics` for `ros2 topic list`.
    3. Open two terminals and drive the turtle: the simulator in one, the teleop in the other.

??? success "Solution"

    ```bash
    # 1
    pixi task add sim "ros2 run turtlesim turtlesim_node"
    # 2
    pixi task add teleop "ros2 run turtlesim turtle_teleop_key"
    pixi task add topics "ros2 topic list"
    # 3: in two terminals
    pixi run sim        # a turtle appears
    pixi run teleop     # click this terminal, use the arrow keys
    ```

    Resulting `[tasks]` table:

    ```toml title="exercises/01-ros-workspace/pixi.toml"
    [tasks]
    sim = "ros2 run turtlesim turtlesim_node"
    teleop = "ros2 run turtlesim turtle_teleop_key"
    topics = "ros2 topic list"
    ```

## 1.4 Build your own node with colcon

`src/turtle_dancer/` is a small ROS 2 C++ package, written for you already.
Building it needs a toolchain and the ROS libraries it includes, and those come from the same channels as everything else.

!!! exercise "Your turn"

    1. Add `ros-dev-tools`: one package that brings colcon, CMake and the compilers.
       The ROS libraries the node uses are already there, `ros-jazzy-ros-base` includes them.
    2. Build the workspace with colcon.
    3. Try to run your node with `ros2 run turtle_dancer dance` and read the error.
    4. Fix it: make Pixi source the colcon overlay in `install/` whenever the environment activates.
       Hint: look up [`activation`](https://pixi.prefix.dev/latest/reference/pixi_manifest/#the-activation-table) in the Pixi documentation, and mind that the overlay's filename differs per platform.
    5. Add a `build` task, and a `dance` task that depends on it.
    6. Run the simulator in one terminal and your node in another.

??? success "Solution"

    ```bash
    # 1
    pixi add ros-dev-tools
    # 2
    pixi run colcon build
    # 3
    pixi run ros2 run turtle_dancer dance
    # Package 'turtle_dancer' not found
    ```

    That error is expected.
    colcon built the node into `install/`, and `ros2` only finds it once that overlay is sourced.
    You can source it by hand in every terminal, or let Pixi do it with an activation script that runs whenever the environment activates.

    4: the overlay has a different filename on Windows, so pick your platform:

    === "Unix (Linux, macOS)"

        ```toml title="exercises/01-ros-workspace/pixi.toml"
        [target.unix.activation]
        scripts = ["install/setup.sh"]
        ```

    === "Windows"

        ```toml title="exercises/01-ros-workspace/pixi.toml"
        [target.win-64.activation]
        scripts = ["install/setup.bat"]
        ```

    The script only exists after the first `colcon build`, so Pixi warns until then.

    ```bash
    # 5
    pixi task add build "colcon build"
    pixi task add dance "ros2 run turtle_dancer dance" --depends-on build
    # 6: in two terminals
    pixi run sim
    pixi run dance    # the turtle starts dancing
    ```

    Resulting `pixi.toml` file:

    ```toml title="exercises/01-ros-workspace/pixi.toml" hl_lines="12 13 18 20 21"
    [workspace]
    authors = ["Jane Doe <jane.doe@example.com>"]
    channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]
    name = "01-ros-workspace"
    platforms = ["osx-arm64"]
    version = "0.1.0"

    [tasks]
    sim = "ros2 run turtlesim turtlesim_node"
    teleop = "ros2 run turtlesim turtle_teleop_key"
    topics = "ros2 topic list"
    build = "colcon build"
    dance = { cmd = "ros2 run turtle_dancer dance", depends-on = ["build"] }

    [dependencies]
    ros-jazzy-ros-base = ">=0.11.0,<0.12"
    ros-jazzy-turtlesim = ">=1.8.3,<2"
    ros-dev-tools = ">=1.0.2,<2"

    [target.unix.activation]
    scripts = ["install/setup.sh"]
    ```

    colcon left `build/`, `install/` and `log/` directories behind, exactly as it does outside Pixi.

## 1.5 Two ROS distros, one workspace

A second ROS distribution is a second environment in the same manifest.
The tasks, the toolchain and the activation are shared; what differs per distro is the channel and the `ros-*` packages.
Those distro-specific pieces go into an environment of their own, declared inline.

!!! exercise "Your turn"

    1. Move the Jazzy pieces into their own environment: declare `[environments.default]` inline, holding the RoboStack channel and the `ros-jazzy` packages.
       The tasks, `ros-dev-tools` and the activation stay at workspace level.
    2. Add a `kilted` environment the same way, with the `robostack-kilted` channel and the `ros-kilted` variants of the packages.
    3. Run turtlesim from each distribution.
       Hint: `pixi run --environment` picks the environment, and the tasks are shared.

??? success "Solution"

    1: the workspace channel list goes back to `conda-forge` only, and the Jazzy channel and packages become the inline `default` environment:

    ```toml title="exercises/01-ros-workspace/pixi.toml"
    --8<-- "solutions/01-ros-workspace/pixi.toml:jazzy"
    ```

    2: the new environment is the same shape, with a different channel and package prefix:

    ```toml title="exercises/01-ros-workspace/pixi.toml"
    --8<-- "solutions/01-ros-workspace/pixi.toml:kilted"
    ```

    ```bash
    # 3
    pixi run sim               # turtlesim on Jazzy
    pixi run -e kilted sim     # the same task, on Kilted
    ```

    Everything at workspace level belongs to the default feature, and every environment includes it.
    That is why `sim` runs in both environments without being defined twice.

??? "The full `pixi.toml`"

    ```toml title="solutions/01-ros-workspace/pixi.toml"
    --8<-- "solutions/01-ros-workspace/pixi.toml"
    ```

## Check your work

```bash
pixi run topics           # ROS is alive
pixi run dance            # your node drives the turtle
pixi run -e kilted test   # ...and the same workspace runs a different distro
```

You should see a list of `/turtle1/...` topics, a dancing turtle, and `ros: kilted ok`.

## Going further

Finished early? Try these.

- Add a viewer with `pixi add ros-jazzy-rviz2`, then `pixi run rviz2`.
- Delete the `.pixi/` folder, run `pixi install`, and watch the environment rebuild from the lockfile.

!!! note "With your own workspace"

    Doing this on your own ROS project is the same steps.
    Run `pixi init` in the repo, add the `robostack-<your-distro>` channel, and add the `ros-<your-distro>-*` packages you depend on.
    Then get `colcon build` running inside the Pixi environment, like exercise 1.4.

---

Next: [CUDA](../explainers/cuda.md).
