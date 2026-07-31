---
icon: lucide/box
---

# Pixi in 30 minutes

!!! abstract "30 minutes, presented"

    **Slides:** [Pixi introduction](../slides/) &middot; **Followed by:** [Exercise 1](../exercises/01-ros-workspace.md)

    By the end of this block you should be able to read a `pixi.toml`, know which command to reach for, and know where the lockfile fits in.

<!-- TODO(content): 30 min. Everything here should be something Exercise 1 immediately uses.
     Resist adding features the exercise does not touch. -->

## What is Pixi

<!-- TODO(content):
     - One workspace = one manifest + one lockfile.
     - conda and PyPI packages side by side.
     - No global state: everything lives in .pixi/ next to the manifest.
     - Where it sits next to conda, mamba, uv, poetry, apt.
-->

## Why it makes sense for robotics

<!-- TODO(content):
     - Binary C++ dependencies without compiling them yourself.
     - One manifest covering the laptop, the CI runner and the robot.
     - Tasks instead of a README full of shell snippets.
     - No sourcing setup.bash.
-->

## The features you will actually use

<!-- TODO(content): a short tour, each with a snippet. Order matches the exercise.
     - `[dependencies]` and version specs.
     - `[tasks]`: depends-on, cwd, args, inputs/outputs caching.
     - `[feature]` + `[environments]`: dev / sim / deploy / cuda.
     - `[target.<platform>]` overrides.
     - `pixi shell` vs `pixi run`.
     - `pixi.lock`: what is in it, why it is committed, what changes it.
-->

## How to set up a workspace

<!-- TODO(content): the exact flow the exercise follows, so the room has seen it once already.
     pixi init -> pixi workspace channel add -> pixi add -> pixi run.
-->

## Takeaways

<!-- TODO(content): the three commands and the one file people should remember. -->

---

Now go do [Exercise 1: Your first ROS 2 workspace](../exercises/01-ros-workspace.md).
