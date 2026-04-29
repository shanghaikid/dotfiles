# Pi agent dotfiles

This directory stores the portable parts of `~/.pi/agent`.

以后不用脚本同步；需要新增、调整或迁移 pi 配置时，直接让 agent 按这份说明更新 `~/dotfiles/pi-agent` 和 `~/.pi/agent` 的链接即可。

## 目录映射

当前约定：把可移植配置放在 `~/dotfiles/pi-agent/`，再从 `~/.pi/agent/` 用符号链接指过去。

```text
~/.pi/agent/APPEND_SYSTEM.md -> ~/dotfiles/pi-agent/APPEND_SYSTEM.md
~/.pi/agent/settings.json    -> ~/dotfiles/pi-agent/settings.json
~/.pi/agent/models.json      -> ~/dotfiles/pi-agent/models.json
~/.pi/agent/extensions       -> ~/dotfiles/pi-agent/extensions
~/.pi/agent/skills           -> ~/dotfiles/pi-agent/skills
```

如果以后增加这些文件/目录，也可以按同样方式纳入 dotfiles：

- `SYSTEM.md`, `AGENTS.md`
- `keybindings.json`
- `prompts/`, `themes/`

## 不放进 git 的内容

这些是运行时数据、缓存或机器本地凭据，不建议放入 dotfiles：

- `auth.json`：OAuth/session token
- `sessions/`：会话历史
- `bin/`：pi 下载的 helper binaries，比如 `rg`、`fd`
- `git/`, `npm/`：pi package 安装目录/缓存
- `secrets/` 或任何真实 API key

`.gitignore` 已经排除了常见的 pi runtime/local 路径。

## Secrets

`models.json` 里的 `apiKey` 不要写真实 key。Pi 支持 shell command 形式，当前用法是：

```json
"apiKey": "!cat ~/.config/pi-agent/secrets/token-zasdas-api-key"
```

真实 key 放在 git 之外：

```bash
mkdir -p ~/.config/pi-agent/secrets
printf '%s\n' '<api-key>' > ~/.config/pi-agent/secrets/token-zasdas-api-key
chmod 600 ~/.config/pi-agent/secrets/token-zasdas-api-key
```

## 新机器初始化

```bash
git clone git@github.com:shanghaikid/dotfiles.git ~/dotfiles
mkdir -p ~/.pi/agent ~/.config/pi-agent/secrets

# 写入本机 secret
printf '%s\n' '<api-key>' > ~/.config/pi-agent/secrets/token-zasdas-api-key
chmod 600 ~/.config/pi-agent/secrets/token-zasdas-api-key

# 建立链接；如果目标已存在，先手动备份/删除再 ln -s
ln -s ~/dotfiles/pi-agent/APPEND_SYSTEM.md ~/.pi/agent/APPEND_SYSTEM.md
ln -s ~/dotfiles/pi-agent/settings.json ~/.pi/agent/settings.json
ln -s ~/dotfiles/pi-agent/models.json ~/.pi/agent/models.json
ln -s ~/dotfiles/pi-agent/extensions ~/.pi/agent/extensions
ln -s ~/dotfiles/pi-agent/skills ~/.pi/agent/skills
```

如果目标文件已经存在，可以先备份：

```bash
mkdir -p ~/.pi/agent/.manual-backup-$(date +%Y%m%d-%H%M%S)
# 然后把已有文件/目录 mv 进去，再重新 ln -s
```

## 日常更新方式

- 直接修改 `~/dotfiles/pi-agent/...`。
- 如果在 pi 运行中改了 extensions、skills、prompts、keybindings 或 context files，进 pi 执行 `/reload`。
- 修改后检查不要提交 secret：

```bash
cd ~/dotfiles
git status --short
grep -RInE 'usr_pool_|sk-[A-Za-z0-9]' pi-agent || true
```
