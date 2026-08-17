---
icon: lucide/users
---

# Collaboration, CI/CD & Docker

!!! abstract "15 minutes, presented"

    **Slides:** [Prepare for collaboration](../slides/) &middot; **Followed by:** [Exercise 3](../exercises/03-collaboration.md)

    By the end of this block you should know what changes when the workspace stops being yours and starts being your team's.

Let's now move beyond "Works on my machine", and make sure it works on your teammate's machine, in CI, and in a Docker image you can deploy to a robot.

## Many platforms, one manifest

Your workspace so far lists the platforms it supports.
Adding one line is what supporting a new platform costs:

```bash
pixi workspace platform add linux-64 osx-arm64 win-64
```

Pixi re-solves the dependencies for each platform separately and records all of them in the same lockfile.
From that moment a teammate's setup is `git clone`, `pixi install`, done: they get the environment the lockfile pins for their platform, not whatever resolved on the day they joined.

Platforms differ, and the manifest has two tools for that:

- A `[target.<platform>]` table overrides dependencies, tasks or activation for one platform, like the `install/setup.bat` versus `install/setup.sh` split from Exercise 1.
- A conditional dependency picks per machine capability, like the `when = "__cuda"` PyTorch split from Exercise 2.

One honest caveat: "it solved" proves the packages exist and agree with each other on every platform.
It does not prove your node runs there.
That is what CI is for.

## CI/CD

CI for a Pixi workspace is short, because the hard question, "what should be installed?", was answered by the lockfile, not the configuration in CI.
[`prefix-dev/setup-pixi`](https://pixi.prefix.dev/latest/integration/ci/github_actions/) installs Pixi, installs from the lockfile, and refuses if the lockfile is stale:

```yaml
- uses: prefix-dev/setup-pixi@v0.10.0
- run: pixi run test
```

The same task names you use locally are the CI script.
There is no second set of setup instructions living in YAML that can drift from what developers do.
The amount of times failing CI will actually be reproducible locally goes up dramatically, because the CI environment is exactly what the lockfile pins, and so is your local machine.

!!! tip "The cache key is your lockfile"

    setup-pixi caches the installed environment keyed on a hash of `pixi.lock`.
    Unchanged lockfile means a cache hit, and a cache hit means CI can reuse an existing environment instantly.

Some more notable features of the GitHub Actions integration:

You can tell the action to install multiple environments, this helps with properly caching the environments in the CI runner, and allows you to run tests in multiple environments in one job:

```yaml
- uses: prefix-dev/setup-pixi@v0.10.0
  with:
    environments: default,kilted
- run: pixi run test --environment default
- run: pixi run test --environment kilted
```

You can add some dependencies that are only needed in CI, as global environments, for example `gcloud` or `awscli` for deployment.

```yaml
- uses: prefix-dev/setup-pixi@v0.10.0
  with:
    global-dependencies: gcloud,awscli
- run: gcloud auth activate-service-account --key-file ${{ secrets.GCP_KEY }}
- run: aws configure set aws_access_key_id ${{ secrets.AWS_ACCESS_KEY_ID }}
```

## pixi-pack: ship the environment itself

Shipping to robots is a different problem sometimes, all of us had to deal with a deployment of some code that was not yet fully managed by a fleet management system and you just need to dump an environment somewhere very remote. 4G connections are unreliable, internet access on the devices is blocked off etc.

[`pixi-pack`](https://pixi.prefix.dev/latest/deployment/pixi_pack/) can help you wrap up the environment into a single archive that you can copy to the robot and unpack there, without any network or package manager needed on the robot. Perfect for testing, and huge potential to automate and simplify deployment of your ROS application to a fleet of robots.

[`pixi-pack`](https://pixi.prefix.dev/latest/deployment/pixi_pack/) takes one environment for one platform out of your lockfile and packs the actual packages into a single archive:

```bash
pixi global install pixi-pack pixi-unpack
pixi-pack --environment default --platform linux-aarch64 pixi.toml
```

The resulting `environment.tar` contains the `.conda` files themselves, laid out as a local channel.
Copy it to the robot over `scp`, a USB stick, whatever reaches it, and unpack:

```bash
pixi-unpack environment.tar
source activate.sh
```

That recreates the environment in `./env` and writes an `activate.sh`, with no Pixi, conda or network needed on the robot.
And because packing only downloads files, you pack for the Jetson from your Mac, the same cross-platform trick as solving.

!!! tip "One file, batteries included"

    `pixi-pack --create-executable` produces `environment.sh`: a single self-extracting file that carries the unpacker inside it.
    Run it on the robot and you get the environment, even without `pixi-unpack` there.

If you build your own packages, `--inject my-package.conda` adds them to the pack on top of what the lockfile pins.

## Docker

Where there is a container runtime, the same lockfile becomes an image.
The [pattern from the Pixi documentation](https://pixi.prefix.dev/latest/deployment/container/) is a two-stage build:

```dockerfile
FROM ghcr.io/prefix-dev/pixi:0.76.2-noble AS build

WORKDIR /app
COPY . .
RUN pixi install --locked
RUN pixi shell-hook -s bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:24.04 AS runtime

COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh
WORKDIR /app
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
```

Two lines carry the idea.
`pixi install --locked` fails the image build if the lockfile does not match the manifest, so the image cannot silently contain something the team never tested.
`pixi shell-hook` writes the environment activation into a plain shell script, so the runtime stage needs no Pixi at all: it receives the finished environment and nothing else.

!!! tip "The image is the lockfile, again"

    Laptop, CI and image now install from the same `pixi.lock`.
    "It worked in the container but not on my machine" stops being a category of bug and starts being a diff of one file.

Two closing notes for the road:
the base image has CUDA variants (`ghcr.io/prefix-dev/pixi:noble-cuda-13.0.0`) for GPU deployments, and rebuilds go much faster when you keep Pixi's package cache between builds with a mount: `RUN --mount=type=cache,target=/root/.cache/rattler pixi install --locked`.

---

Now go do [Exercise 3: Ready for your team](../exercises/03-collaboration.md).
