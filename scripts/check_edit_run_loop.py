"""Check that editing a node's source actually rebuilds it.

Exercise 2 teaches the edit-run loop as the payoff of building ROS packages with
Pixi: change a source file, `pixi run`, see the change. If that stops being
true, the exercise silently teaches the room to trust stale code, so we assert
it here rather than find out on stage.

It failed on pixi 0.73.0 and passes since 0.76.2; see PIXI_IMPROVEMENTS.md,
finding 1. CI runs it as a regression test. It edits the Python node, which
relies on `extra-input-globs = ["**/*.py"]` in that package's manifest.

    pixi run check-edit-run-loop
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

MARKER = "__WORKSHOP_EDIT_RUN_MARKER__"


def run(manifest: pathlib.Path, code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["pixi", "run", "--manifest-path", str(manifest), "python", "-c", code],
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="solutions/02-ros-package/pixi.toml",
        type=pathlib.Path,
        help="workspace manifest containing the source package",
    )
    parser.add_argument(
        "--source",
        default="solutions/02-ros-package/src/turtle_choreographer/turtle_choreographer/choreograph.py",
        type=pathlib.Path,
        help="node source file to edit",
    )
    parser.add_argument(
        "--module",
        default="turtle_choreographer.choreograph",
        help="importable module that --source becomes once the package is built",
    )
    args = parser.parse_args()

    source: pathlib.Path = args.source
    original = source.read_text()

    try:
        for expected in ("first", "second"):
            source.write_text(
                original + f'\n\ndef {MARKER}() -> str:\n    return "{expected}"\n'
            )
            result = run(
                args.manifest,
                f"import {args.module} as d; "
                f"print(getattr(d, {MARKER!r}, lambda: '<absent>')())",
            )
            got = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""

            if result.returncode != 0:
                print(f"FAIL: `pixi run` errored after editing {source}", file=sys.stderr)
                print(result.stderr.strip()[-2000:], file=sys.stderr)
                return 1

            if got == "<absent>":
                print(
                    f"FAIL ({expected} edit): the edited source is not in the "
                    f"environment at all: the added function is missing, so "
                    f"nothing was rebuilt.\n"
                    f"      See PIXI_IMPROVEMENTS.md finding 1.",
                    file=sys.stderr,
                )
                return 1

            if got != expected:
                print(
                    f"FAIL ({expected} edit): source returns {expected!r}, but the "
                    f"environment still returns {got!r}, a stale build.\n"
                    f"      See PIXI_IMPROVEMENTS.md finding 1.",
                    file=sys.stderr,
                )
                return 1

            print(f"ok: the {expected} edit was picked up")

        print("PASS: the edit-run loop rebuilds on every source change")
        return 0
    finally:
        source.write_text(original)


if __name__ == "__main__":
    raise SystemExit(main())
