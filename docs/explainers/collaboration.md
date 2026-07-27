---
icon: lucide/users
---

# Collaboration, CI/CD & Docker

!!! abstract "15 minutes, presented"

    **Slides:** [Prepare for collaboration](../slides/) &middot;
    **Followed by:** [Exercise 3](../exercises/03-collaboration.md)

    By the end of this block you should know what changes when the workspace stops being yours and
    starts being your team's.

<!-- TODO(content): 15 min. Fastest block; the exercise does the heavy lifting. -->

## Many platforms, one manifest

<!-- TODO(content):
     - Adding platforms and what it does to the lockfile.
     - Per-platform dependencies and tasks.
     - Handling a package that simply does not exist for a platform.
     - What "it solved" does and does not prove.
-->

## Jetson and other robots

<!-- TODO(content):
     - linux-aarch64 vs. the Jetson's CUDA and L4T reality.
     - `[system-requirements]` for the robot, not for the laptop.
     - Cross-solving on your laptop for hardware you do not have in front of you.
     - Shipping to the robot: pixi on device, or `pixi-pack`.
-->

## CI/CD

<!-- TODO(content):
     - setup-pixi: caching, environments, frozen installs.
     - Matrix over platforms, and what to run on each.
     - `pixi lock --check` as the "did you commit the lockfile" gate.
     - Publishing built packages to a channel on prefix.dev.
-->

## Docker

<!-- TODO(content):
     - The pixi Docker pattern: install into the image, ship the environment.
     - Multi-stage with pixi-pack to keep images small.
     - Why the same lockfile in the image and on the laptop is the whole point.
-->

## Takeaways

<!-- TODO(content): three bullets, then hand over to the exercise. -->

---

Now go do [Exercise 3 &mdash; Ready for your team](../exercises/03-collaboration.md).
