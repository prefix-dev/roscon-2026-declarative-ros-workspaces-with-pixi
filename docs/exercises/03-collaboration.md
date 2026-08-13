---
icon: lucide/git-branch
---

# Exercise 3: Ready for your team

!!! plain "20 minutes, hands-on"

    **Work in:** `exercises/03-collaboration/` &middot; **Solution:** `solutions/03-collaboration/` &middot; **After:** [Collaboration, CI/CD & Docker](../explainers/collaboration.md)

    **Goal:** take the workspace to your team: a green CI run and a Docker image they can deploy.

<!-- TODO(content): fill in the steps. 20 minutes for three steps, so Step 1 should be
     read-and-commit rather than write-from-scratch. Multi-platform and the Jetson moved to
     Exercise 2; this exercise is now purely collaboration: CI, Docker, sharing. -->

## Step 1: Add CI

<!-- TODO(content): the workflow is provided. Read it, commit it, watch it go green:
     setup-pixi, `pixi lock --check` as the cheap gate, then install and test on a matrix.

     `.github/workflows/ci.yml` in this repository is the live version of exactly this, running
     against all the solutions. Point at it rather than writing YAML from scratch. -->

## Step 2: Ship a Docker image

<!-- TODO(content): the Dockerfile in the solution builds on ghcr.io/prefix-dev/pixi, installs
     from the lockfile, and uses `pixi shell-hook` so no pixi is needed at runtime. Build it,
     compare the image size with a plain ROS base image. -->

## Step 3: Share the environment

<!-- TODO(content): `pixi publish` to a channel, and pixi-pack for a robot with no network. We
     demo these rather than have 50 people mint tokens. Full recipe belongs on the migration page. -->

## Check your work

```bash
pixi run lock-check    # the gate CI enforces
```

<!-- TODO(content): plus a green CI run on the platform matrix. -->

## Going further

<!-- TODO(content):
     - Trim the Docker image further with a multi-stage build.
     - Automated lockfile update PRs.
-->

!!! note "With your own workspace"

    <!-- TODO(content): the realistic adoption order for an existing team: lockfile in CI first,
         Docker second. Each step ships independently and reverts cleanly. -->

---

That is the workshop.
See [Migrating from rosdep & colcon](../reference/migration.md) for the write-up you can hand your team on Monday.
