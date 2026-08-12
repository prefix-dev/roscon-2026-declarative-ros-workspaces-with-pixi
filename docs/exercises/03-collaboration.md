---
icon: lucide/git-branch
---

# Exercise 3: Ready for your team

!!! exercise "20 minutes, hands-on"

    **Work in:** `exercises/03-collaboration/` &middot; **Solution:** `solutions/03-collaboration/` &middot; **After:** [Collaboration, CI/CD & Docker](../explainers/collaboration.md)

    **Goal:** take the workspace from your machine to your team's machines, your CI, and a real GPU.

<!-- TODO(content): fill in the steps. 20 minutes for four steps, so Step 3 should be
     read-and-commit rather than write-from-scratch. -->

## Step 1: Add every platform

<!-- TODO(content): this is where multi-platform is introduced; Exercise 1 stays on the
     participant's own machine. Start from the single-platform starter, then
     `pixi workspace platform add linux-64 osx-arm64 win-64`.
     Re-solve, look at what happened to the lockfile.
     `pixi list --platform win-64`: what your colleague gets, from your Mac.
     (The Jetson aarch64 target comes in Step 2.) -->

## Step 2: Target hardware you do not own

<!-- TODO(content): named platform entries for the robot and a GPU box:

         { name = "jetson", platform = "linux-aarch64", cuda = "12.6" }

     Then a robot feature and environment, and `pixi run robot-list`. You just resolved a complete
     ROS environment for a Jetson from a laptop that is not one. Verified working.

     This is the third time the workshop makes the same point: solving is cheap and portable,
     installing is the expensive part you only do where you need it. Say it out loud here. -->

## Step 3: Add CI

<!-- TODO(content): the workflow is provided. Read it, commit it, watch it go green:
     setup-pixi, a platform matrix, `pixi lock --check` as the cheap gate, then install and test.

     `.github/workflows/ci.yml` in this repository is the live version of exactly this, running
     against all three solutions. Point at it rather than writing YAML from scratch. -->

## Step 4: Run it on a real GPU

<!-- TODO(content): the GPU payoff, on a cloud instance (Brev launchable, link TBD once the
     billing model is confirmed and credits are secured; see IMPLEMENTATION_PLAN.md Stage 5).

     Two paths, both written and tested:
       * GPU box: install the gpu environment, `pixi run gpu-check`, `pixi run gpu-run`.
       * Laptop only: solve for it and inspect, as in Exercise 2. Nobody is blocked.

     Kick off the instance at the START of the session so provisioning is not on the clock here. -->

## Check your work

```bash
pixi run lock-check    # the gate CI enforces
pixi run robot-list    # a Jetson environment, resolved from your laptop
```

<!-- TODO(content): plus a green CI run on a matrix of platforms. -->

## Going further

<!-- TODO(content):
     - The Dockerfile in the solution: build it, compare the image size with a ROS base image.
     - `pixi publish` to your own channel. We demo this rather than have 50 people mint tokens.
       Full recipe belongs on the migration page for afterwards.
     - pixi-pack for a robot with no network.
     - Automated lockfile update PRs.
-->

!!! note "With your own workspace"

    <!-- TODO(content): the realistic adoption order for an existing team: lockfile in CI first,
         platforms second, packaging last. Each step ships independently and reverts cleanly. -->

---

That is the workshop.
See [Migrating from rosdep & colcon](../reference/migration.md) for the write-up you can hand your team on Monday.
