---
icon: lucide/trash-2
---

# Cleaning up

Pixi keeps its files in three places, and all three are safe to delete.
The lockfile can rebuild every environment, the only cost is downloading again.

Start with the built-in commands:

```bash
pixi clean          # this project's environments, the .pixi/ folder
pixi clean cache    # the shared package cache
```

Everything is gone when you remove the folders themselves:

```bash
rm -rf .pixi                     # in the project: its environments
rm -rf ~/.cache/rattler/cache    # every downloaded package, for all projects
rm -rf ~/.pixi                   # pixi itself and your `pixi global` tools
```

`pixi info` prints the exact cache location for your machine; macOS keeps it in `~/Library/Caches/rattler/cache`.

!!! warning "`~/.pixi` contains `pixi` itself"

    Removing `~/.pixi` also deletes the `pixi` binary and everything you installed with `pixi global install`.
    Reinstall with the one-liner from [Before you start](../setup.md).

Afterwards a project comes back exactly as the lockfile describes:

```bash
pixi install
```
