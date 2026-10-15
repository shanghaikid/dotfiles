import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import pty
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


status = load("status", ROOT / ".local/bin/codex-program-status")
installer = load("installer", ROOT / "terminal/install-codex-status.py")


class StatusTests(unittest.TestCase):
    def setUp(self):
        self.saved = {}

    def event(self, event, **extra):
        return status.transition(dict(session_id="session-a", hook_event_name=event, **extra), self.saved)

    def test_lifecycle_and_duplicate_reports(self):
        self.assertIn(b"state=working", self.event("UserPromptSubmit"))
        self.assertIsNone(self.event("UserPromptSubmit"))
        self.assertIn(b"state=done", self.event("Stop"))
        self.assertIn(b"state=idle", self.event("Interrupt"))
        self.assertIn(b"state=clear", self.event("SessionEnd"))

    def test_matching_tool_resolves_approval(self):
        self.event("UserPromptSubmit")
        tool = dict(tool_name="Bash", tool_input={"command": "secret command"})
        report = self.event("PermissionRequest", **tool)
        self.assertIn(b"kind=permission", report)
        self.assertNotIn(b"secret", report)
        self.assertIsNone(self.event("PostToolUse", tool_name="Bash", tool_input={"command": "different"}))
        self.assertIn(b"state=working", self.event("PostToolUse", **tool))
        self.assertNotIn("secret", json.dumps(self.saved))

    def test_parallel_approvals_and_added_description(self):
        tool = dict(tool_name="Bash", tool_input={"command": "a", "description": "reason"})
        self.event("PermissionRequest", **tool)
        self.event("PermissionRequest", tool_name="Bash", tool_input={"command": "b"})
        self.assertIsNone(self.event("PostToolUse", tool_name="Bash", tool_input={"command": "a"}))
        self.assertIn(b"state=working", self.event("PostToolUse", tool_name="Bash", tool_input={"command": "b"}))

    def test_question_and_new_turn_clear_pending(self):
        tool = dict(tool_name="functions.request_user_input", tool_input={"questions": []})
        self.assertIn(b"kind=question", self.event("PreToolUse", **tool))
        self.assertIn(b"state=working", self.event("PostToolUse", **tool))
        self.assertIsNone(self.event("PreToolUse", tool_name="request_user_input_async"))
        self.event("PermissionRequest", tool_name="Bash", tool_input={})
        self.event("UserPromptSubmit")
        self.assertEqual(self.saved["pending"], {})

    def test_ancestor_selection_does_not_follow_selected_pane_or_daemon(self):
        rows = "10 1 ttys004 /path/codex\n11 10 ?? /bin/sh\n20 1 ttys005 /path/codex\n21 20 ?? /bin/sh\n30 1 ?? /path/codex\n31 30 ?? /bin/sh\n"
        self.assertEqual(status.codex_terminal(11, rows), (10, "/dev/ttys004"))
        self.assertEqual(status.codex_terminal(21, rows), (20, "/dev/ttys005"))
        self.assertIsNone(status.codex_terminal(31, rows))
        self.assertIsNone(status.codex_terminal(1, rows))

    def test_real_pty_output(self):
        master, slave = pty.openpty()
        try:
            report = self.event("UserPromptSubmit")
            status.write_terminal(os.ttyname(slave), report)
            self.assertEqual(os.read(master, 1024), report)
        finally:
            os.close(master)
            os.close(slave)

    def test_malformed_input_never_changes_codex_control_flow(self):
        result = subprocess.run([sys.executable, str(ROOT / ".local/bin/codex-program-status")],
                                input="not JSON", text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, "{}\n")
        self.assertEqual(result.stderr, "")

    def test_installer_preserves_other_hooks_and_is_idempotent(self):
        original = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "existing"}]}]}, "other": 42}
        merged = installer.merge(copy.deepcopy(original))
        self.assertEqual(merged["hooks"]["Stop"][0], original["hooks"]["Stop"][0])
        self.assertEqual(merged["other"], 42)
        self.assertEqual(installer.merge(copy.deepcopy(merged)), merged)
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            hooks = home / ".codex/hooks.json"
            hooks.write_text(json.dumps(original))
            config = home / ".codex/config.toml"
            config.write_text('[hooks.state.old]\ntrusted_hash="unchanged"\n')
            installer.install(home, ROOT)
            once = hooks.read_bytes()
            installer.install(home, ROOT)
            self.assertEqual(hooks.read_bytes(), once)
            self.assertIn('trusted_hash="unchanged"', config.read_text())
            self.assertEqual((home / ".local/bin/codex-program-status").resolve(), ROOT / ".local/bin/codex-program-status")
            backups = list((home / ".dotfiles-backups").glob("*/hooks.json"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(json.loads(backups[0].read_text()), original)


if __name__ == "__main__":
    unittest.main()
