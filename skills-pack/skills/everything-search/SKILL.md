---
name: everything-search
description: Instant 1ms PC-wide file and folder search across local drives using Voidtools Everything (`ev` CLI). Use whenever searching for projects, folders, files, large files, or recently modified files anywhere on the machine outside the current workspace.
---

# Everything Instant Search (`ev`)

This machine has **Voidtools Everything** indexing local drives in real time, exposed locally via `127.0.0.1:28491` (read-only metadata/path JSON API, file downloads disabled) and wrapped by the global `ev` CLI (`%USERPROFILE%\.local\bin\ev.cmd` -> `ev.py`, plus `es.exe`).

## Why Use `ev`
- Searches millions of files across local drives in **~1–2 milliseconds** (vs minutes with `Get-ChildItem -Recurse`).
- Works seamlessly inside Antigravity's `run_command` sandbox (`exebox`) AND interactive terminals.
- Handles Arabic folder/file names (`UTF-8`) cleanly without console encoding corruption.

## Quick Usage
```powershell
# Find any file or folder by name or partial path
ev "arena.ai"
ev "<PROJECT_PATH>"

# Match folders only (-d / --folders)
ev -d "<project-dir>"

# Match code files (-f) by extension (-e) while hiding node_modules/.git (-c)
ev -c -f -e py,js,ts,json "auth" -n 25

# Find files modified today or large files
ev -c "<WORKSPACE_ROOT>\ dm:today" -n 30
ev "size:>500mb" -n 20

# Raw JSON output for scripting
ev -c --json -n 10 "package.json"
```

## Troubleshooting
- If `ev` prints `[ev] Everything GUI is not running yet`, ask the user to click the **Everything** icon on their taskbar once (or press `Ctrl+Space`) so the Everything background tray window starts listening on `127.0.0.1:28491`.
