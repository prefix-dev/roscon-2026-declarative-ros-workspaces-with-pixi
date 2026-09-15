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
layout: default
section: Welcome
---

# Who we are

Three of us in the room. Raise your hand, we come to you.

- Wolf Vollprecht: Prefix.dev founder/CEO
- Bas Zalmstra: Software Architect
- Ruben Arts: Pixi, Community focus

<img src="/bas-wolf-ruben-prefix.png" alt="Bas, Wolf, and Ruben from prefix.dev" class="absolute bottom-10 left-1/2 -translate-x-1/2 h-80 w-auto" />

---
section: Welcome
---

# Today

<div class="schedule">

| Time | Duration | Topic | Format |
| --- | --- | --- | --- |
| 08:00 | 15 min | Welcome and setup | together |
| 08:15 | 15 min | Robotics for everyone | we talk |
| 08:30 | 30 min | Pixi intro | we talk |
| 09:00 | 50 min | **Exercise 1:** your first ROS 2 workspace | you type |
| 09:50 | 10 min | Coffee break | together |
| 10:00 | 20 min | Building ROS packages with Pixi | we talk |
| 10:20 | 30 min | **Exercise 2:** build ROS packages with Pixi | you type |
| 10:50 | 20 min | Collaboration, CI/CD & Docker | we talk |
| 11:10 | 30 min | **Exercise 3:** ready for your team | you type |
| 11:40 | 20 min | Wrap-up and Q&A | together |
</div>

<div class="ref">Everything is written up at <a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/" target="_blank">prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi</a></div>

---
section: Welcome
layout: center
---

# Before we start

<a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/setup/" target="_blank" rel="noopener noreferrer">
  <img src="/site-qr.svg" alt="QR code to Before you start, the workshop setup page" style="height: 9rem; margin: 0 auto 1rem;" />
</a>

[**Before you start: workshop setup**](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/setup/)

<CodeWindow title="bash" terminal>

```bash
git clone https://github.com/...
cd roscon-2026-declarative-ros-workspaces-with-pixi
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

</CodeWindow>

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

- The setup becomes doable, and the team shares one image
- Your workflow now lives inside a box
- Editor, debugger, USB/network devices, GPU, GUI tools: much harder
- Setup once, rebuilding is slow, never touch again

<img src="/docker-in-cloud.jpg" alt="Docker in Cloud: a container ship" style="position: absolute; right: 3rem; bottom: 3.2rem; height: 46%; z-index: 0; border-radius: 8px;">

---
section: Philosophy
layout: cover
---

# What we want instead

<CodeWindow title="bash" terminal>

```bash
git clone your-project
cd your-project
pixi run application
```

</CodeWindow>

Any machine, three commands, and your robotics project runs.

---
section: Philosophy
layout: section
---

# How to do that

All machines · Distroless · Declarative · Reproducible · Fast · Simple

---
section: Philosophy
---

<div class="kicker">How we get there · 1/6</div>

# All machines

Linux, macOS, Windows. x86 and arm64.

- Not just Ubuntu
- Your laptop, the CI runner and the robot can all be different machines
- Pick the hardware you need, and the OS you like!

<div class="absolute bottom-16 left-0 right-0 flex items-center justify-center gap-16">
  <img src="/ubuntu.svg" alt="Ubuntu Linux" class="h-18 w-auto" />
  <img src="/fedora.svg" alt="Fedora Linux" class="h-18 w-auto" />
  <img src="/windows.svg" alt="Windows" class="h-18 w-auto" />
  <img src="/apple.svg" alt="Apple" class="h-18 w-auto" />
</div>

---
section: Philosophy
---

<div class="kicker">How we get there · 2/6</div>

# Distroless

Jazzy on Ubuntu 22.04. Kilted on macOS. Humble on Windows.

- A ROS distro is a release process, not an operating system
- Any distro on any machine, and two of them side by side
- Move towards a rolling release model

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

A lockfile (`pixi.lock`) instead of a Docker image.

- Every package, version and hash, recorded when you change something
- The same environment on your laptop, in CI, on the robot
- Use `git` to manage your versions, instead of a container registry

---
section: Philosophy
---

<div class="kicker">How we get there · 5/6</div>

# Fast

Minutes to a running project, not hours.

- Manage the whole environment setup with one tool.
- Let the internet connection be the only slow part.
- Low effortcommand setup: `git clone`, `pixi run sim`

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
layout: section
---

# Why is setup this simple?

You don't have to build the whole ROS stack yourself.


---
section: Philosophy
---

# Standing on conda-forge and RoboStack

<img src="/package-pipeline.svg" alt="Open-source projects are built into conda-forge packages, which supply the RoboStack build environment. ROS sources from ROS Index and rosdistro are built and published to RoboStack channels." class="w-full mt-6" />

Pixi combines packages from **conda-forge** and **RoboStack** in one environment.

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

| Package manager | Packages it installs |
| --- | --- |
| `apt` | Debian packages |
| `brew` | Homebrew packages |
| `pip` | Python packages from PyPI |
| `pixi` | **conda packages + Python packages from PyPI** |


---
section: Pixi
---

# Installing ROS 2

<div class="text-base">

| Official Ubuntu installation| With Pixi + RoboStack |
| --- | --- |
| Use Ubuntu 24.04 and a UTF-8 locale | Install Pixi on Linux, macOS or Windows |
| Enable Universe; install `ros2-apt-source` | `pixi init -c robostack-lyrical -c conda-forge` |
| `sudo apt update`<br>`sudo apt upgrade` | No system package changes |
| `sudo apt install ros-lyrical-desktop` | `pixi add ros-lyrical-desktop` |
| `source /opt/ros/lyrical/setup.bash` | `pixi shell` |
| `ros2 run demo_nodes_cpp talker` | `ros2 run demo_nodes_cpp talker` |

</div>

<div class="ref"><a href="https://docs.ros.org/en/lyrical/Get-Started/Installation.html" target="_blank">Official ROS 2 Lyrical installation guide</a> · <a href="https://robostack.github.io/GettingStarted.html" target="_blank">RoboStack getting started</a></div>

---
section: Pixi
---

# The `pixi.toml`

<CodeWindow title="pixi.toml">

```toml {*}{lines:true}
[workspace]
platforms = ["linux-64", "osx-arm64", "win-64"]
channels = ["robostack-lyrical", "conda-forge"]

[dependencies]
ros-lyrical-desktop = "*"

[tasks]
start = "ros2 launch my_package my_launch_file.launch.py"
```

</CodeWindow>

It lives at the **root** of your workspace.

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/pixi_manifest/" target="_blank">Manifest reference</a></div>

---
section: Pixi
---

# The `pixi` command

| Command | What it does |
| --- | --- |
| `pixi init` | Create a workspace |
| `pixi add ros-lyrical-ros-base` | Add the dependency, solve and install |
| `pixi run ros2 topic list` | Run a command inside the environment |
| `pixi shell` | Open a shell inside the environment |
| `pixi install` | Install the environment |

<div class="ref"><code>pixi &lt;command&gt; --help</code> · tab completion: <code>pixi completion --shell zsh</code> · <a href="https://pixi.prefix.dev/latest/reference/cli/pixi/" target="_blank">CLI reference</a></div>

---
section: Pixi
layout: default
---

# Tasks

<div class="grid gap-6 items-start" style="grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);">

<CodeWindow title="pixi.toml">

```toml {*}{lines:false}
[tasks]
sim = "ros2 run turtlesim turtlesim_node"

[tasks.build]
cmd = "colcon build"
inputs = ["src/turtle_dancer"]

[tasks.dance]
cmd = "ros2 run turtle_dancer dance"
depends-on = ["build"]
```

</CodeWindow>

<CodeWindow title="bash" terminal>

```bash
# On every platform
pixi run sim

# Builds first
pixi run dance

# Run any command
pixi run ros2 topic list
```

</CodeWindow>

</div>

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/advanced_tasks/" target="_blank">Tasks documentation</a></div>

---
section: Pixi
---

# `pixi shell`

<CodeWindow title="bash" terminal>

```bash
pixi shell
ros2 topic list
ros2 run turtlesim turtlesim_node
exit
```

</CodeWindow>

- Puts you inside the environment, like `source install/setup.bash` did
- Everything you type runs there, until you `exit`
- `pixi run` still works inside it

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/cli/pixi/shell/" target="_blank">pixi shell reference</a></div>

---
section: Pixi
---

# Activation

<CodeWindow title="pixi.toml">

```toml {*}{lines:true}
[activation]
scripts = ["install/setup.sh"]

[activation.env]
ROS_DOMAIN_ID = "42"
```

</CodeWindow>

- `pixi run` activates the environment first
- `pixi shell` activates the environment and drops you into a shell
- `pixi shell-hook` prints the whole activation script as a shell script and lets you source it manually

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/environment/#activation" target="_blank">Environment activation</a></div>

---
section: Pixi
---

# Building your own package with colcon

With ROS installed and `src/turtle_dancer/` in your workspace:

<CodeWindow title="bash" terminal>

```bash
pixi add ros-dev-tools
pixi run colcon build

pixi shell
(ros_ws)> ros2 run ...
```

</CodeWindow>

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/01-ros-workspace/#14-build-your-own-node-with-colcon" target="_blank">Exercise 1.4: build your own node with colcon</a></div>

---
section: Pixi
---

# Two distros, one workspace

<CodeWindow title="pixi.toml" :scale="85">

```toml {*}{lines:true}
[environments.default]
channels = ["robostack-lyrical", "conda-forge"]
[environments.default.dependencies]
ros-lyrical-ros-base = ">=0.13"

[environments.kilted]
channels = ["robostack-kilted", "conda-forge"]
[environments.kilted.dependencies]
ros-kilted-ros-base = "*"
```

</CodeWindow>

Every environment has its own channels and packages, the tasks are shared.

`pixi run sim` for Lyrical, `pixi run -e kilted sim` for Kilted.

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_environment/" target="_blank">Multiple environments</a></div>

---
section: Pixi
---

# Solve for machines you don't have

Pixi solves for every platform you declare, not just the one you are currently on.

<CodeWindow title="pixi.toml">

```toml {*}{lines:true}
[workspace]
platforms = ["linux-64", "linux-aarch64", "osx-arm64", "win-64"]
```

</CodeWindow>

<CodeWindow title="Terminal" terminal>

```bash
$ pixi lock
```

</CodeWindow>

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>

---
section: Pixi
---

# Virtual packages

<CodeWindow title="pixi info" terminal>

```bash
$ pixi info
Virtual packages: __unix=0=0
                : __linux=6.8.0=0
                : __glibc=2.39=0
                : __cuda=12.4=0
                : __archspec=1=x86_64
```

</CodeWindow>

- Not packages you install, facts about the machine
- The solver uses them: a package can require `__cuda >=12`
- On a machine you don't have, you declare them yourself

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/system_requirements/" target="_blank">Virtual packages and system requirements</a></div>

---
section: Pixi
---

# CUDA

The driver comes from the OS, everything else from conda-forge.

<CodeWindow title="pixi.toml">

```toml {*}{lines:true}
[workspace]
platforms = [ { platform = "linux-64", cuda = 12 }, "linux-64"]
[dependencies]
pytorch-gpu = { version = ">=2.5", when = "__cuda" }
pytorch = ">=2.5"
```

</CodeWindow>

- `cuda = 12` sets `__cuda` for that platform, so the solver picks GPU builds
- `when = "__cuda"`: the GPU build there, the CPU build everywhere else
- Solving works from any laptop, running needs the driver

<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/explainers/cuda/" target="_blank">CUDA explainer</a> · <a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>


---
section: Pixi
---

# A new workspace in five lines

<CodeWindow title="bash" terminal>

```bash
pixi init ros-workspace -c robostack-lyrical -c conda-forge
cd ros-workspace
pixi add ros-lyrical-ros-base ros-lyrical-turtlesim
pixi run ros2 run turtlesim turtlesim_node
```

</CodeWindow>


<div class="ref"><a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/reference/cheatsheet/" target="_blank">Command cheat sheet</a></div>

---
section: Exercise 1
layout: center
class: text-center
---

# Now it's your turn

## Exercise 1: Your first ROS 2 workspace

30 minutes · `cd exercises/01-ros-workspace`


<small>

[exercises/01-ros-workspace/](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/01-ros-workspace/)

Stuck? Look in `solutions/01-ros-workspace/` or raise your hand.

</small>

---
section: Packaging
layout: center
---

# Building ROS packages with Pixi

Skip colcon.

---
section: Packaging
---

# Two roles for one `pixi.toml`

| | | |
| --- | --- | --- |
| **Workspace** | `[workspace]` | what you `pixi run` |
| **Package** | `[package]` | what Pixi builds |

<br>
<br>
<br>

Currently in preview as we might still change some syntax and conventions.

```bash
pixi workspace preview add pixi-build
```

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/workspace/" target="_blank">Workspaces and packages</a></div>

---
section: Packaging
---

# What you write


<CodeWindow title="pixi.toml">

```toml {*}{lines:true}
[dependencies]
ros-lyrical-turtle-dancer = { path = "src/turtle_dancer" }
```

</CodeWindow>

<CodeWindow title="src/turtle_dancer/pixi.toml">

```toml {*}{lines:true}
[package.build.backend]
name = "pixi-build-ros"
```

</CodeWindow>


<div class="ref"><a href="https://pixi.prefix.dev/latest/build/ros/" target="_blank">Building ROS packages with Pixi</a> · <a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/" target="_blank">Exercise 2</a></div>

---
section: Packaging
---

# `pixi-build-ros` reads your `package.xml`

<div class="grid grid-cols-2 gap-6 items-start mt-6">
<div>

<div class="text-sm mb-2">Existing ROS metadata (excerpt)</div>

<CodeWindow title="package.xml" :scale="70">

```xml {*}{lines:false}
<package format="3">
  <name>turtle_dancer</name>
  <version>0.1.0</version>
  <license>BSD-3-Clause</license>
  <buildtool_depend>ament_cmake</buildtool_depend>
  <depend version_gte="1.0.0">rclcpp</depend>
  <depend>geometry_msgs</depend>
  <exec_depend>turtlesim</exec_depend>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

</CodeWindow>
</div>
<div>

<div class="text-sm mb-2">Explicit Pixi metadata (illustrative)</div>

<CodeWindow title="pixi.toml [package]" :scale="70">

```toml {*}{lines:false}
[package]
name = "ros-lyrical-turtle-dancer"
version = "0.1.0"
license = "BSD-3-Clause"
[package.build-dependencies]
ros-lyrical-ament-cmake = "*"
ros-lyrical-rclcpp = ">=1.0.0"
ros-lyrical-geometry-msgs = "*"
[package.run-dependencies]
ros-lyrical-rclcpp = "*"
ros-lyrical-geometry-msgs = "*"
ros-lyrical-turtlesim = "*"
```

</CodeWindow>
</div>

</div>

<div class="text-base mt-2">

With `pixi-build-ros`, keep the metadata in `package.xml`, not both files.

</div>

<div class="ref">The workspace channel selects the ROS distro. · <a href="https://pixi.prefix.dev/latest/build/backends/pixi-build-ros/" target="_blank">pixi-build-ros documentation</a></div>

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
| `pixi-build-rattler-build` | Conda recipes | `recipe.yaml` |

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/backends/" target="_blank">Build backends overview</a></div>



---
section: Packaging
---

# What goes into a recipe?

The backend works out the sources, dependencies and build steps.

<CodeWindow title="recipe.yaml pseudocode" :scale="80">

```yaml
package:
  name: ros-lyrical-turtle-dancer
  version: 0.1.0
source:
  path: src/turtle_dancer
requirements:
  build: [cxx-compiler, cmake, ninja]
  host: [ros-lyrical-ament-cmake, ros-lyrical-rclcpp]
  run: [ros-lyrical-rclcpp]
build:
  script: configure → compile → install into $PREFIX
```

</CodeWindow>

With `pixi-build-ros`, you don't write this recipe yourself.

---
section: Packaging
---

# Need more control? Use `rattler-build`

Already have a recipe, or need custom build steps?

`rattler-build` builds conda packages from a `recipe.yaml`

<CodeWindow title="pixi.toml  next to your recipe.yaml">

```toml {*}{lines:false}
[package.build.backend]
name = "pixi-build-rattler-build"

[package.build.config]
recipe = "recipe.yaml"
```

</CodeWindow>

Have full control over the sources, dependencies, patches and build steps in the recipe.

<div class="ref"><a href="https://rattler-build.prefix.dev/latest/" target="_blank">rattler-build documentation</a> · <a href="https://pixi.prefix.dev/latest/build/backends/pixi-build-rattler-build/" target="_blank">Using recipes with Pixi</a></div>

---
section: Packaging
---

# Inside a conda package

`ros-lyrical-rclcpp-32.0.0-np2py314h1e5664e_22.conda`

<div class="grid gap-8 items-start" style="grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);">

<FileTree
  root-label="Extracted package · osx-arm64"
  :tree="[
    { name: 'info', type: 'dir', children: [
      { name: 'index.json' },
      { name: 'paths.json' },
    ]},
    { name: 'lib', type: 'dir', children: [
      { name: 'librclcpp.dylib' },
    ]},
    { name: 'include/rclcpp/rclcpp', type: 'dir', children: [
      { name: 'rclcpp.hpp' },
    ]},
    { name: 'share/rclcpp', type: 'dir', children: [
      { name: 'package.xml' },
    ]},
  ]"
/>

<div>

- **Metadata:** `index.json` has the name, version and dependencies; `paths.json` lists files and hashes.
- **Content:** pre-built libraries, headers and ROS resources.

</div>
</div>

<div class="ref">Selected files after extraction. <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html" target="_blank">Conda package format</a></div>

---
section: Packaging
---

# Publishing Pixi packages

Opt each package into workspace publishing:

<CodeWindow title="src/turtle_dancer/pixi.toml">

```toml {*}{lines:false}
[package]
publish = true
```

</CodeWindow>

<CodeWindow title="bash" terminal :scale="80">

```bash
# Local channel, as in Exercise 2
pixi publish --target-channel output

# Your Prefix.dev channel (requires write access)
pixi auth login prefix.dev
pixi publish --target-channel https://prefix.dev/[your-channel]
```

</CodeWindow>

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/cli/pixi/publish/" target="_blank">pixi publish</a> · <a href="https://pixi.prefix.dev/latest/build/workspace/#publishing-the-workspace" target="_blank">Publishing a workspace</a></div>


---
section: Packaging
---

# Depend on a Pixi package

<div class="grid grid-cols-2 gap-6 items-start mt-6">
<div>

<CodeWindow title="pixi.toml · channel, path or Git" :scale="75">

```toml {*}{lines:false}
[dependencies]
# Pre-built package from a channel
ros-lyrical-rclcpp = "32.0.0"

# Local source package
[dependencies.ros-lyrical-turtle-dancer]
path = "src/turtle_dancer"

[dependencies.brain]
git = "https://github.com/user/brain.git"
branch = "main"
```

</CodeWindow>
</div>
<div>

<CodeWindow title="pixi.toml · inline package" :scale="75">

```toml {*}{lines:false}
[dependencies.visualizer]
git = "https://github.com/user/visualizer.git"
package.build.backend.name = "pixi-build-python"
```

</CodeWindow>

<div class="text-base">

No `pixi.toml` upstream?
Define the package's backend here.

</div>
</div>
</div>


<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/pixi_manifest/#dependencies" target="_blank">Dependency specifications</a> · <a href="https://pixi.prefix.dev/latest/build/inline_packages/" target="_blank">Inline packages</a></div>


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
7. publish both packages locally

</div>

<small>

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/**

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

# CI made easy

<CodeWindow title="GitHub Actions (steps)" scale="85">

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: prefix-dev/setup-pixi@v0.10.2
      - run: pixi run test
```

</CodeWindow>

- Two lines: install Pixi and the environment, run your task
- The same task names as on your laptop, no second setup in YAML
- Caching comes for free

<div class="ref"><a href="https://pixi.prefix.dev/latest/integration/ci/github_actions/" target="_blank">setup-pixi on GitHub Actions</a></div>

---
section: Collaboration
---

# Docker

<CodeWindow title="Dockerfile">

```dockerfile
FROM ghcr.io/prefix-dev/pixi:0.80.0-noble AS build
WORKDIR /app
COPY pixi.toml pixi.lock ./
RUN pixi install --locked
RUN pixi shell-hook --shell bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh
```

</CodeWindow>

- Start from the Pixi image, copy the manifest and lockfile in
- Install the environment from the lockfile
- Write the activation to a script, for the next stage

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/container/" target="_blank">Pixi in containers</a></div>

---
section: Collaboration
---

# The runtime stage

<CodeWindow title="Dockerfile">

```dockerfile
FROM ubuntu:26.04 AS runtime
COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["ros2", "run", "demo_nodes_cpp", "talker"]
```

</CodeWindow>

- A plain base image, without a `pixi` binary
- It receives the finished environment and the activation script
- `shell-hook.sh` contains the activation commands without Pixi

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/container/" target="_blank">Pixi in containers</a></div>

---
section: Collaboration
---

# `pixi-pack`: Shipping an environment as a file

<div class="grid grid-cols-2 gap-6 items-start mt-6">

<CodeWindow title="Terminal" terminal scale="85">

```bash
$ pixi-pack --platform linux-64
```

</CodeWindow>

<CodeWindow title="Terminal other machine" terminal scale="85">

```bash
$ pixi-unpack environment.tar
$ source activate.sh
$ ros2 pkg executables demo_nodes_cpp
$ ros2 run demo_nodes_cpp talker
```

</CodeWindow>

</div>

- Use for offline deployment
- Unpack and run on the target platform, without Pixi
- `--create-executable` gives one self-extracting file

<div class="ref"><a href="https://pixi.prefix.dev/latest/deployment/pixi_pack/" target="_blank">pixi-pack</a></div>

---
section: Exercise 3
layout: center
class: text-center
---

# Now it's your turn

## Exercise 3: Ready for your team

30 minutes · `cd exercises/03-collaboration`

<div class="text-left mx-auto" style="max-width: 34rem; margin: 1rem auto;">

1. `pixi global install gh`, put the workspace on GitHub
2. Add CI with `setup-pixi`, watch it go green
3. Build the Docker image and run it: no Pixi inside
4. Pack the environment, unpack it and run without Pixi

</div>

<small>

**prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/03-collaboration/**


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
