---
icon: lucide/life-buoy
---

# Troubleshooting

<!-- TODO(content): fill this in from the dry runs. Every error we hit while rehearsing on Linux,
     macOS and Windows belongs here, with the exact message people will search for. -->

## `pixi` is not found after installing

<!-- TODO(content): shell restart, PATH, and the Windows specifics. -->

## The solver cannot find a ROS package

<!-- TODO(content): missing channel, wrong distro prefix, package genuinely absent for the
     platform. How to tell the three apart with pixi search. -->

## A GUI window does not appear

<!-- TODO(content): macOS Qt specifics, Wayland vs X11, WSL, and Windows firewall prompts. -->

## Nodes cannot see each other

<!-- TODO(content): ROS_DOMAIN_ID collisions in a room full of people on the same network. This
     will happen. Have the fix ready as a task. -->

## A CUDA environment refuses to solve

<!-- TODO(content): `__cuda` not detected, system-requirements too strict or too loose, and how to
     solve for a GPU machine from a laptop without one. -->

## An existing ROS installation interferes

<!-- TODO(content): a sourced /opt/ros in .bashrc leaking into the Pixi environment. Show how to
     detect it and what clean-env does. -->

## Something is slow

<!-- TODO(content): cold cache, conference Wi-Fi, and what to prefetch. -->

---

Not here? Ask in the room, or open an issue on
[GitHub](https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi/issues) so
the next person finds the answer.
