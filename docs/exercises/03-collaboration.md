---
icon: lucide/git-branch
---

# Exercise 3: Ready for your team

!!! plain "30 minutes, hands-on"

    **Work in:** `exercises/03-collaboration/` &middot; **Solution:** `solutions/03-collaboration/` &middot; **After:** [Collaboration, CI/CD & Docker](../explainers/collaboration.md)

    **Goal:** take the workspace to your team: a green CI run, a Docker image, and an archive you can unpack and run without Pixi.

Testing your workspace in CI or shipping your application with Docker is a natural next step.
Set up GitHub Actions, build a Docker image, then pack the environment for a machine without a container runtime.

Start in `exercises/03-collaboration/`.
This is a fresh workspace with prebuilt ROS 2 packages from RoboStack, not the local packages from Exercise 2.
The `talker` and `listener` tasks run the installed `demo_nodes_cpp` executables.
You don't need to compile any ROS packages for this exercise.

## 3.1 Set up GitHub

CI runs on GitHub, so your workspace needs to be a repository there.
The [GitHub CLI](https://cli.github.com) does that from the terminal, and it installs like any other tool.

!!! exercise "Your turn"

    1. Install the GitHub CLI, unless you have it already.
       Hint: Pixi installs tools outside your workspace too, with `pixi global install <tool>`.
    2. Log in with your GitHub account.
    3. Resolve this workspace to generate its `pixi.lock`.
       Exercise 3 is a separate workspace, so don't copy the lockfile from Exercise 2.
    4. Create a Git repository on the `main` branch, commit the workspace including `pixi.lock`, and push it to GitHub.

??? success "Solution"

    ```bash
    # 1
    pixi global install gh
    # 2
    gh auth login
    # 3
    pixi lock
    # 4
    git init -b main
    git add .
    git commit -m "ROS 2 workspace with Pixi"
    gh repo create ros-demo-team --source=. --push --public
    ```

## 3.2 Add CI

A minimal workflow is below: it checks out your repository and then stops.
Your job is the Pixi part, with the [`prefix-dev/setup-pixi`](https://pixi.prefix.dev/latest/integration/ci/github_actions/) action.
The workspace's `test` task runs `ros2 pkg executables demo_nodes_cpp`: it checks that ROS can find the installed package and lists its executables.
It doesn't start the nodes or check communication between them.

!!! exercise "Your turn"

    1. Create `.github/workflows/ci.yml` in your repository, starting from this skeleton:

        ```yaml title=".github/workflows/ci.yml"
        name: CI

        on:
          push:
            branches: [main]
          pull_request:

        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v7
              # Your turn: set up Pixi and run the tests.
        ```

    2. Add the Pixi setup with `locked: true`: install from the committed lockfile, and fail if it is missing or out of date.
    3. Run your `test` task in CI.
    4. Commit, push, and watch the Actions tab go green.

??? success "Solution"

    ```yaml title=".github/workflows/ci.yml"
    --8<-- "solutions/03-collaboration/ci-template.yml:workflow"
    ```

    `locked: true` makes setup-pixi run `pixi install --locked`, which fails if `pixi.lock` is missing or no longer matches the manifest.

    ```bash
    # 4
    git add .github/workflows/ci.yml
    git commit -m "Add CI"
    git push
    ```

## 3.3 Ship a Docker image

A deployment image should not contain a package manager, and it should not be able to drift from what the team tested.
The [pattern from the Pixi documentation](https://pixi.prefix.dev/latest/deployment/container/) does both with a multi-stage build: the build stage has Pixi and installs from the lockfile, the runtime stage only receives the finished environment plus an activation script baked by `pixi shell-hook`.

!!! exercise "Your turn"

    Complete the three `FIXME` lines in `exercises/03-collaboration/Dockerfile`.

    1. Replace the first `RUN pixi FIXME` with a locked install of the default environment.
       It must fail rather than re-solve if `pixi.lock` is missing or out of date.
    2. Replace the second `RUN pixi FIXME` with a Bash activation shell-hook written to `/shell-hook.sh`.
       Append `exec "$@"` to that script so it runs the container's command after activation.
    3. Complete `COPY --from=build FIXME` to copy `/app/.pixi/envs/default` from the build stage to the same absolute path in the runtime stage.
    4. Read your completed file: where is the lockfile enforced, and where does Pixi last run?
    5. Build the image.
    6. Run it, stop it with Ctrl+C, then check what the image weighs.

??? success "Solution"

    Check your three completed lines against this file:

    ```dockerfile title="exercises/03-collaboration/Dockerfile"
    --8<-- "solutions/03-collaboration/Dockerfile"
    ```

    The lockfile is enforced by `pixi install --locked`, the same refusal CI uses.
    Pixi's last appearance is the `pixi shell-hook` line: it writes the activation as a plain shell script, and the runtime stage copies only that script and the installed environment out of the build stage.

    ```bash
    # 5
    docker build -t ros-demo-team:latest .
    # 6
    docker run --rm ros-demo-team:latest
    # Stop the node with Ctrl+C before running the next command.
    docker images ros-demo-team
    ```

    The container runs `ros2 run demo_nodes_cpp talker` and logs `Publishing: 'Hello World: N'`, with `N` increasing.

## 3.4 Pack the environment


[`pixi-pack`](https://pixi.prefix.dev/latest/deployment/pixi_pack/) bundles an environment into `environment.tar`; `pixi-unpack` installs it without a solver or a network connection.
For this exercise, pack for your own machine and use a separate directory as the receiving machine.

!!! exercise "Your turn"

    1. Install `pixi-pack` and `pixi-unpack` as global tools.
    2. Check that the workspace's lockfile is up to date.
    3. Pack the **default** environment for your current platform.
       Hint: omit `--platform` to use the machine you are on.
    4. Keep `environment.tar` and the `unpacked/` directory you will create next out of Git: add both to your repository's `.gitignore`.

??? success "Solution"

    From `exercises/03-collaboration/`, outside a `pixi shell`:

    ```bash
    pixi global install pixi-pack pixi-unpack
    pixi lock --check
    pixi pack
    ```

    `pixi-pack` downloads the locked binary packages, including `demo_nodes_cpp`, and puts them in the archive.

    !!! note "Pack for the machine you will run on"

        The receiver must match the pack's OS and architecture and meet its system requirements.
        An `osx-arm64` pack does not run on Linux or an Intel Mac.
        All packages in this workspace are prebuilt, so you can also pack for another declared platform by downloading its packages.
        Use your own platform here so you can run the result locally.

## 3.5 Unpack and run without Pixi

The receiver needs the archive and the `pixi-unpack` binary, not your source tree, manifest or lockfile.
Install the unpacker before going offline.

!!! exercise "Your turn"

    1. Create an empty `unpacked/` directory and copy only `environment.tar` into it.
    2. Enter that directory, then unpack and activate the environment.
       Use the tab for your shell below.
    3. Check that `ros2` can find the `demo_nodes_cpp` executables.
    4. Run the talker directly with `ros2 run`, without `pixi run`.
       Wait for it to publish a few messages, then stop it with ++ctrl+c++.

??? success "Solution"

    Start in `exercises/03-collaboration/`, in a fresh terminal outside `pixi shell`.
    Choose one tab:

    === "Bash (Linux, macOS)"

        ```bash
        mkdir unpacked
        cp environment.tar unpacked/
        cd unpacked
        pixi unpack environment.tar
        source activate.sh
        ```

    === "Command Prompt (Windows)"

        Open **Command Prompt** (`cmd.exe`), not PowerShell, and navigate to the exercise directory first.
        A batch activation script changes the current environment in Command Prompt; running it from PowerShell would not activate your PowerShell session.

        ```bat
        mkdir unpacked
        copy environment.tar unpacked\
        cd unpacked
        pixi unpack --shell cmd environment.tar
        call activate.bat
        ```

    The remaining commands are the same in both shells:

    ```bash
    ros2 pkg executables demo_nodes_cpp
    ros2 run demo_nodes_cpp talker
    ```

    The executable list should contain `demo_nodes_cpp talker` and `demo_nodes_cpp listener`.
    The talker logs `Publishing: 'Hello World: N'`, with `N` increasing, and keeps running until you press ++ctrl+c++.
    It publishes without a listener running.

    `pixi-unpack` creates `env/` and a shell-specific activation script.
    Activation sets up the ROS environment; no Pixi process is involved in the `ros2` commands.
    If you need to move the deployment again, copy the archive and unpack it at the final location rather than moving the activated `env/` directory.

    Close this terminal when you are done so the unpacked environment does not leak into later commands.

## Going further

Finished early? Try these.

- Add a cheap gate: a first job that runs `pixi lock --check` and fails when someone edits `pixi.toml` without re-solving the lockfile. Break it on purpose to see it work.
- Extend the workflow to a matrix of Linux, macOS and Windows runners, like `.github/workflows/ci.yml` in this workshop's repository.
- Deploy to a GPU: the base image has CUDA variants like `ghcr.io/prefix-dev/pixi:noble-cuda-12.9.1`.
- Let CI update the lockfile for you: [update lockfiles with GitHub Actions](https://pixi.prefix.dev/latest/integration/ci/updates_github_actions/).
- Repeat the unpack in another empty directory with networking disabled.
  Copy both the archive and the platform's standalone `pixi-unpack` binary to a matching machine that has no Pixi installed.
- Try `pixi-pack --environment default --create-executable pixi.toml`.
  This includes the unpacker in a self-extracting file, so the receiver does not need to install it separately.

---

That is the workshop.
