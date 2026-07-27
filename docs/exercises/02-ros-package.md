---
icon: lucide/hammer
---

# Exercise 2 — Build a ROS package with Pixi

!!! exercise "30 minutes, hands-on"

    **Work in:** `exercises/02-ros-package/` &middot;
    **Solution:** `solutions/02-ros-package/` &middot;
    **After:** [Packages, virtual packages & CUDA](../explainers/packaging-and-cuda.md)

    **Goal:** the same turtle-driving node, but built by Pixi as a real ROS package from its
    `package.xml` &mdash; and a CUDA-enabled variant that only applies where a GPU exists.

<!-- TODO(content): fill in the steps. This is the exercise most likely to overrun; make Step 4
     clearly optional. -->

## Step 1 — Look at what you have

<!-- TODO(content): walk the provided src/turtle_dancer: package.xml, setup.py, the node.
     Point out that the dependencies are already declared — in package.xml, not in pixi.toml. -->

## Step 2 — Make it a Pixi package

<!-- TODO(content): enable preview = ["pixi-build"], add [package] + [package.build] with
     pixi-build-ros, add it as a path dependency of the workspace. Show that package.xml
     <depend> entries become real solver dependencies. -->

## Step 3 — Build and run it

<!-- TODO(content): pixi run the node by its ROS entry point. Edit the source, run again,
     show what rebuilds and what does not. -->

## Step 4 — Add CUDA support

<!-- TODO(content): a [feature.cuda] with system-requirements.cuda, restricted to linux-64 and
     linux-aarch64, plus an environment that uses it. Must be doable without a GPU: the check is
     that it solves and builds, not that it runs. -->

## Check your work

<!-- TODO(content): the command that proves the package was built by Pixi and not by colcon. -->

## Going further

<!-- TODO(content):
     - A second package in the same workspace that depends on the first.
     - A C++ package with pixi-build-cmake alongside the Python one.
     - `pixi build` and inspect the resulting .conda file.
-->

!!! note "With your own workspace"

    <!-- TODO(content): pick one leaf package from their repo, point pixi-build-ros at it,
         and expect the interesting failures — this is the highest-value 10 minutes in the
         workshop for people with an existing project. -->

---

Next: [Collaboration, CI/CD & Docker](../explainers/collaboration.md).
