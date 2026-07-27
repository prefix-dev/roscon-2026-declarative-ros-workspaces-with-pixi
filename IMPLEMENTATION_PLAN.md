# Implementation plan

Tracks the work on the workshop material. Delete this file when every stage is complete.

## Stage 1: Repository scaffolding

**Goal**: A repository that builds, deploys and verifies itself, with every page and slide in place
but unwritten.

**Success criteria**:

- `pixi run build` produces the site and the slides.
- All three solution workspaces solve for every declared platform and pass their smoke test.
- CI deploys the site and verifies the solutions on Linux, macOS and Windows.

**Status**: Complete

## Stage 2: Write the explainers

**Goal**: The four presented blocks exist as prose on the site and as slides.

**Deliverables**: `docs/explainers/*.md` and the matching sections of `slides/slides.md`.

**Success criteria**:

- Each block fits its slot when read aloud: 15, 30, 15, 15 minutes.
- Every concept an exercise depends on has been introduced before that exercise.
- No `<!-- TODO(content) -->` markers left in `docs/explainers/`.

**Open questions**:

- How much conda-ecosystem background does a ROSCon audience need? Assume none, or assume they have
  heard of conda?
- Slides and prose are currently two files per block. Keep them in sync by hand, or generate one
  from the other?

**Status**: Not Started

## Stage 3: Write the exercises

**Goal**: Three exercises a participant can complete unattended.

**Deliverables**: `docs/exercises/0{1,2,3}-*.md`, with the starter state in `exercises/` adjusted to
match.

**Success criteria**:

- Every command has been run on Linux, macOS and Windows, and the output in the docs is real output.
- Each exercise has a check step that fails loudly if a step was skipped.
- Timings hold in a dry run with somebody who has not seen the material.

**Known issues to resolve before writing Exercise 2**:

- `ros2 run turtle_dancer dance` does not find the executable for an `ament_python` package built by
  `pixi-build-ros`: the console script lands in `bin/`, but `ros2 run` looks in `lib/<package>/`. The
  solution currently runs the entry point directly (`pixi run dance`). Decide whether to teach it
  that way, fix it in the backend, or document a workaround.

**Status**: Not Started

## Stage 4: Write the reference pages

**Goal**: The pages people use during the workshop and after it.

**Deliverables**: `docs/reference/cheatsheet.md`, `troubleshooting.md`, `migration.md`.

**Success criteria**:

- Every command on the cheat sheet has been run against the pinned Pixi version.
- Troubleshooting covers every failure seen in the dry runs, using the exact error text.
- The migration page reads as a standalone document that a participant can send to their team.

**Status**: Not Started

## Stage 5: Dry run and polish

**Goal**: Confidence that four hours works.

**Success criteria**:

- A full dry run with the three presenters, timed.
- A dry run of the exercises by somebody outside the team, on Windows.
- Download sizes measured per platform, and the prefetch instructions on the setup page match.
- QR code to the site on the welcome slide.
- Decide on the ROS distro: Jazzy is pinned everywhere today. Confirm nothing newer is a better bet
  by September.

**Status**: Not Started
