---
icon: lucide/lightbulb
---

# Why reproducibility matters

!!! abstract "15 minutes, presented"

    **Slides:** [Philosophy](../slides/)

    By the end of this block you should be able to explain, in your own words, why a robotics team
    ends up with "works on my machine" and what a lockfile does about it.

<!-- TODO(content): 15 min of narrative. Keep it opinionated and short — this is the only block
     without an exercise, so it has to earn its slot. -->

## Reproducible package management

<!-- TODO(content):
     - The robotics dependency problem: C++ libraries, drivers, Python, ROS, all at once.
     - What "reproducible" means concretely: same inputs -> same environment, on every machine.
     - Solve vs. install: the lockfile as the boundary between the two.
     - What apt/rosdep guarantee, and what they do not.
-->

## Development workflows

<!-- TODO(content):
     - The gap between the developer machine and the robot.
     - Environments per purpose: dev, test, deploy, simulation.
     - Why "activate the right shell" should not be a human responsibility.
-->

## Avoiding OS lock-in

<!-- TODO(content):
     - Where ROS's Ubuntu assumption comes from and what it costs.
     - Cross-platform teams: the macOS laptop, the Windows integrator, the aarch64 robot.
     - Containers as a deployment tool, not a development environment.
-->

## conda-forge + RoboStack

<!-- TODO(content):
     - conda-forge: what it is, its scale, how binaries get there.
     - RoboStack: ROS distributions as conda packages, which distros exist, how they are built.
     - How the two channels compose into one environment.
-->

## Takeaways

<!-- TODO(content): three bullets, the things we want people to repeat to a colleague next week. -->

---

Next up: [Pixi in 30 minutes](pixi-introduction.md).
