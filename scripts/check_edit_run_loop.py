"""Check that editing a node's source actually rebuilds it.

Exercise 2 teaches the edit-run loop as the payoff of building ROS packages with
Pixi: change a source file, `pixi run`, see the change. If that stops being
true, the exercise silently teaches the room to trust stale code, so we assert
it here rather than find out on stage.

It edits the log line of the C++ node (src/turtle_dancer/src/dance.cpp), runs
the node through `pixi run`, and expects the new text in the output. Twice, so
a single lucky rebuild does not count. It failed on pixi 0.73.0 and passes since
0.76.2 with pixi-build-ros 0.7.2; see PIXI_IMPROVEMENTS.md, finding 1. CI runs
it as a regression test.

The Python node is not checked: pixi-build-ros 0.7.2 does not watch `**/*.py`
by default (the workshop page says so in 2.6). Point --source at
choreograph.py once a backend release includes it.

    pixi run check-edit-run-loop
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import time

MARKER = "__WORKSHOP_EDIT_RUN_MARKER__"
ORIGINAL_LOG_LINE = 'RCLCPP_INFO(get_logger(), "Dancing. Start `pixi run sim` to watch.");'


def run_node(manifest: pathlib.Path, timeout: float) -> str:
    """Start the node through `pixi run`, return everything it printed.

    The node spins forever, so we stop it ourselves: as soon as a line with the
    marker shows up, or when the timeout runs out (which covers the first build).
    """
    process = subprocess.Popen(
        ["pixi", "run", "--manifest-path", str(manifest), "ros2", "run", "turtle_dancer", "dance"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert process.stdout is not None
    output: list[str] = []
    deadline = time.monotonic() + timeout
    try:
        for line in process.stdout:
            output.append(line)
            if MARKER in line or time.monotonic() > deadline:
                break
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
    return "".join(output)


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
        default="solutions/02-ros-package/src/turtle_dancer/src/dance.cpp",
        type=pathlib.Path,
        help="node source file to edit; must contain the node's log line",
    )
    parser.add_argument(
        "--timeout",
        default=600.0,
        type=float,
        help="seconds to wait for the node to build and print its log line",
    )
    args = parser.parse_args()

    source: pathlib.Path = args.source
    original = source.read_text()
    if ORIGINAL_LOG_LINE not in original:
        print(f"FAIL: {source} does not contain the expected log line:\n  {ORIGINAL_LOG_LINE}", file=sys.stderr)
        return 1

    try:
        for expected in ("first", "second"):
            edited_line = ORIGINAL_LOG_LINE.replace("Dancing.", f"Dancing {MARKER}={expected}.")
            source.write_text(original.replace(ORIGINAL_LOG_LINE, edited_line))
            output = run_node(args.manifest, args.timeout)

            marker_lines = [line for line in output.splitlines() if MARKER in line]
            if not marker_lines:
                stale = [line for line in output.splitlines() if "Dancing" in line]
                print(
                    f"FAIL ({expected} edit): the node never printed the edited log line, "
                    f"so nothing was rebuilt. Last 'Dancing' line seen: {stale[-1] if stale else '<none>'}\n"
                    f"      See PIXI_IMPROVEMENTS.md finding 1.",
                    file=sys.stderr,
                )
                print(output[-2000:], file=sys.stderr)
                return 1

            if f"{MARKER}={expected}" not in marker_lines[-1]:
                print(
                    f"FAIL ({expected} edit): source says {expected!r}, but the node printed "
                    f"{marker_lines[-1].strip()!r}: a stale build.\n"
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
