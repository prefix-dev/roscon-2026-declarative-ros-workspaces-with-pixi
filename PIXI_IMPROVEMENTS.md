# Pixi improvement ideas found while building this workshop

Friction hit while scaffolding the ROSCon 2026 material, in rough order of how much it would hurt a ROS developer.
Everything here was reproduced on `pixi 0.73.0`, macOS `osx-arm64`, unless noted.

This is feedback for the Pixi team, not workshop content.

---

## 1. Editing a node's source does not rebuild it, so you silently run stale code

**Update 2026-08-17, pixi 0.76.2 with `pixi-build-ros` 0.7.2: mostly fixed.**
Editing `dance.cpp` now rebuilds `ros-jazzy-turtle-dancer` on the next `pixi run`, and the build cache sidecar lists the input globs it watches (`**/*.cpp`, `package.xml`, `CMakeLists.txt`, ...).
Two things remain:

1. `**/*.py` is not in the released backend's default globs, so a Python (`ament_python`) node still runs stale after an edit.
   `extra-input-globs = ["**/*.py"]` in `[package.build.config]` fixes it, and it is in the backend's `main` branch as a default already.
2. Changing `extra-input-globs` in the package manifest does **not** invalidate the existing build, so the new globs only take effect after something else triggers a rebuild (`touch package.xml`).
   Chicken and egg: the setting that makes edits count is itself an edit that does not count.
   Suggested fix: include the backend configuration in the build cache key.

`pixi run check-edit-run-loop` passes, and CI enforces it.
The original write-up follows for context.

**Severity: high.
This is the most important item in this document.** It breaks the core inner loop of ROS development: edit a node, run it, see the change.

With a source dependency (`ros-jazzy-turtle-dancer = { path = "src/turtle_dancer" }`), editing the node's Python source has no effect.
Nothing rebuilds, nothing warns, and the previously built code runs again:

```console
$ # edit src/turtle_dancer/turtle_dancer/dance.py, changing a returned string
$ pixi run python -c "import turtle_dancer.dance as d; print(d.MARKER())"
edit-run-loop-works            # <- the OLD value; the edit is not there
                               #    returned in 0.7s, no build was attempted
$ pixi install
                               # 0.1s, "nothing to do"
$ pixi lock --check
✔ Lock-file was already up-to-date
```

Everything reports success.
The developer concludes their code change did nothing, and starts debugging the wrong thing.

**What does and does not invalidate the build:**

| Change | Rebuilds? |
| --- | --- |
| Edit the node's `.py` source | **No** |
| Edit `src/turtle_dancer/pixi.toml` (the package manifest) | **No** |
| Add `extra-input-globs = ["turtle_dancer/**/*.py"]` to the backend config | **No** |
| Edit `package.xml` | Yes |
| Edit the *workspace* `pixi.toml` | Yes |
| `rm -rf .pixi/bld` | Yes |

The `package.xml` row is the tell: a rebuild triggered that way *does* pick up the pending source edit, so the build itself is fine; only the change detection is wrong.
Note that `extra-input-globs` did not help, which suggests the staleness check never reaches the backend's glob configuration.

The lockfile records the source dependency with what looks like a content hash:

```yaml
- conda_source: ros-jazzy-turtle-dancer[ebbe11a8] @ src/turtle_dancer
```

That hash appears not to be recomputed from the source tree on `pixi run` / `pixi install`.

**Suggested fix:** recompute the source hash from the package's input globs on every `pixi run` and `pixi install`, and rebuild when it differs.
If a full hash is too expensive for the hot path, an mtime pre-check over the glob set would catch this case at almost no cost.
Failing silently is the worst possible behaviour here.
A warning would at least be actionable.

**Why this matters for the workshop:** we intend to teach the edit-run loop as the payoff of using Pixi for ROS ("no colcon invocation, no sourcing, just edit and run").
Today that demo would show the room stale code, which is worse than not showing it at all.

---

## 2. Stale `.pixi/bld` produces a confusing unrelated failure

**Severity: medium**, and closely related to the above.

When a rebuild *is* finally triggered after the source tree has moved on, the cached build directory can be inconsistent, and the failure surfaces as a setuptools error with no hint that the cache is the problem:

```
× failed to build 'ros-jazzy-turtle-dancer' from 'src/turtle_dancer'
╰─▶   × Script failed to execute
```

With `-v`:

```
UserWarning: Unknown distribution option: 'install_requires'
UserWarning: Unknown distribution option: 'entry_points'
error: option --single-version-externally-managed not recognized
```

Nothing there points at the build cache.
`rm -rf .pixi/bld` fixed it immediately, and an identical clean workspace built the same sources without complaint.

**Suggested fix:** detect the inconsistency and re-create the work directory automatically, or mention `.pixi/bld` in the error so `rm -rf .pixi/bld` is the obvious next step.

---

## 3. `ament_python` install-scripts handling works, but the warning reads like a problem

**Severity: low.
This is a docs/wording issue, not a bug.**

I initially believed the backend put `console_scripts` in `bin/` rather than the `lib/<package>/` directory `ros2 run` searches, because a package without a `setup.cfg` gave:

```console
$ pixi run ros2 pkg executables turtle_dancer     # (empty)
$ pixi run ros2 run turtle_dancer dance
No executable found
```

That was my package being non-canonical, not a backend fault: `ros2 pkg create --build-type ament_python` always generates a `setup.cfg` with `install_scripts=$base/lib/<package>`, and adding it fixed everything.
The backend also already handles the missing case itself:

```
WARNING: setup.cfg not set, will set INSTALL_SCRIPTS_ARG to:
         --install-scripts=$PREFIX/lib/turtle_dancer
```

So the behaviour is right.
Two small things:

1. The message is phrased as a warning about something being unset, when it is really the backend doing the correct thing.
   Something like *"no `install_scripts` in setup.cfg; defaulting to `lib/turtle_dancer` so `ros2 run` can find it"* would reassure rather than alarm.
2. It is only visible with `-v`, so in practice nobody sees it.
   Given how confusing the `No executable found` symptom is when it does go wrong, this one is worth surfacing by default.

**Note:** `ament_cmake` is unaffected: `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` is idiomatic in every `CMakeLists.txt`.
Verified working, including `rosidl` interface generation for a custom `.msg`.

---

## 4. The build drops `files.txt` into the source tree

**Severity: low**, but it is the kind of papercut that makes a tool feel untidy, and it lands in `git status` where users will commit it by accident.

After building, a 14-line `files.txt` appears in `src/turtle_dancer/`.
It is the setuptools install record, listing absolute paths into `.pixi/bld/.../host_placehold_placehold_.../`:

```
/…/.pixi/bld/ros-jazzy-turtle-dancer/ODuh_Nus3y4/host_placehold_placehold_…/lib/python3.12/site-packages/turtle_dancer/dance.py
```

It is build output living in the user's source directory, and it references a throwaway prefix, so it has no value to the user at all.

**Suggested fix:** write it inside the build directory, or delete it afterwards.
(`*.egg-info/` and `build/` also land in the source tree; those are at least familiar to Python developers.)

---

## 5. The `[system-requirements]` deprecation help suggests a syntax that then fails

**Severity: medium.** The suggested fix does not work where you were told to apply it.

Declaring CUDA on a feature:

```toml
[feature.cuda.system-requirements]
cuda = "12.0"
```

warns, helpfully:

```
⚠ the `[system-requirements]` table is deprecated in favor of virtual packages on `platforms`
  help: e.g. platforms = [{ platform = "linux-64", cuda = "12" }]
```

Following that advice inside the same feature fails:

```toml
[feature.cuda]
platforms = [{ platform = "linux-64", cuda = "12" }]
```

```
Error:   × expected a string, found table
```

The rich inline form is only accepted in `[workspace] platforms`; a feature must reference a *named* entry declared there:

```toml
[workspace]
platforms = ["linux-64", { name = "linux-64-gpu", platform = "linux-64", cuda = "12.0" }]

[feature.cuda]
platforms = ["linux-64-gpu"]
```

That is a reasonable model, but nothing in the warning hints at it, and `expected a string, found table` does not point anywhere useful.

**Suggested fix:** make the deprecation help context-aware.
When the deprecated table is on a feature, show the two-part form.
And on the parse error, say so directly: *"feature platforms must reference platform entries declared in `[workspace] platforms` by name; rich entries cannot be declared here."*

---

## 6. Named platform entries lose their name in the lockfile

**Severity: low, but it undercuts the feature's main benefit.**

Naming platform variants is genuinely great for robotics: `jetson` and `workstation-gpu` say what they mean.
But the lockfile renames them:

```yaml
platforms:
- name: p1
  subdir: linux-64
  virtual-packages: [__cuda=12.0, ...]
- name: p2
  subdir: linux-aarch64
  virtual-packages: [__cuda=12.6, ...]
environments:
  robot:
    packages:
      p2:        # which machine was this again?
```

The point of naming a target is that humans can tell targets apart.
Reviewing a lockfile diff, the main thing a team does with lockfiles, you now have to map `p2` back to `jetson` by hand.

**Suggested fix:** keep the author's name in the lockfile.
If the internal identifier must stay opaque, carry the manifest name alongside it as a comment or field.

---

## 7. No way to keep a named platform variant out of the default environment

**Severity: low-medium.**

Because `[workspace] platforms` is the default feature's platform list, adding a variant for one feature also solves the default environment for it:

```yaml
environments:
  default:
    -> linux-64, linux-aarch64, osx-64, osx-arm64, p1, p2, win-64   # p1/p2 not wanted here
  robot:
    -> p2
```

For a workshop manifest, `default` picking up two GPU variants is noise I had to explain in a comment.
In a real project with several hardware targets it grows quickly, and there is no `no-default-feature` equivalent for platforms.

**Suggested fix:** let an environment or the default feature narrow its platform list, or let a named platform entry be marked as opt-in, so only features that reference it get solved for it.

---

## 8. `default-environment` on a task is silently ignored, and PATH leakage hides it

**Severity: medium.** This one produced a task that worked locally and would have failed in CI.

```toml
[tasks.lint]
cmd = "pre-commit run --all-files"
default-environment = "lint"     # accepted by the schema
```

`pre-commit` exists only in the `lint` feature.
Running it:

```console
$ pixi run lint
✨ Pixi task (lint in default): pre-commit run --all-files
[...hooks run and pass...]
```

It ran in `default`, not `lint`.
It appeared to work only because a *globally* installed `pre-commit` was on `PATH` (`/Users/…/.pixi/bin/pre-commit`); `.pixi/envs/default/bin/pre-commit` does not exist.
On a clean CI runner this fails with `pre-commit: not found`.

Two separate problems:

1. `default-environment` is accepted by the schema but had no effect here.
   If it is not supported for this case, it should be rejected at parse time rather than ignored.
2. A task falling through to a binary outside the environment defeats the purpose of having an environment.
   At minimum, warn when a task's command resolves outside the activated prefix: *"`pre-commit` was not found in environment `default`; using `/Users/…/.pixi/bin/pre-commit`"*.
   That single line would have caught this immediately.

The workaround is to define the task on the feature, which is arguably better style anyway:

```toml
[feature.lint.tasks.lint]
cmd = "pre-commit run --all-files"
```

But the failure mode (green locally, red in CI, for a non-obvious reason) is worth closing.

---

## 9. "Command not found" is reported as a list of available tasks

**Severity: low.**

```console
$ pixi run -- timeout 5 ros2 run turtle_dancer dance

Available tasks:
	dance
	sim
```

`timeout` does not exist on macOS.
The output implies the problem is that `timeout` is not a *task*, when the real problem is that no such *command* exists in the environment.
For anyone following a tutorial written on Linux, that is a confusing signpost.

**Suggested fix:** distinguish the two cases.
If the first argument is not a task *and* not resolvable on `PATH`, say `command not found: timeout` and only then offer the task list.

---

## 10. A task in two environments is ambiguous even when one is the default

**Severity: medium for anyone using environments as variants**, which is the pattern we teach.

Two ROS distributions in one workspace, as two environments, is a great demo.
But giving both a `sim` task makes the obvious command fail:

```console
$ pixi run sim
Error:   × the task 'sim' is ambiguous
  help: These environments provide the task 'sim': default, kilted
        Specify the '--environment' flag to run the task in a specific environment
```

The error is clear and the fix is easy, but one of the two candidates is *the default environment*.
Preferring it would make `pixi run sim` do the obvious thing while `pixi run -e kilted sim` stays available, which is exactly the mental model the feature invites.

As it stands, the first command in our Exercise 1 would error, so we renamed the second environment's tasks to `sim-kilted` and friends.
That works, but it hides the nicer story: same task name, different environment.

**Suggested fix:** when a task name is ambiguous and one of the candidate environments is `default`, run it there.
Optionally emit a hint the first time, naming the other environments that also provide it.

---

## 11. RoboStack channel emits a malformed CEP-42 reference

**Severity: cosmetic, and probably RoboStack's to fix rather than Pixi's.** Noted because it shows up on every solve against these channels, and this workshop will put it in front of a few hundred ROS developers.

```
WARN malformed CEP-42 reference `/conda-forge` declared by `https://prefix.dev/robostack-jazzy/`:
must be a relative path starting with `../`
```

Worth either fixing the channel metadata or suppressing the warning for this case, so the first thing a workshop attendee sees is not a warning they cannot act on.

---

## 12. `pixi-build-ros` fetches the rosdistro index from GitHub on every metadata refresh

**Severity: high for a workshop, medium otherwise.** Found 2026-08-17 on `pixi-build-ros` 0.7.2.

The backend downloads `https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml` to learn whether a distro is ROS 1 or 2, even when `distro = "jazzy"` is configured explicitly.
The response is cached, but per workspace (`.pixi/scratch-v0/pixi-build-ros-v0/http-cache`) and with GitHub's `max-age=300`, so any `pixi lock`, `pixi install` or `pixi run` that refreshes source metadata more than five minutes after the last one goes back to GitHub.
Unauthenticated `raw.githubusercontent.com` is rate limited per IP, and after a morning of re-locking from one laptop it answered `429 Too Many Requests` for a good while:

```
× failed to resolve source package 'ros-jazzy-turtle-choreographer' (at 'src/turtle_choreographer')
╰─▶ × the ROS distribution index at https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml
    │ is being rate limited (HTTP 429 Too Many Requests)
```

Fifty attendees behind one conference NAT will hit this in the first ten minutes of Exercise 2, and nothing they can do locally fixes it.
Nothing in the workshop needs the index either: RoboStack channel names already say which distro it is, and Jazzy has been ROS 2 for a while.

**Suggested fixes**, any one of which would do:

- Ship the answer for known distros inside the backend and only fetch for names it does not know.
- Cache globally (`~/.cache/rattler` or the pixi cache dir) and treat a stale cached copy as good enough when the refresh fails (`stale-if-error`).
- An escape hatch: `ROSDISTRO_INDEX_URL` or a `[package.build.config]` key pointing at a local file, so a workshop can ship the file in the repo.

## Things that worked well, for balance

Noted because they are load-bearing for the workshop and worth not regressing:

- **Cross-solving is excellent.** Resolving a `linux-aarch64 + __cuda=12.6` Jetson environment from a MacBook, and inspecting it with `pixi list --platform jetson`, is the single most compelling thing we will show.
  Nothing in the ROS ecosystem comes close.
- **Solve speed sells itself.** A cold solve of an entirely different ROS distro, 391 packages, took **1.3 s**.
  That number does more persuading than any slide.
- **Two ROS distros in one workspace works**, via per-feature channels and separate environments.
  `pixi run -e kilted sim` next to `pixi run -e jazzy sim` is a genuinely striking demo.
- **`colcon` runs happily inside a Pixi environment** (5.2 s for a C++ package), which makes the migration story teachable: attendees keep their existing build, then replace it.
- **`pixi-build-ros` reading `package.xml`** as the single source of truth is the right call, and sibling source discovery across a workspace works as advertised.
  Custom `rosidl` interface generation worked first try.
