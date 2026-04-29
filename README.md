dotfiles
========
just some arch linux config file...

## Pi agent config

Portable pi agent config lives in `pi-agent/` and is linked from `~/.pi/agent/`.

No sync script is required. Future updates can be done by an agent editing `~/dotfiles/pi-agent` directly and keeping the `~/.pi/agent` symlinks in place.

See `pi-agent/README.md` for setup details and secret handling.
