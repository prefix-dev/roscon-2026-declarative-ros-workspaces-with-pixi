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

<!--
Presenter notes live in comments like this one.

Structure of this deck: one `section:` per agenda block, so the footer always shows where we are.
Each presented block ends with a "Now it's your turn" slide that hands over to the exercise.
-->

---
layout: intro
section: Welcome
---

# Who we are

<!-- TODO(content): 15 min block: three short intros and the setup check. -->

- **Ruben Arts:** prefix.dev
- **Wolf Vollprecht:** prefix.dev
- **Bas Zalmstra:** prefix.dev

---
section: Welcome
---

# Today

<div class="schedule">

| | | |
| --- | --- | --- |
| 15 min | Welcome and setup | together |
| 15 min | Robotics for everyone | we talk |
| 30 min | Pixi in 30 minutes | we talk |
| 30 min | **Exercise 1:** your first ROS 2 workspace | you type |
| 30 min | CUDA | we talk |
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

<!-- TODO(content): the QR code to the site, and the one command that proves their setup works. -->

---
section: Philosophy
layout: section
---

# Robotics for everyone

Why the way we install ROS keeps people out.

<!--
15 min. The written version is docs/explainers/philosophy.md.
This block is the why, the rest of the day is the how. It's allowed to persuade; the exercises are not.
-->

---
section: Philosophy
---

# Getting into ROS depends on the machine you own

| You have | Your route |
| --- | --- |
| Ubuntu 24.04 | `apt install`, the happy path |
| Ubuntu 22.04 | Humble only. Want Jazzy? Reinstall your OS |
| Arch or another Linux | Build from source, or a container |
| macOS | No official path. VM or Docker |
| Windows | Limited support, WSL2 or Docker |

<!--
Ask someone new to robotics to get a ROS project running and watch what happens.
Before they touch a robot they first have to learn a lot about apt, bash and OS installation.
Frameworks like lerobot and dora are much more cross-platform, and easier to start with. ROS doesn't have to lose those people.
-->

---
section: Philosophy
---

# "Just use Docker" is the accepted answer

And to be fair, it works.

- The setup becomes doable, and the team shares one image
- But your whole workflow now lives inside a box
- Your editor, your debugger, your USB devices, your GUI tools: all harder
- You're not developing on your machine anymore

<!--
This is the honest slide: Docker solved a real problem, that's why everybody does it.
The cost is the development experience. You lose the flexibility of your own machine and every tool has to be wired through the container boundary.
Using ROS forces an OS, a version and a workflow on you. Good default, but it shouldn't be the only option.
-->

---
section: Philosophy
---

# What we want instead

```bash
git clone <your-project>
cd <your-project>
pixi run application
```

Any machine, three commands, and the third one installs the full ROS environment and starts your launchfile.

<!--
This is the dream, and the goal of this workshop. Compare it with the install page on docs.ros.org.
By Exercise 3 their own workspace does exactly this.
-->

---
section: Philosophy
---

# How we get there

- **All machines**, not just Ubuntu: Linux, macOS, Windows, x86 and arm64
- **Distroless**: Jazzy on Ubuntu 22.04, Kilted on macOS, Humble on Windows
- **Declarative**: the environment is a file in git, roll back to a known good state
- **Reproducible**: a lockfile instead of a Docker image
- **Fast**: minutes to a running project, not hours
- **Simple**: if you can use `pip`, you can use Pixi

<!--
Distroless: to us a ROS distro is a release process, not an OS. There's no reason Humble should be tied to Ubuntu 22.04.
Simple: no sysadmin knowledge needed. `pixi init`, `pixi add`, `pixi run`, that's the same mental model as pip, and it replaces apt, rosdep and the sourcing.
Declarative: pixi.toml says what you want, the lockfile records what you got, git carries both.
Flexible too: latest greatest or pinned, your call. Control back to the developer.
-->

---
section: Philosophy
---

# Standing on conda-forge and RoboStack

- **conda-forge**: tens of thousands of pre-built packages, community run
  <br>`gcc`, `cmake`, `Python`, `OpenCV`, `PyTorch`, for every platform
- **RoboStack**: the ROS distributions built on top of it
  <br>Noetic to Lyrical, `ros-noetic-rqt` to `ros-lyrical-plotjuggler`
- One environment, both channels: conda-forge for the stack, RoboStack for ROS

<!--
None of this works without the community effort underneath.
RoboStack is maintained by people like Tobias Fischer, Silvio Traversaro and Daisuke Nishimatsu, and keeping ROS compiling on three operating systems is genuinely hard work.
Credit them by name. This workshop stands on their shoulders.
-->

---
section: Pixi
layout: section
---

# Pixi in 30 minutes

The basics you need for Exercise 1.

<!--
30 min. The written version is docs/explainers/pixi-introduction.md.
Everything on these slides comes back in Exercise 1 a few minutes later, so keep it concrete: show the file, show the command, move on.
-->

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

<!--
Conda packages are pre-built binaries for Linux, macOS and Windows. PyPI packages work too, as a secondary source.
Nothing lands in /opt, /usr or your system Python. Two projects, two environments, they don't get in each other's way.
Docs: pixi.prefix.dev
-->

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

<!--
We've all done this. Just name it and move on.
-->

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

Everything you need to know for now. It lives at the root of your project.

<div class="ref"><a href="https://pixi.prefix.dev/latest/reference/pixi_manifest/" target="_blank">Manifest reference</a></div>

<!--
Three tables. Everything else today is a variation on this.
channels: where the packages come from. platforms: which machines you solve for.
dependencies: what you want, and which versions you accept. tasks: commands with a name, run inside the environment.
Open the Exercise 1 solution manifest if you want a real one on screen.
-->

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

<!--
The same two-repo setup everybody already has on Ubuntu: the OS repos plus packages.ros.org, except here it is declared in the manifest instead of /etc/apt/sources.list.d/.
`pixi workspace channel add --prepend robostack-jazzy`, then `pixi add ros-jazzy-ros-base`.
The RoboStack channel has to come before conda-forge, that's what --prepend does.
A version like ">=0.11" is what you accept, the lockfile is what you got.
Looking for a package: `pixi search "ros-jazzy-*"`, prefix.dev, or the RoboStack package list.
-->

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

<!--
The everyday flow is init, add, run. That's it for most days.
pixi install is what CI and a fresh clone do: no solving, it installs exactly what the lockfile says.
Every command has --help, and tab completion is one line: `pixi completion --shell zsh >> ~/.zshrc` (bash, fish, powershell too).
`pixi list` shows what is installed, `pixi search` finds packages, `pixi info` tells you about the workspace and the machine.
-->

---
section: Pixi
---

# The README everybody copies from

```md
## How to run
1. source /opt/ros/jazzy/setup.bash
2. rosdep install --from-paths src -y
3. colcon build --symlink-install
4. source install/setup.bash
5. ros2 launch my_robot bringup.launch.py
```

- Skip step 1: `rosdep: command not found`
- Skip step 4: `Package 'my_robot' not found`
- Forget step 2 on a fresh machine and you debug the wrong thing for an hour

<br>

Five steps you have to get right, in order, every time. That's the setup we skip: `pixi run bringup`.

<!--
Every repo has this section. It is the real interface of the project, and it only works when you follow it exactly.
Miss one line and the workspace does not do what it is for, and the error rarely points at the line you missed.
Tasks move these steps into pixi.toml: named, in the right order, run inside the right environment on every platform.
The README then says: `pixi run bringup`.
-->

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

<!--
Tasks run inside the environment. Pixi has a small built-in shell, so a task you write on Linux runs on Windows too.
depends-on chains tasks, inputs/outputs skip a task when its result is already there.
`pixi task add sim "..."` writes the task for you.
-->

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

<!--
In ROS you live on the command line, so most people use `pixi shell` and run their ros2 commands from there.
`pixi run` is for one command, or a task, or from a script and CI.
No sourcing: activation happens when the shell starts, and it is gone when you exit.
-->

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

<!--
Exercise 1 builds a C++ node with colcon inside the Pixi environment. Same as always, and it leaves build/ install/ log/ behind.
The overlay is sourced through an activation script (install/setup.sh, install/setup.bat on Windows).
This is on purpose the "before" state. Exercise 2 replaces it.
-->

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

<!--
The distro specific parts move into the environment. Tasks, ros-dev-tools and the activation stay at workspace level, every environment gets them.
Solving a second full ROS distro takes about a second. Show it.
-->

---
section: Pixi
---

# Solve for machines you don't have

- `platforms`: Pixi solves for all of them, you install where you need it
- A named platform describes a machine: `jetson` is `linux-aarch64` with CUDA 13
- `pixi list --platform jetson`, from your laptop

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/multi_platform_configuration/" target="_blank">Multi-platform configuration</a></div>

<!--
`pixi workspace platform add jetson=linux-aarch64 --cuda 13`, then `pixi list --platform jetson` on a MacBook gives you the Jetson environment without owning one.
Solving is cheap and runs anywhere. Installing is the expensive part, and you only do that where it runs.
How the solver knows about the GPU: next two slides.
-->

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

<!--
Pixi detects them on the machine it runs on: kernel, glibc, macOS version, CPU architecture, and the CUDA driver.
Packages on conda-forge depend on them, that is how the solver knows a GPU build fits.
For a platform you solve but do not run on, you write down what that machine reports. Next slide.
-->

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

<!--
Install the NVIDIA driver with apt (or JetPack on a Jetson), check with nvidia-smi. That is the only system dependency.
The CUDA toolkit, cuDNN, PyTorch's GPU build: all conda packages, pinned in the lockfile like everything else.
A Jetson is the same idea: `pixi workspace platform add jetson=linux-aarch64 --cuda 13`.
`[target."cuda-*"]` gives you tasks and dependencies only for the CUDA platforms.
The CUDA block after the exercise goes deeper. This is what 1.7 and 1.8 need.
-->

---
section: Pixi
---

# The lockfile

- `pixi.lock` has every package, version and hash
- For every platform and every environment
- Pixi writes it, you commit it
- `pixi install --locked` in CI, so nothing changes without you noticing

<div class="ref"><a href="https://pixi.prefix.dev/latest/workspace/lock_file/" target="_blank">The lockfile</a></div>

<!--
It changes when the manifest changes, `pixi update` moves it forward when you want that.
--locked refuses to run when manifest and lockfile don't match.
Commit it. Recreating a lockfile is easy, recreating the environment that worked last week is not.
-->

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

<!--
Do this live if the Wi-Fi allows it, the packages are in the cache from the homework.
The cheat sheet has every command with its flags, point at it once.
-->

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

<!--
Every step has the commands folded away under "Solution" on the page. Ask them to try first.
People with their own workspace: do the same steps on your own project, that's more useful than the turtle.
-->
---
section: Packaging
layout: center
---

# Building ROS packages with Pixi

No colcon, no sourcing.

<!--
Written version: docs/exercises/02-ros-package.md and pixi.prefix.dev/latest/build/ros/.
They need to understand three things: what a package manifest is, why the workspace depends on a path, and what happens on `pixi run` after that.
-->

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

<!--
Everybody here has forgotten to source at least once this month.
Your node is a different kind of thing than turtlesim: one is a package, the other is an overlay.
Pixi can build your package and install it like any other dependency, then all of this goes away.
-->

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

<!--
Until now every pixi.toml had a [workspace] table. A package manifest has [package] and no [workspace]: how to build one package.
It's tiny, because the build backend does the reading. Next slide.
-->

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

<!--
Pixi's side of the deal: solve the dependencies, set up an isolated build environment, cache the result.
The backend's side: know the build system, turn the source into a conda package.
Separating them is what keeps the package manifest at two lines: all the build-system knowledge lives in the backend, not in your file.
They come from conda-forge like everything else, and pinning them in [workspace.dependencies] is why your build is reproducible too.
Today we only need pixi-build-ros: next slide.
-->

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

<!--
The backend is the part that knows the build system. CMakeLists.txt and setup.py stay as they are.
It installs into lib/<package>/, so ros2 run finds the node like any other package.
Sibling packages in the workspace are found automatically. Version constraints in package.xml are ignored, conditional dependencies are not fully supported yet.
-->

---
section: Packaging
---

# What you write

### In the workspace `pixi.toml`

- `preview = ["pixi-build"]`
- `pixi-build-ros = ">=0.7.2"` under `[workspace.dependencies]`
- `ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }`

### In `src/turtle_dancer/pixi.toml`

- `name = "pixi-build-ros"` and `workspace = true` under `[package.build.backend]`

<div class="ref"><a href="https://pixi.prefix.dev/latest/build/ros/" target="_blank">Building ROS packages with Pixi</a> · <a href="https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/02-ros-package/" target="_blank">Exercise 2</a></div>

<!--
Three lines in the workspace: turn on the preview, name the backend once in [workspace.dependencies], depend on your package by path.
The dependency name is the package.xml name with the distro prefix. Path dependencies you write by hand, pixi add doesn't do them.
Two lines in the package: which backend, and workspace = true to take the version from the workspace.
The rest of the exercise is deleting things.
-->

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

<!--
`pixi list` shows the path it was built from where the other packages show a channel.
Change the angular speed in dance.cpp and run again, the turtle turns differently. No build command in between.
C++ sources are watched by default. Python sources are not yet in backend 0.7.2, `extra-input-globs = ["**/*.py"]` in the package manifest fixes that. The exercise page says so in 2.6.
-->

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

<!--
The backend brings its own toolchain for the build, so ros-dev-tools can go.
Same packages, one step further: `pixi publish --path src/turtle_dancer --target-dir output` gives you a .conda file another workspace can pixi add. Upload it to a channel and a teammate never builds it. Exercise 3 shows that.
-->

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

<!--
Step 5 is the payoff, make sure everybody gets there.
People with their own workspace: this is the most useful ten minutes of the day for them. Expect failures, mostly a package.xml dependency that isn't on RoboStack.
-->
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

We are here for the rest of the conference.
Bring us your workspace.
