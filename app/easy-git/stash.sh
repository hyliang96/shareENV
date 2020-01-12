#!/usr/bin/env bash

# -------------------------------------------------------------------------
# git stash
alias gtps='git stash push -u -m'
alias gtpl='git stash apply --index'
# alias gtls-a='git stash list --oneline'   # 列出分支图中所有stash, 而不仅仅是当前节点的stash
alias gtls-a='ghs-no-action stash'   # 列出分支图中所有stash, 而不仅仅是当前节点的stash
# git stash list =  git reflog stash
gtls() # 只显示当前节点的stash
{
    if [[ "$1" =~ '^(-a|--all)$' ]]; then
        gtls-a
        return
    fi

    local stash_on_HEAD

    git stash list --oneline --parents |
    grep $(git rev-parse --short HEAD) |
    awk '{printf $1"|"}' |sed 's/|$//' |
    read stash_on_HEAD

    gtls-a --color=always |
    grep --color=never -E ${stash_on_HEAD} |
    less
}
# gtls1()
# {
    # local stash_on_HEAD

    # git stash list --oneline --parents |
    # grep $(git rev-parse --short HEAD) |
    # awk '{printf $1" "}' |
    # read stash_on_HEAD

    # stash_on_HEAD=($(echo "$stash_on_HEAD"))

    # # git show stash --quiet --abbrev-commit --decorate=no --date=format:'%Y-%m-%d %H:%I:%S' --pretty=format:'%C(yellow)%h%Creset%C(auto)%gd%d%Creset %Cgreen%cr %C(bold blue)%an%Creset %C(bold 0)%s%C(reset)'
    # ghs stash "${stash_on_HEAD[@]}"
# }

alias gtsh='git stash show'
alias gtrm='git stash drop'
alias gtrma='git stash clear' # 删除所有节点的stash


