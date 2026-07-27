---
theme: default
title: Declarative ROS workspaces with Pixi and RoboStack
info: |
  ROSCon 2026 — Tuesday, September 22nd, 08:00–12:00
  A hands-on workshop for reproducible ROS development.

  Ruben Arts, Wolf Vollprecht, Bas Zalmstra — prefix.dev
class: text-center
colorSchema: light
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
mdc: true
---

# Declarative ROS workspaces with Pixi and RoboStack

A hands-on workshop for reproducible ROS development

ROSCon 2026 · Ruben Arts, Wolf Vollprecht, Bas Zalmstra · prefix.dev

<!--
Presenter notes live in comments like this one.

Structure of this deck: one `section:` per agenda block, so the footer always shows where we are.
Each section ends with a slide that hands over to an exercise.
-->

---
layout: intro
section: Welcome
---

# Who we are

<!-- TODO(content): 15 min block — three short intros and the setup check. -->

- **Ruben Arts** — prefix.dev
- **Wolf Vollprecht** — prefix.dev
- **Bas Zalmstra** — prefix.dev

---
section: Welcome
---

# Today

| | | |
| --- | --- | --- |
| 15 min | Welcome and setup | together |
| 15 min | Why reproducibility matters | we talk |
| 30 min | Pixi in 30 minutes | we talk |
| 30 min | **Exercise 1** — your first ROS 2 workspace | you type |
| 30 min | Packages, virtual packages & CUDA | we talk |
| 30 min | **Exercise 2** — build a ROS package with Pixi | you type |
| 15 min | Collaboration, CI/CD & Docker | we talk |
| 20 min | **Exercise 3** — ready for your team | you type |

Everything is written up at
**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi**

---
section: Welcome
layout: center
---

# Before we start

<!-- TODO(content): the QR code to the site, and the one command that proves their setup works. -->

---
section: Philosophy
layout: section
---

# Why reproducibility matters

<!-- TODO(content): 15 min. See docs/explainers/philosophy.md for the outline. -->

---
section: Philosophy
---

# Reproducible package management

<!-- TODO(content) -->

---
section: Philosophy
---

# Development workflows

<!-- TODO(content) -->

---
section: Philosophy
---

# Avoiding OS lock-in

<!-- TODO(content) -->

---
section: Philosophy
---

# conda-forge + RoboStack

<!-- TODO(content) -->

---
section: Pixi
layout: section
---

# Pixi in 30 minutes

<!-- TODO(content): 30 min. See docs/explainers/pixi-introduction.md for the outline. -->

---
section: Pixi
---

# What is Pixi

<!-- TODO(content) -->

---
section: Pixi
---

# Why it makes sense for robotics

<!-- TODO(content) -->

---
section: Pixi
---

# The features you will actually use

<!-- TODO(content) -->

---
section: Pixi
---

# How to set up a workspace

<!-- TODO(content) -->

---
section: Exercise 1
layout: center
class: text-center
---

# Exercise 1

## Your first ROS 2 workspace

30 minutes · `exercises/01-ros-workspace/`

<!-- TODO(content): the URL and the four steps, big enough to read from the back of the room. -->

---
section: Packaging
layout: section
---

# Packages, virtual packages & CUDA

<!-- TODO(content): 30 min. See docs/explainers/packaging-and-cuda.md for the outline. -->

---
section: Packaging
---

# What is in a conda package

<!-- TODO(content) -->

---
section: Packaging
---

# Your workspace as a package

<!-- TODO(content) -->

---
section: Packaging
---

# Virtual packages

<!-- TODO(content) -->

---
section: Packaging
---

# CUDA in practice

<!-- TODO(content) -->

---
section: Exercise 2
layout: center
class: text-center
---

# Exercise 2

## Build a ROS package with Pixi

30 minutes · `exercises/02-ros-package/`

<!-- TODO(content) -->

---
section: Collaboration
layout: section
---

# Collaboration, CI/CD & Docker

<!-- TODO(content): 15 min. See docs/explainers/collaboration.md for the outline. -->

---
section: Collaboration
---

# Many platforms, one manifest

<!-- TODO(content) -->

---
section: Collaboration
---

# Jetson and other robots

<!-- TODO(content) -->

---
section: Collaboration
---

# CI/CD and Docker

<!-- TODO(content) -->

---
section: Exercise 3
layout: center
class: text-center
---

# Exercise 3

## Ready for your team

20 minutes · `exercises/03-collaboration/`

<!-- TODO(content) -->

---
section: Wrap-up
layout: center
class: text-center
---

# Thank you

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi**

pixi.prefix.dev · robostack.github.io · discord.gg/kKV8ZxyzY4

We are here for the rest of the conference. Bring us your workspace.
