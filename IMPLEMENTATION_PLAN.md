# Implementation plan

Tracks the work on the workshop material.
Delete this file when every stage is complete.

## Design decisions

Settled in review.
Change these deliberately, not by drift.

| Decision | Choice | Why |
| --- | --- | --- |
| ROS distro | **Jazzy** primary | Lyrical (2026 LTS) is missing `navigation2`, `realsense2-camera` and `cartographer_ros`, which bring-your-own-workspace attendees need. Verified 2026-07-27. |
| Second distro | **Installed**, as a parallel `kilted` environment in one workspace | Per-feature channels let both distros coexist; `pixi run -e kilted sim` switches instantly, so nothing waits mid-exercise. Verified working. |
| Ex1 endpoint | Environment + a package built with **colcon** | Ends on the pain we remove: `ros2 run` fails with `Package not found` until you `source install/setup.bash`. Ex2 deletes it. `colcon` inside a Pixi env verified, 5.2 s. |
| Ex1 node | **Pre-written** in the starter | Nobody should type C++ in a package-management workshop; buys ~5 min. |
| Ex2 packages | C++ (`ament_cmake`) **and** Python (`ament_python`), both core | C++ primary: `ros2 run` works and it suits a C++-heavy room. |
| Ex2 focus | **The edit-run loop**; packaging is the means, not the subject | Directly contrasts the colcon loop from Ex1. **Blocked**, see Stage 0. |
| CUDA in Ex2 | **Declare and cross-solve only**, no GPU run | CUDA packages are Linux-only, so a build step excludes every macOS attendee. Solving for a GPU target from a Mac works and is the better demo. |
| GPU run | Moved to **Ex3**, on **Brev**, with a laptop fallback path | Keeps Ex2 in budget and puts the GPU next to the Jetson target, where "hardware I'm not sitting at" is the theme. |
| Publishing | **Presenter demo**, not hands-on | A one-line command; avoids distributing write tokens to ~50 people. Buys Ex3 ~5 min. |
| Windows | **First-class**, to be proven by CI | Native ROS 2 on Windows with no WSL is the most impressive claim we have. Unverified from macOS; CI decides. |

## Stage 0: Unblock the Exercise 2 premise

**Goal**: `pixi run` rebuilds a source package after its source changes.

Editing a node's `.py` source does not invalidate the build.
`pixi run`, `pixi install` and `pixi lock --check` all report success while running the previously built code.
Only editing `package.xml`, editing the *workspace* manifest, or `rm -rf .pixi/bld` forces a rebuild.
`extra-input-globs` does not help.
Full write-up: `PIXI_IMPROVEMENTS.md` finding 1.

Exercise 2 teaches this loop as the payoff of using Pixi for ROS, so it must be fixed in Pixi before the workshop.
Decided: fix upstream rather than teach a workaround.

**Success criteria**:

- `pixi run check-edit-run-loop` passes.
- The `edit-run-loop` job in `.github/workflows/ci.yml` loses its `continue-on-error: true`.

**Status**: Blocked on a Pixi fix, target well before September.

## Stage 1: Repository scaffolding

**Goal**: A repository that builds, deploys and verifies itself, with every page and slide in place but unwritten.

**Success criteria**:

- `pixi run build` produces the site and the slides. ✅
- All three solution workspaces solve for every declared platform and pass their smoke test. ✅
- CI deploys the site and verifies the solutions on Linux, macOS and Windows. ✅

**Still to do**, following the decisions above:

- Add the `kilted` environment to solution 01 so both distros are prefetchable.
- Add the C++ `ament_cmake` package to solution 02 as the primary one.
- Add the colcon "before" state to exercise 01, including a Windows CI job that proves `colcon build` works there.
- Move the CUDA/GPU pieces from solution 02 to solution 03, and add the Brev path.

**Status**: Complete for the site and lockfile machinery; content-shaping work listed above.

## Stage 2: Write the explainers

**Goal**: The four presented blocks exist as prose on the site and as slides.

**Deliverables**: `docs/explainers/*.md` and the matching sections of `slides/slides.md`.

**Success criteria**:

- Each block fits its slot when read aloud: 15, 30, 15, 15 minutes.
- Every concept an exercise depends on has been introduced before that exercise.
- No `<!-- TODO(content) -->` markers left in `docs/explainers/`.

**Open questions**:

- How much conda-ecosystem background does a ROSCon audience need?
  Assume none, or assume they have heard of conda?
- Slides and prose are two files per block.
  Keep them in sync by hand, or generate one from the other?

**Status**: Not Started

## Stage 3: Write the exercises

**Goal**: Three exercises a participant can complete unattended.

**Deliverables**: `docs/exercises/0{1,2,3}-*.md`, with the starter state in `exercises/` matching.

**Success criteria**:

- Every command has been run on Linux, macOS and Windows, and the output in the docs is real output.
- Each exercise has a check step that fails loudly if a step was skipped.
- Timings hold in a dry run with somebody who has not seen the material.
- Ex1 ≤ 24 min of content, Ex2 ≤ 26, Ex3 ≤ 18, so each has real slack.

**Status**: Not Started

## Stage 4: Write the reference pages

**Goal**: The pages people use during the workshop and after it.

**Deliverables**: `docs/reference/cheatsheet.md`, `troubleshooting.md`, `migration.md`.

**Success criteria**:

- Every command on the cheat sheet has been run against the pinned Pixi version.
- Troubleshooting covers every failure seen in the dry runs, using the exact error text.
- The migration page reads as a standalone document a participant can send to their team.

**Status**: Not Started

## Stage 5: Logistics and dry run

**Goal**: Confidence that four hours works.

**Success criteria**:

- A full dry run with the three presenters, timed.
- A dry run of the exercises by somebody outside the team, on Windows.
- Prefetch measured per platform and stated on the setup page.
  Currently ~1.7 GB installed per ROS distro, and we install two, so the homework is substantial.
  Decide what happens for attendees who arrive without it.
- Brev: billing model confirmed, credits secured, a Launchable built and tested, and the fallback path written.
  Blocking for the Ex3 GPU run.
- QR code to the site on the welcome slide.
- Repo URL confirmed.
  `prefix-dev/roscon-2026-…` is assumed in `zensical.toml`, the `build-slides` base path, and several docs links.
- Licence: BSD-3-Clause throughout today; decide whether the prose should be CC-BY-4.0.

**Status**: Not Started
