#!/usr/bin/env bash


# 历史
# alias glg="git log --graph --oneline --all --pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cr %C(bold blue)%an%Creset %s' --abbrev-commit --date=short"  #列出提交历史图谱，含远仓、本仓
# alias glg="git log  --graph --abbrev-commit --oneline --pretty=format:'%C(yellow)%h%C(reset)%C(auto)%d%C(reset) %C(green)%cr %C(bold blue)%an%C(reset) %s' --date=short --all"  #列出提交历史图谱，含远仓、本仓
# alias glg1="git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset)%>|(20)%<(1)%<(15)%C(bold green)%ar%C(reset) %<(17,trunc)%C(bold blue)%an%C(reset) %C(white)%s%C(reset)%n%C(auto)%d%C(reset)' --all" #
# alias glg2="git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset)%C(auto)%d%C(reset)%>|(50)%<(1)%>(14)%C(bold green)%ar%C(reset) %C(bold cyan)%ad%C(reset) %C(dim white)%an%C(reset)%n%>|(25)%<(1)%s'  --date=format:'%Y-%m-%d' --all"
# # '%Y-%m-%d 周%w %H:%M:%S'
# alias glg=" "

glg()
{
    if [[ "$1" =~ '^(-h|--help)$' ]]; then
        cat << EOF
glg                  : 显示分支图中所有stash
glg --noe-stash      : 整个分支图只显示当前一个stash
glg --no-stash       : 不显示任何stash
EOF
        git log --help
        return
    elif [ "$1" = '--one-stash' ]; then
        shift
        local cmd=' --all'
    elif [ "$1" = '--no-stash' ]; then
        shift
        local cmd=' --exclude=refs/stash --all'
    else
        if [ "$(git stash list 2>/dev/null)" = '' ]; then
            local cmd=' --all'
        else
            local cmd=' --all $(git reflog show --format="%h" stash)'
        fi
    fi

    alias _glg="git log --graph --abbrev-commit --decorate=no --date=format:'%Y-%m-%d' --pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cd %cr %C(bold blue)%an%Creset %C(bold #777777)%s%C(reset)' $cmd"
    alias _glg_table="git log --graph --abbrev-commit --decorate=no --date=format:'%Y-%m-%d' --format=format:'%C(yellow)%h%C(reset) %C(auto)%d%C(reset) %C(green)%>|(50)%ad %ar %C(reset)  %C(blue)%<(16,trunc)%an%C(reset) %C(bold #777777)%>|(1)%s%C(reset)' $cmd"
    #  --date=format:'%Y-%m-%d %H:%I:%S'
    eval _glg "$@"
}
# "$(git for-each-ref --format="%(refname)" refs/heads/ refs/remotes/ | grep -v "\.stgit$")"
#
alias glgs='glg --simplify-by-decoration'               #列出简化历史图谱
# alias ghs='git reflog'   # 按时间顺序列出 版本重置（git reset）、提交（git commit）
alias ghs="git reflog --abbrev-commit --pretty=format:'%C(yellow)%h%C(reset)%C(yellow) - %gd%C(reset)%C(auto)%d%Creset %C(green)%cr%C(reset) %C(bold blue)%an%C(reset) %C(bold #CCCCCC)%gs%C(reset) %C(bold #777777)%s%C(reset)'"
alias ghs-no-action="git reflog --abbrev-commit --pretty=format:'%C(yellow)%h%C(reset)%C(yellow) - %gd%C(reset)%C(auto)%d%C(reset) %C(green)%cr%C(reset) %C(bold blue)%an%C(reset) %C(bold #777777)%s%C(reset)'"

alias gsh="git show"
