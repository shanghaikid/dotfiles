dotfiles
========
just some arch linux config file...

## Alacritty + tmux (macOS)

Our [Alacritty fork](https://github.com/shanghaikid/alacritty) includes the
Catppuccin Mocha palette, JetBrains Nerd Font, window preferences, scrolling and
clipboard settings, native macOS shortcuts, and the Baidu Pinyin Shift/Enter
fix, plus OSC 7501 program status in native window/tab titles. These are built into the app and do not need a user configuration file.

This repository adds tmux startup, tabs/splits, Command shortcuts for tmux,
and short `directory · branch` tab labels. The Alacritty configuration contains
only that tmux integration. The tab bar uses Mocha colors with a mauve active
tab. No tmux plugins are required.

### First install on another Mac

Use our fork's `macos-ime-fix` branch with built-in defaults (commit `6b3d423`
or later). With Homebrew and Xcode Command Line Tools installed, build the
complete `.app` bundle so its fonts are included:

```sh
brew install tmux git rust scdoc
mkdir -p ~/workspace
git clone --branch macos-ime-fix https://github.com/shanghaikid/alacritty.git ~/workspace/alacritty
cd ~/workspace/alacritty
make app
ditto target/release/osx/Alacritty.app /Applications/Alacritty.app

git clone git@github.com:shanghaikid/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install-terminal.sh
```

If either repository already exists, use `git pull --ff-only` in that checkout
instead of cloning it again. A separate font installation is unnecessary.
See the fork's [build and defaults documentation](https://github.com/shanghaikid/alacritty/blob/macos-ime-fix/LOCAL-DEFAULTS.md)
for universal Intel/Apple Silicon bundles. Alacritty 0.17 and tmux 3.7 are the
versions originally used to verify this setup. OSC 7501 is verified with our tmux 3.8 fork. Official Alacritty builds can use the tmux
integration, but will use their own appearance defaults and lack our IME fix.

The installer links these files and backs up existing files under
`~/.dotfiles-backups/terminal-*`:

| Installed path | Repository file |
| --- | --- |
| `~/.tmux.conf` | `.tmux.conf` |
| `~/.config/alacritty/alacritty.toml` | `.config/alacritty/alacritty.toml` |
| `~/.config/tmux/window-name` | `.config/tmux/window-name` |

On macOS it also moves Alacritty's Hide shortcut to Control-Option-Shift-Command-H,
leaving Command-H available for pane navigation. Restart Alacritty once after
the initial installation so the menu shortcut and shell launcher take effect.
The launcher finds tmux on both Apple Silicon and Intel Homebrew installations.
Your existing zsh setup stays in place; this installer does not replace `.zshrc`.

### Future updates

```sh
cd ~/dotfiles
git pull --ff-only
tmux source-file ~/.tmux.conf  # needed only if tmux is already running
```

The symlinks pick up new repository content directly. Alacritty reloads its
tmux bindings automatically; shell-launcher changes require a restart.

Appearance, fonts, and native defaults are maintained in the Alacritty fork.
To update those, rebuild and replace the app, then reopen Alacritty:

```sh
cd ~/workspace/alacritty
git pull --ff-only
make app
ditto target/release/osx/Alacritty.app /Applications/Alacritty.app
```

### Program status (OSC 7501)

The Alacritty fork implements Program Status Protocol revision 0.4 without any
extra Alacritty configuration. Programs must send reports themselves. A native
title can show `— [working 42%] build` or `— [permission] build`.

For raw reports from programs inside tmux, use our tmux fork. Upstream tmux
consumes unknown OSCs before Alacritty sees them. Build a native executable:

```sh
brew install autoconf automake pkg-config libevent ncurses utf8proc
mkdir -p ~/workspace
git clone --branch osc7501 https://github.com/shanghaikid/tmux.git ~/workspace/tmux
cd ~/workspace/tmux
contrib/program-status/build.sh
mkdir -p ~/.local/bin
install -m 755 tmux ~/.local/bin/tmux
```

For later updates, `git pull --ff-only` in that checkout and rerun the build
script. The shared Rust engine and its lockfile are pinned to our remote
Alacritty repository; no sibling checkout or extra plugin is needed.

This dotfiles version shows `#{pane_program_status}` next to the existing
directory/branch tab label. Status updates are event-driven and limited to
10 Hz; repeated identical reports do not trigger status redraws.

An existing server continues running its old executable. To try the new build
while preserving all current sessions, run:

```sh
~/.local/bin/tmux -L osc7501 new-session -A -s alacritty
```

The normal launcher uses the new default server after its old sessions finish.
Do not kill an active server just to upgrade it. Plain Alacritty windows use
the protocol after reopening the updated app. See the fork's
[protocol behavior and measured performance](https://github.com/shanghaikid/alacritty/blob/macos-ime-fix/OSC7501.md).

### Shortcuts

| Shortcut | Action |
| --- | --- |
| Shift-Enter | Newline in Codex (the fork sends Ctrl-J in legacy input mode) |
| Command-T | New tmux tab in the current directory |
| Command-Shift-[ / ] | Previous / next tab |
| Control-Tab / Control-Shift-Tab | Next / previous tab |
| Command-1 through Command-9 | Select tab by number |
| Command-D / Command-Shift-D | Side-by-side / stacked split |
| Command-H / J / K / L | Select left / down / up / right pane |
| Command-W | Close pane, with confirmation |
| Control-B then Z | Toggle pane zoom |
| Control-B then R | Reload tmux configuration |

Tab labels follow the active pane's directory and Git branch, refreshing every
five seconds. Directory names are capped at 24 characters and branches at 16;
long names end with `…`. Home appears as `~`, non-Git directories show only their
name, and detached Git HEADs show a short commit ID.

History scrolling uses one line per wheel event to keep Mac trackpad gestures
responsive. This changes tmux copy-mode scrolling only; mouse-aware applications
keep their own scrolling behavior. Use PageUp/PageDown in copy mode for large
jumps. Long files can also be read directly with `less --mouse file.md`.

## Pi agent config

Portable pi agent config lives in `pi-agent/` and is linked from `~/.pi/agent/`.

No sync script is required. Future updates can be done by an agent editing `~/dotfiles/pi-agent` directly and keeping the `~/.pi/agent` symlinks in place.

See `pi-agent/README.md` for setup details and secret handling.
