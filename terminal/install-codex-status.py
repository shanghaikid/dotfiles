#!/usr/bin/env python3
"""Merge terminal-status hooks without replacing existing hooks or trust settings."""

import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile


COMMAND = '"$HOME/.local/bin/codex-program-status" "$PPID"'
EVENTS = ("SessionStart", "SessionEnd", "UserPromptSubmit", "PermissionRequest",
          "PreToolUse", "PostToolUse", "Stop", "Interrupt")


def merge(existing):
    hooks = existing.setdefault("hooks", {})
    for event in EVENTS:
        groups = hooks.setdefault(event, [])
        if any(h.get("command") == COMMAND for group in groups for h in group.get("hooks", [])):
            continue
        group = {"hooks": [{"type": "command", "command": COMMAND, "timeout": 1}]}
        if event == "SessionStart":
            group["matcher"] = "^(startup|resume|clear)$"
        if event == "PreToolUse":
            group["matcher"] = r"(^|[._])request_user_input$"
        groups.append(group)
    return existing


def install(home, repo):
    source = repo / ".local/bin/codex-program-status"
    destination = home / ".local/bin/codex-program-status"
    hook_path = home / ".codex/hooks.json"
    original = hook_path.read_bytes() if hook_path.exists() else None
    document = json.loads(original) if original else {}
    updated = (json.dumps(merge(document), indent=2) + "\n").encode()
    needs_link = not destination.is_symlink() or destination.resolve() != source.resolve()
    needs_hooks = updated != original
    backup = home / ".dotfiles-backups" / ("codex-status-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    if needs_link and (destination.exists() or destination.is_symlink()):
        backup.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(backup / "codex-program-status"))
    if needs_hooks and original is not None:
        backup.mkdir(parents=True, exist_ok=True)
        (backup / "hooks.json").write_bytes(original)
    if needs_link:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source)
    if needs_hooks:
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        # Follow an existing hooks.json symlink while updating its target atomically.
        target = hook_path.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=".hooks-", dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(updated)
            os.replace(name, target)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    print("Codex status hooks installed. In Codex, run /hooks and trust the codex-program-status entries.")
    if backup.exists():
        print("Previous files: " + str(backup))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    install(args.home, Path(__file__).resolve().parents[1])
