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

- **Ruben Arts**, prefix.dev: Pixi
- **Wolf Vollprecht**, prefix.dev: RoboStack, mamba, conda-forge
- **Bas Zalmstra**, prefix.dev: rattler, the Rust conda libraries under Pixi

<br>

Three of us in the room. Raise your hand, we come to you.

<!--
15 min block with the setup check. Short intros: who you are, what you work on, and that all three of us are here for questions the whole session.
Ask the room: who runs ROS on Ubuntu, who on macOS or Windows, who brought their own workspace.
-->

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

<!--
Everybody did the homework: Pixi installed, repo cloned, packages cached. This one command proves it, from the cache, no Wi-Fi needed.
No turtle: Troubleshooting on the site, or grab one of us now, not in twenty minutes.
Also: a `source /opt/ros/.../setup.bash` in .bashrc shadows the Pixi environment, turn it off for today.
-->

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

# Getting into ROS is linked to an OS and a distro

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
- Editor, debugger, USB/network devices, GPU, GUI tools: much harder
- Setup once, never touch again
- You're not developing on your machine anymore


<img src="/docker-in-cloud.jpg" alt="Docker in Cloud: a container ship" style="position: absolute; right: 3rem; bottom: 3.2rem; height: 46%; z-index: 0; border-radius: 8px;">

<!--
Docker solved a real problem, that's why everybody does it now.
The cost is the development experience. You lose the flexibility of your own machine and every tool has to be wired through the container boundary.
Using ROS forces an OS, a version and a workflow on you. Good default, but it shouldn't be the only option.
-->

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

<!--
This is the dream, and the goal of this workshop. Compare it with the install page on docs.ros.org.
By Exercise 3 their own workspace does exactly this.
-->

---
section: Philosophy
layout: section
---

# How we get there

All machines · Distroless · Declarative · Reproducible · Fast · Simple

<!--
The overview, then one beat per item. Keep the pace up: 30 to 40 seconds each.
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 1/6</div>

# All machines

Linux, macOS, Windows. x86 and arm64.

- Not just Ubuntu, and not just the one Ubuntu that matches your distro
- Your laptop, the CI runner and the robot can all be different machines
- Pick the hardware you need, and the OS you like!

<!--
This is the routes table from earlier, solved. The person on a MacBook and the person on Arch work on the same project, today.
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 2/6</div>

# Distroless

Jazzy on Ubuntu 22.04. Kilted on macOS. Humble on Windows.

- A ROS distro is a release process, not an operating system
- There's no reason Humble should be tied to Ubuntu 22.04
- Any distro on any machine, and two of them side by side

<!--
RoboStack packages every distro for every platform, so the coupling between ROS release and OS release is just gone.
Side by side matters for migrations: you test Kilted next to Jazzy in the same repo, no second machine.
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 3/6</div>

# Declarative

Your environment is a file in git.

- `pixi.toml` says what you want
- Update your environment when you want
- Roll back to a known good state like you roll back code

<!--
Contrast with imperative setup: a README of steps run once, in an order nobody remembers, on a machine nobody can recreate.
The file is reviewable too: an environment change is a pull request, not a Slack message saying "reinstall".
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 4/6</div>

# Reproducible

A lockfile (pixi.lock) instead of a Docker image.

- Every package, version and hash, recorded when you change something
- The same environment on your laptop, in CI, on the robot
- Use `git` to manage your versions, not a container registry

<!--
The Docker image also gives reproducibility, but at the cost of the whole workflow moving into the container.
The lockfile gives the same guarantee as a text file in git, diffs included.
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 5/6</div>

# Fast

Minutes to a running project, not hours.

- Manage everything with one tool, no apt, no rosdep, no sourcing
- Let the internet connection be the only slow part, not the setup.
- Getting started: `git clone`, `pixi run sim`

<!--
Say the numbers out loud: a cold solve of 391 packages is about a second, an install from cache is seconds.
The first download is the only slow part, which is why the homework was warming the cache.
-->

---
section: Philosophy
---

<div class="kicker">How we get there · 6/6</div>

# Simple

If you can use `pip`, you can use Pixi.

- `pixi init`, `pixi add`, `pixi run`: the whole daily flow
- No apt, no rosdep, no sourcing, no `sudo`, no sysadmin knowledge
- Manage everything in one place, and reuse it across all your projects and devices.

<!--
The mental model is the same as pip or npm: a manifest, add things, run things.
What disappears is everything around it: apt for system deps, rosdep to glue them, the sourcing ritual. That's the "for everyone" of this block: the barrier to entry drops to knowing one tool.
-->

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

<!--
Not a container, not a virtualenv: a zip with compiled files plus a metadata file that says what it needs.
The dependency metadata is what a solver uses: rclcpp says it needs rcl, rcl says it needs rmw, and so on down to libc.
apt packages are the closest cousin, but apt installs into the system and one version per machine. Conda packages install into as many environments as you like.

The history: 2012, the scientific Python community. pip couldn't ship compiled code back then, and NumPy or SciPy needed C and Fortran compilers on every user's machine. Conda was the answer: ship the binaries, per platform. It has carried the compiled half of data science ever since, and conda-forge (2016) made it fully community run.
So this is not a new format we invented for robotics: Pixi and RoboStack reuse an ecosystem that has been shipping GPU and compiler stacks for over a decade.
That's the unit everything today is made of. conda-forge and RoboStack, next slide, are collections of these.
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

# Pixi introduction

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

Everything you need to know for now. It lives at the **root** of your project.

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

<!--
This is the `source setup.bash` you never type again. The RoboStack packages ship activation scripts, Pixi runs them on every activation.
[activation] is for your own additions: a script (the colcon overlay on the next slide) or plain environment variables like ROS_DOMAIN_ID.
Per platform with [target.win-64.activation], Windows gets a .bat.
pixi shell-hook is what Docker and CI use to activate without Pixi present.
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
The CUDA explainer on the site goes deeper. This is what 1.7 and 1.8 need.
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

From works on my machine to works on the team's.

<!--
15 min. The written version is docs/explainers/collaboration.md.
What changes when the workspace stops being yours: more platforms, a lockfile gate in CI, an image for the robot.
-->

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

<!--
Supporting a platform costs one line. The teammate gets what the lockfile pins for their platform, not whatever resolved on the day they joined.
[target.<platform>] for per-OS dependencies, tasks and activation (the setup.sh / setup.bat split from Exercise 1). when = "__cuda" for per-machine capability (Exercise 1 too).
-->

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

<!--
CI for a Pixi workspace is short because the hard question, what should be installed, is answered by the lockfile, not by CI configuration.
A failing CI run reproduces locally far more often: CI installs what the lockfile pins, and so do you.
More: `environments: default,kilted` to test two environments in one job, `global-dependencies: gcloud,awscli` for deploy tooling.
-->

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

<!--
That is the whole run() in src/main.ts: download, addPath, login, global install, pixi info, install (with cache restore and save around it), pixi list, activate, logout.
Cache: a hit means no install at all, so a CI run on an unchanged lockfile is seconds. cache-write lets you only save on main so the 10 GB cache limit lasts.
activate-environment writes pixi run's environment variables to GITHUB_ENV and its PATH changes to GITHUB_PATH, so later steps can call ros2 directly, no pixi run needed.
The token is only used for the install step and logged out afterwards, so it doesn't leak into later steps.
-->

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

<!--
Where there is a container runtime, the same lockfile becomes an image. The build stage is the only place Pixi exists.
CUDA base images exist too: ghcr.io/prefix-dev/pixi:noble-cuda-13.0.0. A cache mount on /root/.cache/rattler makes rebuilds fast.
-->

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

<!--
Why two stages: the build stage carries Pixi, the package cache and the source tree. None of that belongs on the robot.
The runtime stage copies out the environment directory and the one script, so the image is small and has nothing in it that could drift.
Every command in the container runs through shell-hook.sh, activated, the same way pixi run does it on your laptop.
-->

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

<!--
Someone edits pixi.toml and forgets to commit the lockfile. Without --locked that silently goes through and you ship an environment nobody ran.
With --locked the build tells you, right there, before anything is pushed.
-->

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

<!--
Robots on 4G, or with internet blocked: you can't pixi install there. pixi-pack takes one environment for one platform out of the lockfile and packs the .conda files as a local channel.
`pixi global install pixi-pack pixi-unpack`. --platform takes the conda subdir (linux-aarch64), not the name jetson.
Your own packages: `pixi publish --target-channel` uploads them to a channel so a teammate can pixi add them. We demo that, it needs a token.
-->

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

<!--
3.1 needs a GitHub account and gh auth login, say so up front.
The publish and pack steps are a demo from the front: both need a channel token, fifty people minting tokens is not a good use of twenty minutes.
-->

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
