---
theme: default
title: Declarative ROS workspaces with Pixi and RoboStack
info: |
  ROSCon 2026, Tuesday, September 22nd, 08:00–12:00
  A hands-on workshop for reproducible ROS development.

  Ruben Arts, Wolf Vollprecht, Bas Zalmstra (prefix.dev)
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

---
layout: intro
section: Welcome
---

# Who we are

- **Ruben Arts**, prefix.dev: Pixi
- **Wolf Vollprecht**, prefix.dev: RoboStack, mamba, conda-forge
- **Bas Zalmstra**, prefix.dev: rattler, the Rust conda libraries under Pixi

<br>

Three of us in the room. Raise your hand, we come to you.

---
section: Welcome
---

# Today

<div class="schedule">

| | | |
| --- | --- | --- |
| 15 min | Welcome and setup | together |
| 15 min | Robotics for everyone | we talk |
| 30 min | Pixi in 30 minutes, CUDA included | we talk |
| 30 min | **Exercise 1:** your first ROS 2 workspace | you type |
| 15 min | Building ROS packages with Pixi | we talk |
| 30 min | **Exercise 2:** build ROS packages with Pixi | you type |
| 15 min | Collaboration, CI/CD & Docker | we talk |
| 20 min | **Exercise 3:** ready for your team | you type |

</div>

<div class="ref">Everything is written up at <a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/" target="_blank">prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi</a></div>

---
section: Welcome
layout: center
---

# Before we start

<img src="/site-qr.svg" alt="QR code to the workshop site" style="height: 11rem; margin: 0 auto 1rem;" />

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi**

```bash
git clone https://github.com/...
cd roscon-2026-declarative-ros-workspaces-with-pixi
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

A turtle appears? You're ready.

---
section: Philosophy
layout: section
---

# Robotics for everyone

Why the way we install ROS keeps people out.

---
section: Philosophy
---

# Getting into ROS is linked to an OS and a distro

| You have | Your route |
| --- | --- |
| Ubuntu 24.04 | `apt install`, the happy path |
| Ubuntu 22.04 | Humble only. Want Jazzy? Reinstall your OS |
| Arch or another Linux | Build from source, or a container |
| macOS | No official path. VM or Docker |
| Windows | Limited support, WSL2 or Docker |

---
section: Philosophy
---

# "Just use Docker" is the accepted answer

And to be fair, it works.

- The setup becomes doable, and the team shares one image
- But your whole workflow now lives inside a box
- Editor, debugger, USB/network devices, GPU, GUI tools: much harder
- Setup once, never touch again
- You're not developing on your machine anymore

<img src="/docker-in-cloud.jpg" alt="Docker in Cloud: a container ship" style="position: absolute; right: 3rem; bottom: 3.2rem; height: 46%; z-index: 0; border-radius: 8px;">

---
section: Philosophy
layout: cover
---

# What we want instead

```bash
git clone <your-project>
cd <your-project>
pixi run application
```

Any machine, three commands, and your project runs.

---
section: Philosophy
layout: section
---

# How we get there

All machines · Distroless · Declarative · Reproducible · Fast · Simple

---
section: Philosophy
---

<div class="kicker">How we get there · 1/6</div>

# All machines

Linux, macOS, Windows. x86 and arm64.

- Not just Ubuntu, and not just the one Ubuntu that matches your distro
- Your laptop, the CI runner and the robot can all be different machines
- Pick the hardware you need, and the OS you like!

---
section: Philosophy
---

<div class="kicker">How we get there · 2/6</div>

# Distroless

Jazzy on Ubuntu 22.04. Kilted on macOS. Humble on Windows.

- A ROS distro is a release process, not an operating system
- There's no reason Humble should be tied to Ubuntu 22.04
- Any distro on any machine, and two of them side by side

---
section: Philosophy
---

<div class="kicker">How we get there · 3/6</div>

# Declarative

Your environment is a file in git.

- `pixi.toml` says what you want
- Update your environment when you want
- Roll back to a known good state like you roll back code

---
section: Philosophy
---

<div class="kicker">How we get there · 4/6</div>

# Reproducible

A lockfile (pixi.lock) instead of a Docker image.

- Every package, version and hash, recorded when you change something
- The same environment on your laptop, in CI, on the robot
- Use `git` to manage your versions, not a container registry

---
section: Philosophy
---

<div class="kicker">How we get there · 5/6</div>

# Fast

Minutes to a running project, not hours.

- Manage everything with one tool, no apt, no rosdep, no sourcing
- Let the internet connection be the only slow part, not the setup.
- Getting started: `git clone`, `pixi run sim`

---
section: Philosophy
---

<div class="kicker">How we get there · 6/6</div>

# Simple

If you can use `pip`, you can use Pixi.

- `pixi init`, `pixi add`, `pixi run`: the whole daily flow
- No apt, no rosdep, no sourcing, no `sudo`, no sysadmin knowledge
- Manage everything in one place, and reuse it across all your projects and devices.

---
section: Philosophy
---

# What is a conda package

`ros-jazzy-rclcpp-28.1.18-np2py312hd441986_18.conda`

- An archive with **pre-built binaries** and metadata: name, version, dependencies
- Any language: C++ libraries, Python, compilers, CMake, `ros2` itself
- Installing means downloading and extracting into an environment, no compilation
- The same package format on Linux, macOS and Windows, built per platform
- Born in the scientific Python world in 2012, so this has been battle-tested for 14 years

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/explainers/cuda/" target="_blank">More in the CUDA explainer: what's inside a conda package</a></div>

---
section: Philosophy
---

# Standing on conda-forge and RoboStack

- **conda-forge**: tens of thousands of pre-built packages, community run
  <br>`gcc`, `cmake`, `Python`, `OpenCV`, `PyTorch`, for every platform
- **RoboStack**: the ROS distributions built on top of it
  <br>Noetic to Lyrical, `ros-noetic-rqt` to `ros-lyrical-plotjuggler`
- One environment, both channels: conda-forge for the stack, RoboStack for ROS

---
section: Pixi
layout: section
---

# Pixi introduction

The basics you need for Exercise 1.

---
section: Pixi
---

# What is Pixi

- `apt` is for Debian packages
- `brew` is for Homebrew packages
- `pip` is for PyPI packages
- **Pixi is for conda packages** <span style="opacity: 0.55; font-weight: 400;">+ PyPI</span>

<br>

Pixi creates an environment per project, from one file: `pixi.toml`.

---
section: Pixi
---

# How you install ROS today

- Find the Ubuntu version that matches your distro
- `sudo apt install ros-jazzy-*`, system wide
- One distro per machine
- `source /opt/ros/jazzy/setup.bash` in every terminal
- A second project? Docker, or a second machine
- macOS? Not supported. Windows? Build from source

---
section: Pixi
---

# `pixi.toml`

```toml
[workspace]       # metadata, channels, platforms
[dependencies]    # what you want installed
[tasks]           # commands with a name
```

<br>

Everything you need to know for now. It lives at the **root** of your project.

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/pixi_manifest/" target="_blank">Manifest reference</a></div>

---
section: Pixi
---

# Channels and dependencies

- A channel is like an apt source, but it's written in your `pixi.toml`
- `conda-forge` for everything, `robostack-jazzy` for ROS 2 Jazzy
  <br><span style="opacity: 0.55;">exactly like the Ubuntu repos plus the ROS repo you add to `sources.list`</span>
- Package names are `ros-<distro>-<name>`, with hyphens
- `pixi add` writes it in the manifest, solves and installs

<div class="ref"><a href="https://robostack.github.io" target="_blank">RoboStack package list</a> · <a href="https://prefix.dev/channels" target="_blank">Search packages on prefix.dev</a></div>

---
section: Pixi
---

# The `pixi` command

```bash
pixi init                       # a new workspace
pixi add ros-jazzy-ros-base     # add, solve, install
pixi run ros2 topic list        # run inside the environment
pixi shell                      # step inside
pixi install                    # everything from the lockfile
```

<div class="text-sm" style="margin-top: 0.5rem;">

| You know | With Pixi |
| --- | --- |
| `apt install`, system wide | `pixi add`, per project |
| `source install/setup.bash` | `pixi shell` |
| `rosdep install`, hoping for the same versions | `pixi install`, from the lockfile |

</div>

<div class="ref"><code>pixi &lt;command&gt; --help</code> · tab completion: <code>pixi completion --shell zsh</code> · <a href="https://pixi.prefix.dev/latest/reference/cli/pixi/" target="_blank">CLI reference</a></div>

---
section: Pixi
layout: two-cols-header
---

# Tasks

::left::

```toml
[tasks]
sim = "ros2 run turtlesim turtlesim_node"
build = "colcon build"

[tasks.dance]
cmd = "ros2 run turtle_dancer dance"
depends-on = ["build"]
```

::right::

<div style="margin-left: 1.5rem;">

- `pixi run sim`, on every platform
- `pixi run dance` builds first
- Any command works: `pixi run ros2 topic list`

</div>

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/advanced_tasks/" target="_blank">Tasks documentation</a></div>

---
section: Pixi
---

# `pixi shell`

```bash
pixi shell
ros2 topic list
ros2 run turtlesim turtlesim_node
exit
```

- Puts you inside the environment, like `source install/setup.bash` did
- Everything you type runs there, until you `exit`
- `pixi run` still works inside it

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/cli/pixi/shell/" target="_blank">pixi shell reference</a></div>

---
section: Pixi
---

# Activation

Every `pixi run` and `pixi shell` activates the environment first: `PATH`, `ROS_DISTRO`, `AMENT_PREFIX_PATH`, all set for you.

```toml
[activation]
scripts = ["install/setup.sh"]

[activation.env]
ROS_DOMAIN_ID = "42"
```

- Packages bring their own: the ROS setup comes with `ros-jazzy-ros-workspace`
- Your workspace can add scripts and variables
- `pixi shell-hook` prints the whole thing as a shell script

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/environment/#activation" target="_blank">Environment activation</a></div>

---
section: Pixi
---

# Building your own package with colcon

- `ros-dev-tools` gives you colcon, CMake and the compilers
- `colcon build` works like it always did
- `ros2 run` only finds your node after sourcing, so we source on activation

<br>

edit, `colcon build`, source, run. Remember this one.

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/01-ros-workspace/#14-build-your-own-node-with-colcon" target="_blank">Exercise 1.4: build your own node with colcon</a></div>

---
section: Pixi
---

# Two distros, one workspace

```toml
[environments.default]
channels = ["robostack-jazzy", "conda-forge"]
[environments.default.dependencies]
ros-jazzy-ros-base = ">=0.11"

[environments.kilted]
channels = ["robostack-kilted", "conda-forge"]
[environments.kilted.dependencies]
ros-kilted-ros-base = "*"
```

Every environment has its own channels and packages, the tasks are shared.

`pixi run sim` for Jazzy, `pixi run -e kilted sim` for Kilted.

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_environment/" target="_blank">Multiple environments</a></div>

---
section: Pixi
---

# Solve for machines you don't have

- `platforms`: Pixi solves for all of them, you install where you need it
- A named platform describes a machine: `jetson` is `linux-aarch64` with CUDA 13
- `pixi list --platform jetson`, from your laptop

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>

---
section: Pixi
---

# Virtual packages

```console
$ pixi info
Virtual packages: __unix=0=0
                : __linux=6.8.0=0
                : __glibc=2.39=0
                : __cuda=12.4=0
                : __archspec=1=x86_64
```

- Not packages you install, facts about the machine
- The solver uses them: a package can require `__cuda >=12`
- On a machine you don't have, you declare them yourself

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/system_requirements/" target="_blank">Virtual packages and system requirements</a></div>

---
section: Pixi
---

# CUDA

The driver comes from the OS, everything else from conda-forge.

```bash
pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
```

```toml
[dependencies]
pytorch-gpu = { version = ">=2.5", when = "__cuda" }
pytorch = ">=2.5"
```

- `--cuda 12` sets `__cuda` for that platform, so the solver picks GPU builds
- `when = "__cuda"`: the GPU build there, the CPU build everywhere else
- Solving works from any laptop, running needs the driver

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/explainers/cuda/" target="_blank">CUDA explainer</a> · <a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>

---
section: Pixi
---

# The lockfile

- `pixi.lock` has every package, version and hash
- For every platform and every environment
- Pixi writes it, you commit it
- `pixi install --locked` in CI, so nothing changes without you noticing

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/lock_file/" target="_blank">The lockfile</a></div>

---
section: Pixi
---

# A workspace in five lines

```bash
pixi init ros-workspace
cd ros-workspace
pixi workspace channel add --prepend robostack-jazzy
pixi add ros-jazzy-ros-base ros-jazzy-turtlesim
pixi run ros2 run turtlesim turtlesim_node
```

That's it.

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/reference/cheatsheet/" target="_blank">Command cheat sheet</a></div>

---
section: Exercise 1
layout: center
class: text-center
---

# Now it's your turn

## Exercise 1: Your first ROS 2 workspace

30 minutes · `cd exercises/01-ros-workspace`

<div class="text-left mx-auto" style="max-width: 30rem; margin: 1rem auto;">

1. `pixi init`, add the RoboStack channel, `pixi add` ROS 2
2. Add tasks and drive the turtle
3. Build `src/turtle_dancer` with colcon
4. Add Kilted as a second environment
5. Add PyTorch, a GPU platform and a Jetson

</div>

<small>

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/01-ros-workspace/**

Stuck? Look in `solutions/01-ros-workspace/` or raise your hand.

</small>

---
section: Packaging
layout: center
---

# Building ROS packages with Pixi

No colcon, no sourcing.

---
section: Packaging
---

# The loop from Exercise 1

<div class="text-2xl" style="margin: 2rem 0;">

edit → `colcon build` → `source install/setup.bash` → `ros2 run`

</div>

- Forget to source: `Package 'turtle_dancer' not found`
- `build/ install/ log/` in your workspace
- A full toolchain, just to build your own package

---
section: Packaging
---

# Two roles for one `pixi.toml`

| | | |
| --- | --- | --- |
| **Workspace** | `[workspace]` | what you `pixi run` |
| **Package** | `[package]` | what Pixi builds |

<br>

The package manifest lives next to `package.xml`, and `package.xml` doesn't change.

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/workspace/" target="_blank">Workspaces and packages</a></div>

---
section: Packaging
---

# Build backends

Pixi doesn't know how to compile your code. A **build backend** does.

| Backend | Builds | Reads |
| --- | --- | --- |
| `pixi-build-cmake` | C and C++ | `CMakeLists.txt` |
| `pixi-build-python` | Python | `pyproject.toml` |
| `pixi-build-rust` | Rust | `Cargo.toml` |
| `pixi-build-ros` | ROS packages | `package.xml` |

- The package manifest names its backend, Pixi fetches and runs it
- The backend is a conda package itself, versioned and pinned like the rest

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/backends/" target="_blank">Build backends overview</a></div>

---
section: Packaging
---

# `pixi-build-ros` reads your `package.xml`

- Name, version, dependencies and build type come from `package.xml`
- Dependencies get RoboStack names: `rclcpp` becomes `ros-jazzy-rclcpp`
- The distro comes from your channel
- It runs your normal `ament_cmake` or `ament_python` build
- The result is a conda package

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/" target="_blank">pixi-build-ros documentation</a></div>

---
section: Packaging
---

# What you write

```toml
# pixi.toml, three new lines
[workspace]
preview = ["pixi-build"]
[workspace.dependencies]
pixi-build-ros = ">=0.7.2"
[dependencies]
ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }
```

```toml
# src/turtle_dancer/pixi.toml, the whole file
[package.build.backend]
name = "pixi-build-ros"
workspace = true
```

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/ros/" target="_blank">Building ROS packages with Pixi</a> · <a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/" target="_blank">Exercise 2</a></div>

---
section: Packaging
---

# `pixi run dance`

1. Pixi checks if the sources, `package.xml` or `CMakeLists.txt` changed
2. If so, it builds and installs the package into the environment
3. It runs the task

<br>

Your node is now a normal package in the environment, next to `turtlesim`. No sourcing.

<div class="text-2xl" style="margin-top: 1.5rem;">

edit → `pixi run dance`

</div>

---
section: Packaging
---

# What you can delete

- `build = "colcon build"`
- `ros-dev-tools`
- `[target.*.activation]`
- `build/ install/ log/`

<br>

What's left is a small workspace `pixi.toml` and a two line package manifest.

---
section: Exercise 2
layout: center
class: text-center
---

# Now it's your turn

## Exercise 2: Build ROS packages with Pixi

30 minutes · `cd exercises/02-ros-package`

<div class="text-left mx-auto" style="max-width: 34rem; margin: 1rem auto;">

1. Turn on `pixi-build`, add the backend to the workspace
2. Write `src/turtle_dancer/pixi.toml`, two lines
3. Add the path dependency, `pixi install`
4. Delete the colcon parts, `pixi run dance`
5. Change `dance.cpp`, run again
6. Do the same for `src/turtle_choreographer`

</div>

<small>

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/**

Brought your own workspace? Try the backend on one of your packages and call us over.

</small>

---
section: Collaboration
layout: section
---

# Collaboration, CI/CD & Docker

From works on my machine to works on the team's.

---
section: Collaboration
---

# Many platforms, one manifest

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```

- Pixi solves every platform and records all of them in one lockfile
- A teammate: `git clone`, `pixi install`, done
- Differences go in `[target.win-64]` or a `when = "__cuda"` condition

<br>

Solved means the packages exist and agree. It doesn't mean your node runs there. That's what CI is for.

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>

---
section: Collaboration
---

# CI made easy

```yaml
- uses: prefix-dev/setup-pixi@v0.10.0
- run: pixi run test
```

- Two lines: install Pixi and the environment, run your task
- The same task names as on your laptop, no second setup in YAML
- Caching comes for free

<div class="ref"><a href="https://pixi.prefix.dev/latest/integration/ci/github_actions/" target="_blank">setup-pixi on GitHub Actions</a></div>

---
section: Collaboration
---

# What `setup-pixi` does for you

1. Downloads the Pixi binary and puts it on `PATH`
2. Logs in to your channels, if you gave it a token
3. Restores the environment from cache, keyed on the hash of `pixi.lock`
4. `pixi install`, per environment you ask for, `--locked` if you say so
5. Saves the cache, runs `pixi list` so you can see what you got
6. Optionally activates the environment for every next step

```yaml
- uses: prefix-dev/setup-pixi@v0.10.0
  with:
    environments: default kilted
    activate-environment: default
    auth-token: ${{ secrets.PREFIX_DEV_TOKEN }}
```

<div class="ref"><a href="https://github.com/prefix-dev/setup-pixi" target="_blank">setup-pixi source</a> · <a href="https://pixi.prefix.dev/latest/integration/ci/github_actions/" target="_blank">GitHub Actions docs</a></div>

---
section: Collaboration
---

# Docker

One Dockerfile, two stages.

```dockerfile
FROM ghcr.io/prefix-dev/pixi:0.76.2-noble AS build
COPY . /app
RUN pixi install --locked
RUN pixi shell-hook -s bash > /shell-hook.sh
```

- Start from the Pixi image, copy the workspace in
- Install the environment from the lockfile
- Write the activation to a script, for the next stage

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/container/" target="_blank">Pixi in containers</a></div>

---
section: Collaboration
---

# The runtime stage

```dockerfile
FROM ubuntu:24.04 AS runtime
COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
```

- A plain base image, no Pixi, no package manager
- It receives the finished environment and the activation script, nothing else
- `shell-hook.sh` is the `source setup.bash` of the container

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/container/" target="_blank">Pixi in containers</a></div>

---
section: Collaboration
---

# Why `--locked`

```dockerfile
RUN pixi install --locked
```

- Without it, Pixi re-solves when `pixi.toml` and `pixi.lock` disagree, and the image gets something the team never tested
- With it, the build fails instead
- Same flag in CI, same answer: the lockfile is the only thing that decides what's installed

<br>

Laptop, CI and image all install from the same `pixi.lock`.
"It works in the container but not on my machine" becomes a diff of one file.

---
section: Collaboration
---

# `pixi-pack`

```bash
pixi-pack --environment default --platform linux-aarch64 pixi.toml
```

```bash
pixi-unpack environment.tar     # on the other machine
source activate.sh
```

- One archive with the packages inside, no network or package manager needed to unpack
- Pack for any platform from the machine you're on
- `--create-executable` gives one self-extracting file

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/pixi_pack/" target="_blank">pixi-pack</a> · <a href="https://pixi.prefix.dev/latest/reference/cli/pixi/publish/" target="_blank">pixi publish</a></div>

---
section: Exercise 3
layout: center
class: text-center
---

# Now it's your turn

## Exercise 3: Ready for your team

20 minutes · `cd exercises/03-collaboration`

<div class="text-left mx-auto" style="max-width: 34rem; margin: 1rem auto;">

1. `pixi global install gh`, put the workspace on GitHub
2. Add CI with `setup-pixi`, watch it go green
3. Build the Docker image and run it: no Pixi inside
4. We demo `pixi publish` and `pixi-pack`

</div>

<small>

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/03-collaboration/**

Your own workspace works here too. That's the point.

</small>

---
section: Wrap-up
layout: center
class: text-center
---

# Thank you

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi**

pixi.prefix.dev · robostack.github.io · discord.gg/kKV8ZxyzY4

We are here for the rest of the conference.
Bring us your workspace.
