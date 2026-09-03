---
icon: lucide/life-buoy
---

# Troubleshooting

## `pixi` is not found after installing

The installer puts `pixi` in `~/.pixi/bin` and adds that directory to your `PATH`, but only new shells pick that up.
Restart your terminal and check again:

```bash
pixi --version
```

Still not found?
Make sure `~/.pixi/bin` is on the `PATH` yourself, in your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.pixi/bin:$PATH"
```

On Windows the installer updates the user `PATH` in the registry.
Close Windows Terminal completely, all tabs, and open it again.

## The solver cannot find a ROS package

First make sure the `robostack-<distro>` channel is defined, before `conda-forge`:

```bash
pixi workspace channel add --prepend robostack-jazzy
```

Then check the name.
RoboStack packages are `ros-<distro>-<name>` with hyphens, so `rclcpp` is `ros-jazzy-rclcpp`.

If both are right, the package may simply not be built for your platform.
Search for it on [prefix.dev](https://prefix.dev/channels/robostack-jazzy) and check which platforms it is actually built for, or ask from the command line:

```bash
pixi search -c robostack-jazzy ros-jazzy-rclcpp
```

## A CUDA environment refuses to solve

A GPU build only resolves for a platform that has a CUDA version.
Make sure you add `cuda = "12"` to the platform you have CUDA on, `linux-64` or `win-64` for example:

```toml
[workspace]
platforms = [
    "osx-arm64",
    "win-64",
    { name = "cuda-linux-64", platform = "linux-64", cuda = "12" },
]
```

Or let Pixi write that for you:

```bash
pixi workspace platform add cuda-linux-64=linux-64 --cuda 12
```

Match the version to what `nvidia-smi` reports on the machine that has the GPU.

## An existing ROS installation interferes

A `source /opt/ros/jazzy/setup.bash` in your `~/.bashrc` leaks `ROS_DISTRO`, `AMENT_PREFIX_PATH` and `PYTHONPATH` into every Pixi environment, and the two installations mix.
Find the line:

```bash
grep -n "source /opt/ros" ~/.bashrc
```

Comment it out:

```bash
sed -i 's|^source /opt/ros|# &|' ~/.bashrc
```

Then restart your terminal.
Your system ROS is untouched, uncomment the line whenever you need it back.

## Linux: the turtlesim window does not appear

On modern desktop environments (GNOME, KDE, ...) a Qt GUI like `turtlesim` renders through Wayland. The conda-forge build of Qt needs its Wayland platform plugin as a separate package, so on `linux-64` add the `qt-wayland` dependency to your workspace:

You will notice the problem because `ros2 run turtlesim turtlesim_node` aborts with this warning:

```
qt.qpa.xcb: could not connect to display :0
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, minimal, minimalegl, offscreen, vnc, webgl, xcb.

[ros2run]: Aborted
```

You can add the dependency from the command line:

```bash
pixi add --platform linux-64 qt-wayland
```

Resulting in a `pixi.toml` like this:

```toml
# turtlesim's Qt window needs a platform plugin
[target.linux-64.dependencies]
qt-wayland = "*"
```

Then tell Qt to actually use that Wayland support by setting the platform environment variable in your workspace:

```bash
pixi workspace activation env set --target linux-64 QT_QPA_PLATFORM=wayland-egl
```

Resulting in a `pixi.toml` like this:

```toml
[target.linux-64.activation.env]
QT_QPA_PLATFORM = "wayland-egl"
```


## Windows: `Cannot open include file` or `failed to persist temporary file`

Windows caps most file paths at 260 characters, and a ROS environment nests deep.
If your build stops with `error C1083: Cannot open include file` on a header that clearly exists, or an install fails with `failed to persist temporary file: The system cannot find the path specified`, your workspace folder sits too deep on the disk.

Two ways out, either works:

Move the workspace closer to the drive root, `C:\ws` beats `C:\Users\you\Documents\workshops\roscon-2026\...`.

Or tell Pixi to keep its environments somewhere short, once, for every workspace:

```powershell
pixi config set --global detached-environments 'C:\pix'
```

## Something is slow

First check if it is an internet issue: the first download of a ROS environment is a few gigabytes, and conference Wi-Fi is shared with the whole room.
If nothing is moving anymore, cancel and restart the command.
Pixi keeps everything it already downloaded in its cache, so it continues where it stopped.

---

Not here?
Ask in the room, or open an issue on [GitHub](https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi/issues) so the next person finds the answer.
