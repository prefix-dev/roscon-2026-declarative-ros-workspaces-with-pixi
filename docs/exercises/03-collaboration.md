---
icon: lucide/git-branch
---

# Exercise 3 — Ready for your team

!!! exercise "20 minutes, hands-on"

    **Work in:** `exercises/03-collaboration/` &middot;
    **Solution:** `solutions/03-collaboration/` &middot;
    **After:** [Collaboration, CI/CD & Docker](../explainers/collaboration.md)

    **Goal:** the workspace from Exercise 2, but solving for every platform your team uses, building
    in GitHub Actions, and publishing the package to a channel.

<!-- TODO(content): fill in the steps. 20 minutes is tight — Step 3 should be copy-paste-and-read,
     not write-from-scratch. -->

## Step 1 — Add every platform

<!-- TODO(content): pixi workspace platform add for linux-64, linux-aarch64, osx-arm64, osx-64,
     win-64. Look at what the lockfile does. Handle the package that is not available everywhere. -->

## Step 2 — Target the robot

<!-- TODO(content): a jetson environment: linux-aarch64 + CUDA system requirements, solved from
     the laptop. Show `pixi list --platform linux-aarch64`. -->

## Step 3 — Add CI

<!-- TODO(content): the provided workflow: setup-pixi, a platform matrix, pixi lock --check,
     build and test. Have them commit and read the logs rather than write YAML. -->

## Step 4 — Publish

<!-- TODO(content): pixi build, then publish to a prefix.dev channel from CI. Use a throwaway
     channel so people can actually run it in the room. -->

## Check your work

<!-- TODO(content): green CI on a matrix of platforms, and the package visible in a channel. -->

## Going further

<!-- TODO(content):
     - The Dockerfile in the solution: build it, compare the image size with a ROS base image.
     - pixi-pack for the robot that has no network.
     - Dependabot-style lockfile updates in CI.
-->

!!! note "With your own workspace"

    <!-- TODO(content): the realistic order to adopt this in an existing team: lockfile in CI
         first, platforms second, packaging last. -->

---

That is the workshop. See [Migrating from rosdep & colcon](../reference/migration.md) for the write-up
you can hand to your team on Monday.
