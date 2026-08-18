---
icon: lucide/hammer
---

# Exercise 2: Build ROS packages with Pixi

!!! plain "30 minutes, hands-on"

    **Work in:** `exercises/02-ros-package/` &middot; **Solution:** `solutions/02-ros-package/` &middot; **After:** [CUDA](../explainers/cuda.md)

    **Goal:** hand the build to Pixi.
    The same C++ node from Exercise 1, plus a Python one, both built and installed from their `package.xml`: no `colcon build`, no `source install/setup.bash`, no `build/` directory.

Exercise 1 built your node the ROS way: colcon in the workspace, an `install/` overlay, and sourcing before every run.
Pixi can build the package itself and put it in the environment next to `turtlesim`, so none of that is needed anymore: no colcon, no overlay, no sourcing, not even the build tools in your workspace.
This exercise gets you there one piece at a time, until what is left is edit and run.

Same format as before: each step says what to do, the commands are folded away underneath, and the [cheat sheet](../reference/cheatsheet.md) helps with the flags.

!!! warning "Work inside the workshop repository"

    ```bash
    cd exercises/02-ros-package
    ```

    This is where Exercise 1 left off, trimmed to Jazzy only: `pixi.toml` builds `src/turtle_dancer/` with `colcon` and sources the overlay on activation.
    The Kilted environment and the PyTorch node are left out so the diff in this exercise stays about the build.

    Run the colcon way once, so you have the before in front of you:

    ```bash
    pixi run dance      # colcon builds, then the node starts; Ctrl-C to stop
    ls                  # build/ install/ log/ appeared next to src/
    ```

## 2.1 Turn on Pixi build

Building packages from source is a [preview feature](https://pixi.prefix.dev/latest/reference/pixi_manifest/#preview-features) in Pixi, so a workspace opts in.
It also needs a [build backend](https://pixi.prefix.dev/latest/build/backends/), the piece that knows the build system.
For ROS that is [`pixi-build-ros`](https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/), and since every package in the workspace uses the same one, you declare it once, in [`[workspace.dependencies]`](https://pixi.prefix.dev/latest/build/workspace_dependencies/).

!!! exercise "Your turn"

    1. Enable the `pixi-build` preview in the `[workspace]` table.
    2. Add `pixi-build-ros = ">=0.7.2"` to `[workspace.dependencies]`.
       There is no CLI command for either, edit `pixi.toml`.

??? success "Solution"

    ```toml title="exercises/02-ros-package/pixi.toml" hl_lines="6 8 9"
    [workspace]
    name = "02-ros-package"
    channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]
    platforms = ["linux-64", "osx-arm64", "win-64"]
    version = "0.1.0"
    preview = ["pixi-build"]

    [workspace.dependencies]
    pixi-build-ros = ">=0.7.2"
    ```

    `[workspace.dependencies]` is a pool of shared specs, not an install list: nothing lands in the environment because of it.
    Packages pick entries out of the pool, which is the next step, and bumping the backend version later is one line.

## 2.2 Give the package a manifest

Until now every `pixi.toml` you wrote had a `[workspace]` table.
There is a second main table which describes a single package:

| Manifest role | Marked by | Describes | In this exercise |
| --- | --- | --- | --- |
| **Workspace** | `[workspace]` | your environment: channels, platforms, dependencies, tasks | `pixi.toml` |
| **Package** | `[package]` | how to build one package | `src/turtle_dancer/pixi.toml` |

A workspace is what you `pixi run`.
A package is what Pixi turns into a conda package, through the backend.
`pixi-build-ros` reads `package.xml` for the name, version, dependencies and build type, maps the dependencies to their RoboStack names, and runs the `ament_cmake` or `ament_python` build you already have.
So the package manifest has very little to say.

!!! exercise "Your turn"

    1. Create `src/turtle_dancer/pixi.toml` that names `pixi-build-ros` as its build backend, taking the version from the workspace pool.
       Hint: `workspace = true`.
    2. Open `package.xml` and `CMakeLists.txt`.
       Which lines does the backend need, and which one makes `ros2 run` find the executable?
       Change nothing.

??? success "Solution"

    ```toml title="exercises/02-ros-package/src/turtle_dancer/pixi.toml"
    --8<-- "solutions/02-ros-package/src/turtle_dancer/pixi.toml"
    ```

    Two lines: which backend, and "the version is in the workspace pool".
    The ROS distro comes from the `robostack-jazzy` channel of the workspace, and everything else comes from `package.xml`.

    From `package.xml` the backend takes `<name>`, `<version>`, `<depend>` and `<build_type>`.
    From `CMakeLists.txt` the line that matters is `install(TARGETS dance DESTINATION lib/${PROJECT_NAME})`: `ros2 run` looks in `lib/<package>/`, and that is where the backend installs whatever your CMake installs.
    Both files are the ones colcon used a minute ago, unchanged.

## 2.3 Depend on your own package

A workspace depends on a local package like on anything else, except the specifier is a `path` to the package directory.
The dependency name is the `package.xml` name with the distro prefix and hyphens: `ros-jazzy-turtle-dancer`, the name RoboStack would give it if it were published there.

!!! exercise "Your turn"

    1. Add `ros-jazzy-turtle-dancer` as a path dependency on `src/turtle_dancer`.
       `pixi add` does not write path dependencies, edit `[dependencies]` by hand.
    2. Install, and watch what happens.
    3. Find your package in `pixi list`.

??? success "Solution"

    ```toml title="exercises/02-ros-package/pixi.toml" hl_lines="2"
    [dependencies]
    ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }
    ros-jazzy-ros-base = ">=0.11"
    ros-jazzy-turtlesim = ">=1.8"
    ros-dev-tools = ">=1.0"
    ```

    ```bash
    # 2
    pixi install
    ```

    A `Running build for recipe: ros-jazzy-turtle-dancer-0.1.0-...` block scrolls by.
    The first install fetches the backend and a build environment (CMake, the compilers, the ROS libraries from `package.xml`) into `.pixi/bld/`, compiles the node and installs the result into the environment as a conda package.
    Later builds are incremental.

    ```console
    $ pixi list | grep turtle          # 3
    ros-jazzy-turtle-dancer                                       conda  src/turtle_dancer
    ros-jazzy-turtlesim   1.8.3   np2py312hd441986_18   669.96 KiB   conda  https://prefix.dev/robostack-jazzy
    ```

    Where other packages show a channel, yours shows the path it was built from.
    On Windows, `findstr turtle` instead of `grep turtle`.

## 2.4 Delete the colcon machinery

Right now the node is in the environment twice: once in colcon's `install/`, once built by Pixi.
Everything colcon needed can go.

!!! exercise "Your turn"

    1. Remove the `build` task, the `depends-on` of `dance`, the `ros-dev-tools` dependency and both `activation` tables.
    2. Delete `build/`, `install/` and `log/`.
    3. Run the node.
       In a second terminal, run the simulator and watch it go.

??? success "Solution"

    ```bash
    # 1
    pixi task remove build
    pixi remove ros-dev-tools
    # ...then in your editor: drop `depends-on` from dance, and delete both [target.*.activation] tables
    # 2 (PowerShell: Remove-Item -Recurse build, install, log)
    rm -rf build install log
    # 3, in two terminals
    pixi run sim
    pixi run dance
    ```

    Resulting `pixi.toml`:

    ```toml title="exercises/02-ros-package/pixi.toml"
    [workspace]
    name = "02-ros-package"
    channels = ["https://prefix.dev/robostack-jazzy", "conda-forge"]
    platforms = ["linux-64", "osx-arm64", "win-64"]
    version = "0.1.0"
    preview = ["pixi-build"]

    [workspace.dependencies]
    pixi-build-ros = ">=0.7.2"

    [dependencies]
    ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }
    ros-jazzy-ros-base = ">=0.11"
    ros-jazzy-turtlesim = ">=1.8"

    [tasks]
    sim = "ros2 run turtlesim turtlesim_node"
    teleop = "ros2 run turtlesim turtle_teleop_key"
    topics = "ros2 topic list"
    dance = "ros2 run turtle_dancer dance"
    ```

    `pixi run ros2 run turtle_dancer dance` works as well, from a fresh terminal, with nothing sourced.
    The node is a package in the environment now, the same as `turtlesim`.

## 2.5 Live in the edit-run loop

In Exercise 1 a change to the node meant edit, `pixi run build`, run, with the sourcing hidden in an activation script.
See what it means now.

!!! exercise "Your turn"

    1. Open `src/turtle_dancer/src/dance.cpp` and change the default angular speed from `0.8` to `3.0`.
    2. Run the node again, with the simulator still open.
    3. There was no build command in between.
       How did the new speed get in?

??? success "Solution"

    ```cpp title="src/turtle_dancer/src/dance.cpp"
    angular_speed_ = declare_parameter("angular_speed", 3.0);
    ```

    ```bash
    # 2
    pixi run dance      # the build output scrolls by, then the turtle turns in tight circles
    ```

    3: `pixi run` checks the inputs of every source dependency before it runs anything: `package.xml`, `CMakeLists.txt`, the source files.
    One of them changed, so the package was rebuilt and reinstalled first.
    Change it back to `0.8` and run again: same thing, the other way.

    !!! note "What counts as an input"

        The backend watches C and C++ sources, `package.xml`, `CMakeLists.txt`, `setup.py`, launch files, messages and a few more by default.
        Anything else goes in `extra-input-globs` under `[package.build.config]` in the package manifest.

## 2.6 Add the Python package

`src/turtle_choreographer/` is a second node, in Python this time, an `ament_python` package provided pre-written.
It gets the same treatment: a package manifest, a path dependency, a task.

!!! exercise "Your turn"

    1. Create `src/turtle_choreographer/pixi.toml`: the same two lines as the C++ one.
    2. Add `ros-jazzy-turtle-choreographer` as a path dependency.
    3. Add a `choreograph` task that runs `ros2 run turtle_choreographer choreograph`.
    4. Run it, with the simulator open.

??? success "Solution"

    ```toml title="exercises/02-ros-package/src/turtle_choreographer/pixi.toml"
    --8<-- "solutions/02-ros-package/src/turtle_choreographer/pixi.toml"
    ```

    ```toml title="exercises/02-ros-package/pixi.toml"
    --8<-- "solutions/02-ros-package/pixi.toml:dependencies"
    ```

    ```bash
    # 3
    pixi task add choreograph "ros2 run turtle_choreographer choreograph"
    # 4
    pixi run choreograph     # the turtle draws a figure of eight
    ```

    One workspace, two languages, one lockfile.

    !!! note "Editing the Python node"

        `pixi-build-ros` 0.7.2 does not have `**/*.py` in its default inputs, so an edit to `choreograph.py` alone does not trigger a rebuild yet.
        Until the next backend release, add this to the package manifest if you want the loop from 2.5 for the Python node too:

        ```toml title="src/turtle_choreographer/pixi.toml"
        [package.build.config]
        extra-input-globs = ["**/*.py"]
        ```

    !!! note "`setup.cfg` is what makes `ros2 run` find a Python node"

        Have a look at `src/turtle_choreographer/setup.cfg`: `install_scripts=$base/lib/turtle_choreographer`.
        That puts the entry point in `lib/<package>/`, where `ros2 run` looks, instead of `bin/`.
        `ros2 pkg create --build-type ament_python` generates this file for you.
        Hand-written packages sometimes lack it; the backend then fills in the same default, but it is better to have the file.

??? "The full `pixi.toml`"

    ```toml title="solutions/02-ros-package/pixi.toml"
    --8<-- "solutions/02-ros-package/pixi.toml"
    ```

## Check your work

```bash
pixi run dance          # C++ node, no sourcing
pixi run choreograph    # Python node
pixi run executables    # ros2 sees both nodes, exactly as after a colcon build
ls                      # src/ and pixi.toml, no build/ install/ log/
```

`executables` is one more task to add: `ros2 pkg executables turtle_dancer && ros2 pkg executables turtle_choreographer`.
It should print:

```text
turtle_dancer dance
turtle_choreographer choreograph
```

## Going further

Finished early? Try these.

- Compare what you started with against what you have: `git diff --stat exercises/02-ros-package/pixi.toml`.
- Build a real package: `pixi publish --path src/turtle_dancer --target-dir output` leaves a `.conda` file in `output/`.
  That is the same kind of file RoboStack serves; another workspace can `pixi add` it, and Exercise 3 shows what uploading it to a channel looks like.
- Trim the workspace: replace `ros-jazzy-ros-base` with `ros-jazzy-ros2run`.
  Everything the nodes need comes through their `package.xml` now, so `pixi list` gets a lot shorter.
- Add a third package with a custom `.msg`, and use it from both nodes.
  Interface generation works through this backend.

!!! note "With your own workspace"

    Pick one leaf package from your repository, one that does not depend on your other packages.
    Put the two-table `pixi.toml` from 2.2 next to its `package.xml`, add the path dependency, `pixi install`.
    Expect it to fail the first time, and read the error: usually a `package.xml` dependency that is not on RoboStack under that name, which `extra-package-mappings` in the backend config fixes, or one that is not packaged at all.
    This is the ten minutes of the workshop we most want to spend with you, so raise a hand.

---

Next: [Collaboration, CI/CD & Docker](../explainers/collaboration.md).
