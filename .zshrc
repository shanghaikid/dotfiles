PATH="/home/shanghaikid/dev/bin:/usr/local/sbin:/usr/local/bin:/usr/bin"

autoload -U compinit promptinit
compinit
promptinit

# This will set the default prompt to the walters theme
prompt walters


PROMPT="%{$fg[red]%}%n%{$reset_color%}@%{$fg[blue]%}%m %{$fg_no_bold[yellow]%}%1~ %{$reset_color%}%# "
RPROMPT="[%{$fg_no_bold[yellow]%}%?%{$reset_color%}]"
alias ll="ls -al --color"
alias vi="vim"
alias vim="vim -p"
alias gs="git status"
alias gg="git log --graph --all"
alias free="free -h"
alias du.="du -h -d 0"
alias vimsshconfig="vim ~/.ssh/config"
alias kik="ssh-keygen -R"
alias dstat="dstat -lamps"

export HISTSIZE=10000
export SAVEHIST=10000
export HISTFILE=~/.zhistory
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_DUPS
setopt EXTENDED_HISTORY
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS

#sudo mount -t vboxsf eclipse /eclipse
#sudo mount -t vboxsf workspace /workspace
