---
icon: lucide/arrow-right-left
---

# Migrating from rosdep & colcon

## Generate a Pixi workspace with `pixi-ros`

You don't have to translate every dependency in your `package.xml` files by hand.
[`pixi-ros`](https://github.com/ruben-arts/pixi-ros) reads them and generates a `pixi.toml`, mapping dependencies to RoboStack and conda-forge packages.
It keeps colcon for building your source packages.

Install the helper:

```bash
pixi global install pixi-ros
```

From the root of your existing ROS workspace, initialize it for your ROS distro (Jazzy in this example):

```bash
pixi-ros init --distro jazzy
```

Review the generated `pixi.toml` and resolve any dependencies reported as `NOT FOUND` before building.
Packages that aren't available are commented out in the manifest, not installed.

```bash
pixi install
pixi run build
pixi run test
```

## Getting help

- [Pixi documentation](https://pixi.prefix.dev)
- [RoboStack](https://robostack.github.io) and its [GitHub organisation](https://github.com/RoboStack)
- The `#pixi` channel on [Discord](https://discord.gg/kKV8ZxyzY4)
- Missing a package in RoboStack?
  It is a pull request, and we will help you write it.
