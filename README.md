# Declarative ROS workspaces with Pixi and RoboStack

A hands-on workshop for reproducible ROS development.

**ROSCon 2026 — Tuesday, September 22nd, 08:00–12:00**

📖 **[prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/)**

[Pixi](https://pixi.prefix.dev) is a fast, cross-platform package manager built on the conda
ecosystem. [RoboStack](https://robostack.github.io) provides the ROS 2 distribution as conda
packages. Together they let you declare an entire ROS environment — system libraries, Python
packages and ROS nodes — in a single `pixi.toml`, with a lockfile that guarantees reproducibility.

## Attending the workshop?

Do this at home, not on conference Wi-Fi:

```bash
# 1. Install pixi
curl -fsSL https://pixi.sh/install.sh | bash     # Windows: see the site

# 2. Get the material
git clone https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi.git
cd roscon-2026-declarative-ros-workspaces-with-pixi

# 3. Warm up the package cache and check it works
pixi run --manifest-path solutions/01-ros-workspace/pixi.toml sim
```

A turtle should appear. Full instructions:
[Before you start](https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/setup/).

## What is in here

```text
docs/          the workshop site (Zensical)
slides/        the presented slides (Slidev)
exercises/     where participants work — one directory per exercise
solutions/     the finished workspaces, smoke-tested in CI on Linux, macOS and Windows
```

## Working on the material

Everything runs through Pixi tasks; `pixi task list` shows them all.

| Command | What it does |
| --- | --- |
| `pixi run docs` | Serve the site at <http://localhost:8000> with live reload |
| `pixi run slides` | Present the slides locally |
| `pixi run build` | Build the site and the slides into `site/` |
| `pixi run lock-solutions` | Re-solve every solution workspace for every platform |
| `pixi run lint` | Formatters and linters |

The site deploys to GitHub Pages from `main`. The slides are built into `site/slides/`, which is
what the "Slides" entry in the navigation points at.

### Adding content

- Explainers are `docs/explainers/*.md`, exercises are `docs/exercises/*.md`. Add new pages to `nav`
  in `zensical.toml`.
- Slides are one file, `slides/slides.md`. Each agenda block is a `section:` in the frontmatter,
  which is what the footer displays.
- `<!-- TODO(content) -->` markers show what still needs writing; `IMPLEMENTATION_PLAN.md` tracks the
  stages.

## Credit

Built by [prefix.dev](https://prefix.dev). Structure borrowed from the
[DESY Pixi workshop](https://github.com/prefix-dev/desy-workshop) and Matthew Feickert's
[reproducible CUDA workflows tutorial](https://github.com/matthewfeickert-talks/reproducible-cuda-workflows-with-pixi-scipy-2026).

## License

BSD-3-Clause. See [LICENSE](LICENSE).
