---
icon: lucide/hammer
---

# Exercise 2: Build ROS packages with Pixi

!!! exercise "30 minutes, hands-on"

    **Work in:** `exercises/02-ros-package/` &middot; **Solution:** `solutions/02-ros-package/` &middot; **After:** [Pixi in 30 minutes](../explainers/pixi-introduction.md)

    **Goal:** hand the build to Pixi.
    The same C++ node from Exercise 1, plus a Python one, both built and installed from their `package.xml`: no `colcon build`, no `source install/setup.bash`, no `build/` directory.

<!-- TODO(content): fill in the steps. The subject is the *workflow*, not packaging internals.
     Wire things up quickly, then spend the time in the edit-run loop. -->

## Step 1: Let Pixi build the C++ package

<!-- TODO(content): add preview = ["pixi-build"], a src/turtle_dancer/pixi.toml with the
     pixi-build-ros backend, and the path dependency:

         ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }

     Note the name: the package.xml name with the RoboStack distro prefix. Nothing about the
     package itself changes: package.xml and CMakeLists.txt stay exactly as they were. -->

## Step 2: Delete the colcon machinery

<!-- TODO(content): remove the colcon build task and its toolchain, delete build/ install/ log/,
     then:

         $ pixi run ros2 run turtle_dancer dance

     No sourcing. This is the before/after that Exercise 1 set up, and it is the emotional centre of
     the workshop, so give it a moment. Verified working. -->

## Step 3: Live in the edit-run loop

<!-- TODO(content): THE point of this exercise. Change the angular speed in dance.cpp, `pixi run
     dance` again, watch the turtle turn differently. No build command in between.

     Then contrast explicitly with the Exercise 1 loop: edit, colcon build, re-source, run.

     WARNING: this does not work on pixi 0.73.0: a source-only edit does not trigger a rebuild, so
     you would be demonstrating stale code. See PIXI_IMPROVEMENTS.md finding 1; the fix is expected
     before the workshop, and `pixi run check-edit-run-loop` at the repo root guards it. Do not write
     this step until that check passes. -->

## Step 4: Add the Python package

<!-- TODO(content): src/turtle_choreographer is provided. Same treatment: a package pixi.toml with
     the backend, and a path dependency. One workspace, two languages, one lockfile.

     Mention setup.cfg and why it matters (install_scripts -> lib/<pkg>/, which is what lets
     `ros2 run` find a Python entry point). Every `ros2 pkg create --build-type ament_python`
     generates it; hand-written packages sometimes lack it. -->

## Check your work

```bash
pixi run dance          # C++ node, no sourcing
pixi run choreograph    # Python node
pixi run executables    # ros2 sees your node, exactly as after a colcon build
```

<!-- TODO(content): expected output for each. -->

## Going further

<!-- TODO(content):
     - `pixi build` and inspect the resulting .conda file.
     - Add a custom-interfaces package and depend on it from both nodes. Verified that rosidl
       generation works with this backend.
     - Compare the diff of this exercise against Exercise 1: count the lines and files removed.
-->

!!! note "With your own workspace"

    <!-- TODO(content): point pixi-build-ros at one leaf package from their repo and expect
         interesting failures. This is the highest-value ten minutes in the workshop for anyone with
         an existing project, so leave room to sit with people here. -->

---

Next: [Collaboration, CI/CD & Docker](../explainers/collaboration.md).
