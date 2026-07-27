---
icon: lucide/terminal
---

# Command cheat sheet

<!-- TODO(content): trim to what the exercises use, then verify every line. A cheat sheet with a
     command that does not exist is worse than no cheat sheet. -->

## Workspace

| Command | What it does |
| --- | --- |
| `pixi init` | Create a `pixi.toml` in the current directory |
| `pixi workspace channel add <channel>` | Add a channel |
| `pixi workspace platform add <platform>` | Add a platform |
| `pixi add <package>` | Add a dependency and update the lockfile |
| `pixi add --pypi <package>` | Add a dependency from PyPI |
| `pixi remove <package>` | Remove a dependency |

## Running things

| Command | What it does |
| --- | --- |
| `pixi run <task>` | Run a task from `[tasks]` |
| `pixi run <command>` | Run any command inside the environment |
| `pixi shell` | Open a shell with the environment activated |
| `pixi run -e <env> <task>` | Run in a specific environment |
| `pixi task list` | List the available tasks |

## Environments and locking

| Command | What it does |
| --- | --- |
| `pixi install` | Install the environment from the lockfile |
| `pixi lock` | Update the lockfile without installing |
| `pixi lock --check` | Fail if the lockfile is out of date &mdash; use this in CI |
| `pixi update <package>` | Update one package to the newest allowed version |
| `pixi list` | Show what is installed |
| `pixi tree <package>` | Show why a package is in the environment |
| `pixi clean` | Remove `.pixi/` |

## Inspecting

| Command | What it does |
| --- | --- |
| `pixi info` | Versions, cache locations, and the virtual packages your machine reports |
| `pixi search <package>` | Search the configured channels |
| `pixi list --platform <platform>` | What would be installed on another platform |

## Building

<!-- TODO(content): confirm the exact build/publish commands against the pixi version we pin for
     the workshop before printing this on a slide. -->

| Command | What it does |
| --- | --- |
| `pixi build` | Build the `[package]` in this workspace into a `.conda` file |

## RoboStack channels

| ROS distribution | Channel |
| --- | --- |
| Jazzy (LTS) | `https://prefix.dev/robostack-jazzy` |
| Humble (LTS) | `https://prefix.dev/robostack-humble` |
| Kilted | `https://prefix.dev/robostack-kilted` |
| Noetic (ROS 1) | `https://prefix.dev/robostack-noetic` |

<!-- TODO(content): verify each channel URL and add the ones we leave out, or drop the table. -->
