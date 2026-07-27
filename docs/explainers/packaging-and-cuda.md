---
icon: lucide/cpu
---

# Packages, virtual packages & CUDA

!!! abstract "30 minutes, presented"

    **Slides:** [Advanced package management](../slides/) &middot;
    **Followed by:** [Exercise 2](../exercises/02-ros-package.md)

    By the end of this block you should understand the difference between depending on a package and
    *being* one, and how Pixi decides whether your machine can run a CUDA build.

<!-- TODO(content): 30 min. This is the densest block; cut ruthlessly if the room is behind
     schedule, because Exercise 2 is where it lands. -->

## What is in a conda package

<!-- TODO(content):
     - Anatomy: files, index.json, run/host/build dependencies, run_exports.
     - Why relocatable prefixes matter and how they are patched.
     - How a ROS package becomes ros-<distro>-<name>.
-->

## Your workspace as a package

<!-- TODO(content):
     - `[package]` next to `[workspace]`, and the `pixi-build` preview feature.
     - Build backends: pixi-build-cmake, pixi-build-python, pixi-build-ros.
     - What pixi-build-ros reads out of package.xml, and what it maps to.
     - Source dependencies: `{ path = "src/..." }`, and why editable-by-default matters.
     - `pixi build` vs `pixi install`: when a rebuild is triggered.
-->

## Virtual packages

<!-- TODO(content):
     - What a virtual package is: `__linux`, `__glibc`, `__cuda`, `__osx`, `__archspec`.
     - `pixi info` to read what your machine reports.
     - `[system-requirements]`: overriding what the solver may assume.
     - The two failure modes: solving for a machine you do not have, and refusing to solve for one
       you do.
-->

## CUDA in practice

<!-- TODO(content):
     - The CUDA packages on conda-forge: cuda-version, cuda-toolkit, cudart, and the -dev split.
     - Declaring `system-requirements.cuda` and what it does to the solve.
     - Building a CUDA-enabled node without a GPU in the machine that builds it.
     - A CUDA feature that only applies to linux-64 and linux-aarch64.
-->

## Takeaways

<!-- TODO(content): three bullets. -->

---

Now go do [Exercise 2 &mdash; Build a ROS package with Pixi](../exercises/02-ros-package.md).
