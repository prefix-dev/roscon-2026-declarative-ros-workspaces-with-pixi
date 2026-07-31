---
icon: lucide/arrow-right-left
---

# Migrating from rosdep & colcon

<!-- TODO(content): this is the page people send to their team after the conference. It should read
     as a standalone document, not as workshop notes. -->

## What maps to what

<!-- TODO(content): a table. rosdep install -> pixi install, colcon build -> pixi build,
     source install/setup.bash -> nothing, apt -> conda channels, .rosinstall/vcs -> path or git
     dependencies. Be honest where there is no clean mapping. -->

## A migration order that works

<!-- TODO(content): the low-risk sequence:
     1. Pixi for the tooling only, ROS still from apt.
     2. ROS from RoboStack, colcon still building your packages.
     3. Your packages built by Pixi.
     4. Multi-platform.
     Each step is independently shippable and revertible. -->

## What you keep

<!-- TODO(content): package.xml stays the source of truth. Your CMakeLists stay. Your launch files
     stay. -->

## What you give up

<!-- TODO(content): be straight about it: packages not yet in RoboStack, apt-only vendor drivers,
     the parts of the ROS tooling that assume /opt/ros. And what to do about each. -->

## Deploying to a robot

<!-- TODO(content): pixi on the device, pixi-pack for offline, Docker. Pick a recommendation. -->

## Getting help

- [Pixi documentation](https://pixi.prefix.dev)
- [RoboStack](https://robostack.github.io) and its [GitHub organisation](https://github.com/RoboStack)
- The `#pixi` channel on [Discord](https://discord.gg/kKV8ZxyzY4)
- Missing a package in RoboStack?
  It is a pull request, and we will help you write it.
