---
icon: lucide/cpu
---

# Using with CUDA machines

!!! abstract "30 minutes, presented"

    **Slides:** [Advanced package management](../slides/) &middot; **Followed by:** [Exercise 2](../exercises/02-ros-package.md)

    By the end of this block you should understand the difference between depending on a package and *being* one, and how Pixi decides whether your machine can run a CUDA build.


## What does one require to setup a CUDA-enabled ROS workspace?



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

Now go do [Exercise 2: Build a ROS package with Pixi](../exercises/02-ros-package.md).
