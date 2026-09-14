# Exercise 2: Build ROS packages with Pixi

This is where Exercise 1 left off, trimmed to Lyrical: colcon builds `src/turtle_dancer/`, and the overlay is sourced through an activation script.
The Kilted environment and the PyTorch node are left out on purpose, so the changes in this exercise are only about the build.
Run `pixi run build` once before `pixi run dance`, so activation can find `install/default/local_setup.*`.

`src/turtle_choreographer/` is a Python node, provided pre-written.
The initial colcon build skips it; you add it in the second half.

**Instructions:** [Exercise 2 on the workshop site](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/)

**Solution:** [`../../solutions/02-ros-package/`](../../solutions/02-ros-package/)
