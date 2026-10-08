#!/bin/bash
set -euo pipefail

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

for tool in tmux git; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        printf 'Missing dependency: %s. See README.md.\n' "$tool" >&2
        exit 1
    fi
done
if [[ ! -x /bin/zsh ]]; then
    printf 'This terminal configuration requires /bin/zsh.\n' >&2
    exit 1
fi

backup_dir="$HOME/.dotfiles-backups/terminal-$(date +%Y%m%d-%H%M%S)-$$"
link_file() {
    local relative=$1 source="$repo_dir/$1" destination="$HOME/$1"
    if [[ -L "$destination" && $(readlink "$destination") == "$source" ]]; then
        printf 'Already linked: %s\n' "$destination"
        return
    fi
    if [[ -e "$destination" || -L "$destination" ]]; then
        mkdir -p "$backup_dir/$(dirname -- "$relative")"
        mv -- "$destination" "$backup_dir/$relative"
        printf 'Backed up: %s\n' "$backup_dir/$relative"
    fi
    mkdir -p "$(dirname -- "$destination")"
    ln -s -- "$source" "$destination"
    printf 'Linked: %s\n' "$destination"
}

link_file .tmux.conf
link_file .config/alacritty/alacritty.toml
link_file .config/tmux/window-name

if [[ $(uname -s) == Darwin ]]; then
    # Free Command-H for pane navigation, preserving other menu customizations.
    defaults write org.alacritty NSUserKeyEquivalents -dict-add \
        'Hide Alacritty' '@^~$h' 'Hide alacritty' '@^~$h'
fi

if tmux has-session 2>/dev/null; then
    tmux source-file "$HOME/.tmux.conf"
    printf 'Reloaded the running tmux configuration.\n'
fi
printf 'Terminal configuration installed. Future git pulls update these links.\n'
