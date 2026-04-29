export EDITOR="vim"

autoload -U compinit promptinit
compinit
promptinit

# Prompt
autoload -Uz vcs_info
zstyle ':vcs_info:git:*' formats ' %F{214}⎇ %b%f'  # 橙黄色 git 分支
precmd() { vcs_info }
setopt PROMPT_SUBST

# 青色路径 + 橙黄色 git 分支 + 绿色/红色提示符
PROMPT='%F{81}%~%f${vcs_info_msg_0_} %(?.%F{119}❯.%F{203}❯)%f '
RPROMPT='%F{243}%*%f'  # 更柔和的灰色时间
alias ll="ls -al -G"
alias vi="vim"
alias vim="vim -p"
alias gs="git status"
alias gg="git log --graph --all"
alias free="free -h"
alias du.="du -h -d 0"
alias vimsshconfig="vim ~/.ssh/config"
alias vg="vim ~/.config/ghostty/config"
alias kik="ssh-keygen -R"
alias dstat="dstat -lamps"
alias cleanmilvus="rm -rf volumes/minio volumes/milvus volumes/etcd && sudo docker-compose up -d"

export HISTSIZE=10000
export SAVEHIST=10000
export HISTFILE=~/.zhistory
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_DUPS
setopt EXTENDED_HISTORY
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

export FZF_DEFAULT_COMMAND='ag --ignore .git -g ""'
export PATH=$PATH:~/.cargo/bin

# 设置 HTTP 和 HTTPS 代理
alias setproxy='export HTTP_PROXY=http://127.0.0.1:7890; export HTTPS_PROXY=http://127.0.0.1:7890; export ALL_PROXY=http://127.0.0.1:7890'

# 取消 HTTP 和 HTTPS 代理
alias unsetproxy='unset HTTP_PROXY; unset HTTPS_PROXY; unset ALL_PROXY'

export PATH="$HOME/.local/bin:$PATH"

gpgconf --launch gpg-agent

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Added by Antigravity
export PATH="$HOME/.antigravity/antigravity/bin:$PATH"

# opencode
export PATH="$HOME/.opencode/bin:$PATH"



export OPENAI_API_KEY="usr_pool_0128_716cfd45641f"
