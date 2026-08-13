---
icon: lucide/rocket
---

# Declarative ROS workspaces with Pixi and RoboStack

A hands-on workshop for reproducible ROS development.

**ROSCon 2026, Tuesday, September 22nd, 08:00 &ndash; 12:00**

[Pixi](https://pixi.prefix.dev) is a fast, cross-platform package manager built on the conda ecosystem.
[RoboStack](https://robostack.github.io) provides the ROS 2 distribution as conda packages.
Together they let you declare your entire ROS environment (system libraries, Python packages and ROS nodes) in a single `pixi.toml`, with a lockfile that guarantees reproducibility.

!!! warning "Do this before you arrive"

    ROS is big and conference Wi-Fi is not.
    Follow [Before you start](setup.md) at home to install Pixi and warm up your package cache.
    It takes five minutes and saves you thirty.

## What you will do

- Set up a ROS 2 workspace from scratch using Pixi and RoboStack.
- Add NVIDIA GPU and CUDA support for accelerated ROS workloads.
- Target multiple platforms (Linux, macOS, Windows, ARM) from one project file.
- Learn team workflows with lockfiles, CI/CD and Docker.

You can work on the example workspace in this repository or bring your own.
By the end you will have a working Pixi-based ROS workspace and know how to migrate existing projects.
All experience levels are welcome.

## Schedule

<div class="schedule" markdown>

| Time | Block | Format |
| --- | --- | --- |
| 15 min | Welcome, introductions and [setup check](setup.md) | Together |
| 15 min | [Robotics for everyone](explainers/philosophy.md) | Presented |
| 30 min | [Pixi in 30 minutes](explainers/pixi-introduction.md) | Presented |
| 30 min | [Exercise 1: Your first ROS 2 workspace](exercises/01-ros-workspace.md) | Hands-on |
| 30 min | [CUDA](explainers/cuda.md) | Presented |
| 30 min | [Exercise 2: CUDA, PyTorch and a Jetson](exercises/02-ros-package.md) | Hands-on |
| 15 min | [Collaboration, CI/CD & Docker](explainers/collaboration.md) | Presented |
| 20 min | [Exercise 3: Ready for your team](exercises/03-collaboration.md) | Hands-on |

</div>

The explainers are presented from the [slides](slides/); this site holds the same material in written form so you can read ahead, catch up, or work through everything on your own afterwards.

## Your hosts

- **Wolf Vollprecht**, prefix.dev GmbH, Founder & CEO
- **Bas Zalmstra**, prefix.dev GmbH, Software Architect
- **Ruben Arts**, prefix.dev GmbH, Software Engineer

Found a mistake, or something that could be explained better?
Open an issue or a pull request on [GitHub](https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi).
The material stays online after the conference.
