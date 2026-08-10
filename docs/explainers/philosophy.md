---
icon: lucide/lightbulb
---

# Robotics for everyone

!!! abstract "15 minutes, presented"

    **Slides:** [Philosophy](../slides/)

    By the end of this block you should be able to explain why robotics has such a high bar to entry today, and how reproducible, cross-platform environments lower that bar so more people can build robots.

Ask someone new to robotics to get a ROS project running and watch what happens.
They pick the wrong Ubuntu, or they are on a Mac and there is no clear path, or they follow a wiki page that was right two years ago.

!!! note "The routes into ROS today (without RoboStack or Pixi)"

    Say you just want to try ROS 2.
    Your path depends entirely on the machine you happen to own:

    - **Ubuntu 24.04:** install Jazzy from apt, you are on the happy path.
    - **Ubuntu 22.04:** you get Humble. Need Jazzy instead? Upgrade or reinstall your OS.
    - **Another Linux (Arch):** build from source, or run an Ubuntu container.
    - **macOS:** no official path. Spin up a Linux VM or a Docker image.
    - **Windows:** limited support, build from source, or reach for WSL2 or Docker.

Right now there is basically one answer to this: stop fighting your own machine and move development into a VM or a Docker image.
And to be fair, that works.
It makes the setup doable, and everyone on the team can share the same image.
But you're not getting a "normal" development experience where you can just run things locally on your machine.
Your whole workflow now lives inside a box, and you lose the flexibility of your own machine.

Using ROS forces you into a specific OS, a specific version, and a specific workflow.
This might be a good start for most robotics projects but for sure not all.
ROS is missing out on a lot of users due to this lock-in.

## The philosophy of Pixi and RoboStack

Pixi together with RoboStack take a different approach.

- All machines, not just Ubuntu.
- Reproducible, share it with your team without requiring a Docker Image.
- Declarative, use version control to roll back to a known good state.
- Fast, to get started in minutes instead of hours.
- Flexible, use the latest greatest, or pin to a known good version.

Giving control back to the developer, instead of depending on the ecosystem dictating how you should work.

!!! tip "Our dream, and goal for this workshop"
    We want everyone to be able to run a ROS project with just three commands:

    ```bash
     git clone <your-project>
     cd <your-project>
     pixi run application
     # Installs your full ROS environment
     # Runs the right launchfile for your project
    ```

    Instead of this: [docs.ros.org](https://docs.ros.org/en/lyrical/Installation/Ubuntu-Install-Debs.html)

### Cross-platform

RoboStack is focused on making ROS work on Linux, macOS, and Windows.
There is a huge list of packages available on [all major platforms](https://robostack.github.io/lyrical.html).
Making it possible for anyone to join without first having to understand Ubuntu, Docker, or WSL2.

This is extended with Pixi, which has the ability to manage multiple platforms from a single project file.
Making it possible to use the same project file, and CLI commands to run your ROS application on any machine.

![Pixi and RoboStack cross-platform](https://user-images.githubusercontent.com/5497832/129636748-67ece961-f762-4440-a95f-c097012fac3f.jpg)

### Distroless

We don't believe in distro lock-in.
To us it's just a release process but there is no reason ROS2 Humble should be tied to Ubuntu 22.04, or ROS2 Lyrical to Ubuntu 26.04.
RoboStack packages ROS2 for all distro's but that means that you can run any distro on any machine.

!!! tip "No more distro lock-in"
    - ROS2 Lyrical on Ubuntu 24.04 :heavy_check_mark:
    - ROS2 Lyrical on macOS 15 :heavy_check_mark:
    - ROS2 Humble on Windows 11 :heavy_check_mark:
    - ROS2 Kilted on Ubuntu 26.04 :heavy_check_mark:
    - Any mix of these should work!

### Project focused

Pixi allows you to declare your entire ROS environment in a single `pixi.toml` file, including system libraries, Python packages, and ROS nodes.
The lockfile guarantees that anyone who checks out your project can recreate the same environment, on any machine, without having to know the details of how to set it up.
This creates a fully reproducible environment for your project, and makes it easy to share with others.

!!! tip "Not breaking your system ever again"
     Pixi installs everything in a project-specific environment, so you never have to worry about breaking your system or conflicting with other projects.
     You can have multiple projects with different ROS versions and dependencies on the same machine, without any conflicts.

### Flexible dependency management

RoboStack is build on top of conda-forge, which is a huge collection of pre-built, cross-platform binary packages.
This means that you can use any package from conda-forge in your ROS project, and you can also use any package from RoboStack in your conda-forge project.
This allows you to mix and match dependencies from both ecosystems, and gives you the flexibility to use the best tool for the job, without being locked into a specific distribution or package manager.

!!! tip "Mix and match dependencies"
    - Use any package from conda-forge in your ROS project.
    - Use any package from RoboStack in your conda-forge project.
    - No more distro lock-in, no more dependency hell.

### Standing on conda-forge and RoboStack

None of this would work without an enormous amount of community effort underneath it.
[conda-forge](https://conda-forge.org) is a huge, community-run collection of pre-built, cross-platform binary packages, tens of thousands of them, already compiled for Linux, macOS, and Windows.
That is the base layer.

RoboStack builds on conda-forge and packages the ROS distributions themselves as conda packages, so you can install ROS the same way you install anything else, on any of those platforms.
It is maintained by people like [Tobias Fischer](https://github.com/Tobias-Fischer), [Silvio Traversaro](https://github.com/traversaro), and [Daisuke Nishimatsu](https://github.com/wep21), and it is genuinely hard work to keep ROS compiling across multiple operating systems.
The two channels compose into a single environment: conda-forge for most dependencies, RoboStack for the ROS parts.

---

Next up: [Pixi in 30 minutes](pixi-introduction.md).
