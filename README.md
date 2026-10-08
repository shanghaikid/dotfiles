dotfiles
========
just some arch linux config file...

## Alacritty + tmux (macOS)

The shared terminal setup includes the Tokyo Night palette, tmux tabs/splits,
macOS Command shortcuts, clipboard integration, and short `directory · branch`
tab labels. No tmux plugins are required.

### First install on another Mac

Install [Alacritty](https://github.com/alacritty/alacritty/releases) from its
official macOS release, plus tmux, Git, and the configured font:

```sh
brew install tmux git
brew install --cask font-jetbrains-mono-nerd-font
git clone git@github.com:shanghaikid/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install-terminal.sh
```

If the repository already exists, use `git pull --ff-only` before running the
installer. Alacritty 0.17 and tmux 3.7 are the versions used to verify this setup.

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
appearance and bindings automatically; shell-launcher changes require a restart.

### Shortcuts

| Shortcut | Action |
| --- | --- |
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
