---
icon: lucide/rocket
---

# Declarative ROS workspaces with Pixi and RoboStack

A hands-on workshop for reproducible ROS development.

**ROSCon 2026, Tuesday, September 22nd, 08:00 &ndash; 12:00**

!!! note "Work in progress"

    This material is under active development until the workshop.
    Expect the exercises, the solutions and this site to change, and run `git pull` again before you come.

[Pixi](https://pixi.prefix.dev) is a fast, cross-platform package manager built on the conda ecosystem.
[RoboStack](https://robostack.github.io) provides the ROS 2 distribution as conda packages.
Together they let you declare your entire ROS environment (system libraries, Python packages and ROS nodes) in a single `pixi.toml`, with a lockfile that guarantees reproducibility.

!!! warning "Do this before you arrive"

    ROS is big and conference Wi-Fi is not.
    Follow [Before you start](setup.md) at home to install Pixi and warm up your package cache.
    It takes five minutes and saves you thirty.
    If your laptop or the room network cannot keep up, we have a separate [Brev fallback setup](brev.md).

## What you will do

- Set up a ROS 2 workspace from scratch with Pixi and RoboStack, and run two ROS distros side by side.
- Give the turtle a PyTorch brain: add CUDA support and solve for a GPU box and a Jetson from your own laptop.
- Build your own ROS packages with Pixi, no colcon, no sourcing.
- Make it team-ready: one lockfile for Linux, macOS and Windows, CI in two lines, and a Docker image with no Pixi inside.

You can work on the example workspace in this repository or bring your own.
By the end your workspace runs on any machine with three commands: `git clone`, `cd`, `pixi run`.
All experience levels are welcome.

## Schedule

<div class="schedule" markdown>

| Time | Block | Format |
| --- | --- | --- |
| 15 min | Welcome, introductions and [setup check](setup.md) | Together |
| 15 min | [Robotics for everyone](explainers/philosophy.md) | We talk |
| 30 min | [Pixi in 30 minutes](explainers/pixi-introduction.md) and [CUDA](explainers/cuda.md) | We talk |
| 30 min | [Exercise 1: Your first ROS 2 workspace](exercises/01-ros-workspace.md) | You type |
| 15 min | Building ROS packages with Pixi | We talk |
| 30 min | [Exercise 2: Build ROS packages with Pixi](exercises/02-ros-package.md) | You type |
| 15 min | [Collaboration, CI/CD & Docker](explainers/collaboration.md) | We talk |
| 20 min | [Exercise 3: Ready for your team](exercises/03-collaboration.md) | You type |

</div>

The explainers are presented from the [slides](slides/); this site holds the same material in written form so you can read ahead, catch up, or work through everything on your own afterwards.

## Your hosts

- **Wolf Vollprecht**, prefix.dev GmbH, Founder & CEO
- **Bas Zalmstra**, prefix.dev GmbH, Software Architect
- **Ruben Arts**, prefix.dev GmbH, Software Engineer

Found a mistake, or something that could be explained better?
Open an issue or a pull request on [GitHub](https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi).
The material stays online after the conference.
