---
icon: lucide/box
---

# Pixi in 30 minutes

!!! abstract "30 minutes, presented"

    **Slides:** [Pixi introduction](../slides/) &middot; **Followed by:** [Exercise 1](../exercises/01-ros-workspace.md)

    By the end of this block you should be able to read a `pixi.toml`, know which command to reach for, and know where the lockfile fits in.

You just heard why we want ROS to run anywhere.
This block is the how.
Everything here is something [Exercise 1](../exercises/01-ros-workspace.md) uses a few minutes later, so treat it as the warm-up, not a reference manual.
The actual reference is the [Pixi documentation](https://pixi.prefix.dev/).

## What is Pixi

Pixi is a package manager built on top of the conda ecosystem.

- `apt` is for Debian packages
- `brew` is for homebrew packages
- `pip` is for PyPI packages
- Pixi is for conda packages, and supports PyPI packages as a secondary source.

Conda packages are pre-built, cross-platform binary packages.
Pixi installs these in workspace specific virtual environments.

All Pixi documentation can be found at [https://pixi.prefix.dev/](https://pixi.prefix.dev/).

## The manifest, `pixi.toml`

Pixi workspaces' are declared in a single `pixi.toml` file.
It's located at the root of the workspace.
You declare where you want to get your dependencies from (`channels`), for which machines (`platforms`), what you want to install (`dependencies`), and what commands you want to run (`tasks`).

A minimal example:

```toml title="pixi.toml"
[workspace]
# Which platforms should be supported, and for which the lockfile will be generated.
platforms = ["linux-64", "osx-arm64", "win-64"]
# From which channels to get packages. conda-forge is the base, RoboStack is the ROS distro.
channels = ["conda-forge", "robostack-jazzy"]

# What conda packages to install. These are the ROS distro packages, but you can add any conda package here.
[dependencies]
ros-jazzy-ros-base = ">=0.11.0,<0.12"
ros-jazzy-turtlesim = ">=1.8.3,<2"

# What tasks you want to easily run. These are cross-platform commands that will be run in the workspace environment.
[tasks]
sim = "ros2 run turtlesim turtlesim_node"
```

### Dependencies and channels

Channels are where packages come from, like apt sources but written down in the workspace.
Dependencies are what you want from them.

```toml title="pixi.toml"
[workspace]
channels = ["conda-forge", "robostack-jazzy"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
ros-jazzy-ros-core = ">=0.11.0,<0.12"
```

A version spec like `>=0.11.0,<0.12` says what you accept.
The lockfile then pins the one exact version you got.

When you are missing dependencies you can use

- Use `pixi search "ros-jazzy-*"` to find packages in the channels you have configured.
- Use the search on [prefix.dev](https://prefix.dev) to search all packages.
- Look at the [RoboStack package list](https://robostack.github.io/lyrical.html) to see what ROS packages are available on RoboStack.

### Tasks

Tasks are cross-platform commands you define once and run by name.

```toml title="pixi.toml"
[tasks]
sim = "ros2 run turtlesim turtlesim_node"
```

```bash
pixi run sim
```

The commands you write for a task are run in the workspace environment.

??? "How does this work on all platforms?"
    The commands you write are not run with `bash` or `cmd`, they are run in a custom built-in shell that works on all platforms.
    It's called `deno_task_shell` and it's built into Pixi.
    It's a minimal shell, so not all commands (like `if`, `while`) in Bash will work, but the basic command running ones do.

    More details can be found in the [Pixi documentation](https://pixi.prefix.dev/latest/workspace/advanced_tasks/#our-task-runner-deno_task_shell).


Tasks support a graph style dependency system, so you can define a task that depends on another task.

```toml title="pixi.toml"
[tasks]
download-data = "curl -O https://example.com/data.zip"
build = "colcon build"
start = {
     cmd = "ros2 launch my_package my_launchfile.launch.py",
     depends-on = ["build", "download-data"],
}
```

This will first `build` your workspace, then `download-data`, and finally `start` your launchfile.

Want a task to only run once?
Add the `inputs` and `outputs` keys to the task, and Pixi will cache the result based on those files.

```toml title="pixi.toml"
[tasks]
download-data = {
    cmd = "curl -O https://example.com/data.zip",
    outputs = ["data.zip"],
}
```

Now Pixi will only run the `download-data` task if `data.zip` is missing, and will skip it if it already exists.

See the [Pixi documentation](https://pixi.prefix.dev/docs/tasks/) for more details and more task features.

### Environments

With Pixi you're not limited to just one environment per workspace or machine.
You can define multiple environments in the same `pixi.toml`, each with its own set of dependencies and tasks.
This allows you to create the right environment for the job, whether it's for development, testing, or deployment.

!!! note "Common reasons to split into multiple environments"
    - Support multiple ROS distros in the same workspace.
    - Tiny environments for a specific job, like generating documentation or running tests, without installing the full ROS distro.
    - Keep your deployment environment clean of testing and debugging tools to minimize the attack surface and reduce the size of your deployment.

=== "Multi distro"
     Setup an environment per ROS distro, and run the same command in each one.

    ```toml title="pixi.toml"
    [environments.jazzy]
    channels = ["conda-forge", "robostack-jazzy"]
    [environments.jazzy.dependencies]
    ros-jazzy-ros-core = "*"
    ros-jazzy-turtlesim = "*"

    [environments.humble]
    channels = ["conda-forge", "robostack-humble"]
    [environments.humble.dependencies]
    ros-humble-ros-core = "*"
    ros-humble-turtlesim = "*"

    [tasks]
    sim = "ros2 run turtlesim turtlesim_node"
    ```
    Since there are two environments, you need to tell Pixi which one to use when running a task.

    ```bash
    pixi run -e jazzy sim
    pixi run -e humble sim
    ```
=== "Specialized environments"

    Setup a separate environment that has one task, generating documentation, and only the dependencies needed for that task.
    ```toml title="pixi.toml"
    [environments.docs]
    no-default-feature = true # Required to avoid inheriting the default environment
    channels = ["conda-forge"]
    platforms = ["linux-64", "osx-arm64", "win-64"]

    [environments.docs.dependencies]
    zensical = "*"

    [environments.docs.tasks]
    build-docs = "zensical build --strict"
    ```

    Pixi will automatically figure out that the `build-docs` task has to be run in the `docs` environment
    ```bash
    pixi run build-docs
    ```

=== "Split environments"

    Split your environment into the default environment and the production environment.
    Here we're using features to define the dependencies for each environment, and then combining them in the `environments` section.
    `features` are a reusable way to define parts of an environment, and can be combined in different ways to create different environments.

    Using the `solve-group` option, you can tell Pixi to solve the dependencies as one group, so that only one version of each packages is installed, even if they are used in multiple environments.

    ```toml title="pixi.toml"
    [workspace]
    platforms = ["linux-64", "osx-arm64", "win-64"]
    channels = ["conda-forge", "robostack-jazzy"]

    # Main environment needed for all environments
    [feature.main.dependencies]
    ros-jazzy-ros-core = "*"
    ros-jazzy-turtlesim = "*"

    [feature.test.dependencies]
    pytest = "*"
    pytest-cov = "*"
    [feature.test.tasks]
    test = "pytest --cov=src"

    [environments]
    default = { features = ["main", "test"], solve-group = "one"}
    prod = {features = ["main"], solve-group = "one"}
    ```

    Pixi will find that the `test` task is only available in the `default` environment, and will run it there.
    ```bash
    pixi run test
    ```

## Command line interface

With the `pixi` command you can manage your workspace, install dependencies, and run tasks.


| Command | Description |
| --- | --- |
| `pixi init <workspace>` | Create a new workspace with a `pixi.toml` manifest. |
| `pixi add <package>` | Add a package to the workspace and update the lockfile. |
| `pixi update` | Update all packages in the workspace to the latest compatible versions and update the lockfile. |
| `pixi run <task>` | Run a task in the workspace environment. |
| `pixi shell` | Open a shell in the workspace environment. |

### Which one to use: `pixi run` vs `pixi shell`

Pixi has two ways to activate the workspace environment: `pixi run` and `pixi shell`.
Use `pixi run` to run a single command, or a Pixi task.
Use `pixi shell` to open a shell in the workspace environment, where you can run multiple commands.
In the ROS world, you're using the command line alot so it's recommended to use `pixi shell` to enter the environment and then run your commands from there.

You can use `pixi run` in a `pixi shell` session.

## The lockfile

`pixi.lock` holds the solved result: every package, version, and hash, for every platform in your manifest.
You commit it to git.
It changes when you change your dependencies, and Pixi updates it for you.

```yaml title="pixi.lock"
# This is an example of a lockfile generated by Pixi.
version: 7
platforms:
- name: linux-64
  virtual-packages:
  - __unix=0=0
  - __linux=4.18
  - __glibc=2.28
  - __archspec=0=x86_64
environments:
  default:
    channels:
    - url: https://conda.anaconda.org/conda-forge/
    packages:
      linux-64:
      - conda: https://conda.anaconda.org/conda-forge/linux-64/_openmp_mutex-4.5-20_gnu.conda
      - conda: https://conda.anaconda.org/conda-forge/linux-64/bzip2-1.0.8-hda65f42_9.conda
      - conda: https://conda.anaconda.org/conda-forge/linux-64/c-ares-1.34.8-hb03c661_0.conda
packages:
- conda: https://conda.anaconda.org/conda-forge/linux-64/markupsafe-3.0.3-py314h67df5f8_1.conda
  sha256: c279be85b59a62d5c52f5dd9a4cd43ebd08933809a8416c22c3131595607d4cf
  md5: 9a17c4307d23318476d7fbf0fedc0cde
  depends:
  - __glibc >=2.17,<3.0.a0
  - libgcc >=14
  - python >=3.14,<3.15.0a0
  - python_abi 3.14.* *_cp314
  constrains:
  - jinja2 >=3.0.0
  license: BSD-3-Clause
  license_family: BSD
  run_exports: {}
  size: 27424
  timestamp: 1772445227915
```

??? tip "Lockfile: To commit or not to commit?"
    **You should commit the lockfile to git**, so that everyone on your team gets the same environment.
    If you don't commit it, Pixi will have to regenerate the environment everytime you reinstall the workspace.

    It's always easier to throw it away than to try to recreate it when some dependency updated without you noticing.
    These things always tempt to break when you are preparing for a demo or a presentation.

    If you worry about stale dependencies, you can use `pixi update` or `pixi upgrade` to automate updates of your environment.
    More info on the [Pixi documentation](https://pixi.prefix.dev/latest/workspace/lock_file/#committing-your-lock-file).

## How to set up a workspace

This is the exact flow Exercise 1 walks through, so you will have seen it once already.

```bash
pixi init ros-workspace
cd ros-workspace
pixi workspace channel add robostack-jazzy
pixi add ros-jazzy-ros-core ros-jazzy-turtlesim
pixi run ros2 run turtlesim turtlesim_node
```

`init` creates the manifest, `workspace channel add` points it at the ROS packages, `add` writes the dependencies and solves them, and `run` executes a command in the environment.
A turtle appears.
That's it.

---

Now go do [Exercise 1: Your first ROS 2 workspace](../exercises/01-ros-workspace.md).
