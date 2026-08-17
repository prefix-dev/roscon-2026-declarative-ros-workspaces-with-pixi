---
icon: lucide/git-branch
---

# Exercise 3: Ready for your team

!!! plain "20 minutes, hands-on"

    **Work in:** `exercises/03-collaboration/` &middot; **Solution:** `solutions/03-collaboration/` &middot; **After:** [Collaboration, CI/CD & Docker](../explainers/collaboration.md)

    **Goal:** take the workspace to your team: a green CI run and a Docker image they can deploy.

Testing your workspace in CI or shipping your application with Docker is a natural next step.
Let's setup GitHub Actions to run your tests and build a Docker image from the environment you can deploy.

## 3.1 Set up GitHub

CI runs on GitHub, so your workspace needs to be a repository there.
The [GitHub CLI](https://cli.github.com) does that from the terminal, and it installs like any other tool.

!!! exercise "Your turn"

    1. Install the GitHub CLI, unless you have it already.
       Hint: Pixi installs tools outside your workspace too, with `pixi global install <tool>`.
    2. Log in with your GitHub account.
    3. Turn your workspace into a repository on GitHub.

??? success "Solution"

    ```bash
    # 1
    pixi global install gh
    # 2
    gh auth login
    # 3
    git init
    git add .
    git commit -m "ROS 2 workspace with Pixi"
    gh repo create turtle-workspace --private --source=. --push
    ```

## 3.2 Add CI

A minimal workflow is below: it checks out your repository and then stops.
Your job is the Pixi part, with the [`prefix-dev/setup-pixi`](https://pixi.prefix.dev/latest/integration/ci/github_actions/) action.

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
              - uses: actions/checkout@v4
              # Your turn: set up Pixi and run the tests.
        ```

    2. Add the Pixi setup: install from the lockfile, exactly what it pins.
    3. Run your `test` task in CI.
    4. Commit, push, and watch the Actions tab go green.

??? success "Solution"

    ```yaml title=".github/workflows/ci.yml"
    --8<-- "solutions/03-collaboration/ci-template.yml:workflow"
    ```

    `locked: true` makes setup-pixi run `pixi install --locked`, which errors instead of re-solving when someone edited `pixi.toml` and forgot the lockfile.

    ```bash
    # 4
    git add .github/workflows/ci.yml
    git commit -m "Add CI"
    git push
    gh run watch
    ```

## 3.3 Ship a Docker image

A deployment image should not contain a package manager, and it should not be able to drift from what the team tested.
The [pattern from the Pixi documentation](https://pixi.prefix.dev/latest/deployment/container/) does both with a multi-stage build: the build stage has Pixi and installs from the lockfile, the runtime stage only receives the finished environment plus an activation script baked by `pixi shell-hook`.

!!! exercise "Your turn"

    1. Read the provided `Dockerfile`: find where the lockfile is enforced, and find the last line where Pixi still exists.
    2. Build the image.
    3. Run it, then check what the image weighs.

??? success "Solution"

    ```dockerfile title="solutions/03-collaboration/Dockerfile"
    --8<-- "solutions/03-collaboration/Dockerfile"
    ```

    The lockfile is enforced by `pixi install --locked`, the same refusal CI uses.
    Pixi's last appearance is the `pixi shell-hook` line: it writes the activation as a plain shell script, and the runtime stage copies only that script and the installed environment out of the build stage.

    ```bash
    # 2
    docker build -t turtle-dancer:latest .
    # 3
    docker run --rm turtle-dancer:latest
    docker images turtle-dancer
    ```

## 3.4 Share the environment

Deployment is not always a Docker host.
Two more ways to hand your work to others, shown as a demo up front rather than hands-on, because both need a channel token and fifty people minting tokens is not a good use of twenty minutes:

- [`pixi publish`](https://pixi.prefix.dev/latest/reference/cli/pixi/publish/) builds the workspace's packages into `.conda` files and uploads them to a channel, so a teammate can `pixi add` your package like any other. In CI it is one more job with a single `pixi publish --target-channel` step.
- [`pixi-pack`](https://pixi.prefix.dev/latest/deployment/pixi_pack/) packs a locked environment into a single archive you can copy to a robot that has no network, and unpack there without any package manager.

The full recipes are on the [migration page](../reference/migration.md), written to be read after the workshop.

## Check your work

```bash
gh run list                      # the CI run on your repository is green
docker run --rm turtle-dancer    # the image runs, and there is no pixi in it
```

## Going further

Finished early? Try these.

- Add a cheap gate: a first job that runs `pixi lock --check` and fails when someone edits `pixi.toml` without re-solving the lockfile. Break it on purpose to see it work.
- Extend the workflow to a matrix of Linux, macOS and Windows runners, like `.github/workflows/ci.yml` in this workshop's repository.
- Deploy to a GPU: the base image has CUDA variants like `ghcr.io/prefix-dev/pixi:noble-cuda-12.9.1`.
- Let CI update the lockfile for you: [update lockfiles with GitHub Actions](https://pixi.prefix.dev/latest/integration/ci/updates_github_actions/).

!!! note "With your own workspace"

    The realistic adoption order for an existing team is the order of this exercise.
    CI ships first: one file, and nothing changes for anyone's workflow.
    Docker second, once the team trusts the lockfile.
    Each step ships independently and reverts cleanly.

---

That is the workshop.
See [Migrating from rosdep & colcon](../reference/migration.md) for the write-up you can hand your team on Monday.
