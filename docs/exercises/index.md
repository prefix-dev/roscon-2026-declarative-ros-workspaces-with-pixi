---
icon: lucide/wrench
---

# How the exercises work

There are three exercises. Each one follows an explainer, and each one stands on its own: if you get
stuck or arrive late you can start any exercise from its solution and keep up.

## The layout

Every exercise has a directory to work in and a finished version to compare against:

```text
exercises/
  01-ros-workspace/     ← you work here
  02-ros-package/
  03-collaboration/
solutions/
  01-ros-workspace/     ← the finished version, verified in CI
  02-ros-package/
  03-collaboration/
```

The solutions are real Pixi workspaces that are re-solved on every commit, so they are never stale.
Peeking is allowed &mdash; but type the commands yourself, that is where the learning is.

## How to read an exercise

Each page is a series of steps. Every step tells you what to do and how to check it worked:

- **Goal** &mdash; what you will have at the end.
- **Steps** &mdash; do these in order.
- **Check your work** &mdash; run this; if it prints the right thing, move on.
- **Going further** &mdash; optional, for when you finish early.

!!! tip "Work at your own pace"

    The timings are what we plan for in the room. Nothing stops you from finishing the rest later
    &mdash; this site stays online, and everything here works without us.

## If you brought your own project

Each exercise has a "with your own workspace" note describing the equivalent step for an existing
ROS project. Doing the exercise on your own code is the more useful path if you are comfortable, and
we would rather help you with that.

## Getting help

- Raise a hand. There are three of us in the room.
- [Troubleshooting](../reference/troubleshooting.md) covers the errors we expect to see.
- [Command cheat sheet](../reference/cheatsheet.md) if you forget a flag.

Ready? Start with [Exercise 1](01-ros-workspace.md).
