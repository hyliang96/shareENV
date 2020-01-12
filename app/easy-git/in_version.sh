#!/usr/bin/env bash

# ------------------ git ----------------------------
# 版本内操作

# 初创
alias gin='git init'       # 创建.git:    cd 项目文件夹; gi
# 暂存
alias gs='git status'     # 查看当前状态:  gs
alias ga='git add'        # 暂存增改文件:  ga 文件
gaa() {
    if [ $# -eq 0 ]; then
        local git_path="$(git_root)"
    else
        local git_path="$1"
    fi
    git add -A "$git_path"
}

alias gut='git rm -r --cached'   # git untrack
alias grm='git rm -rf'    # （删除并）暂存删除： grm 文件              ；用于替代rm
alias gmv='git mv'        # （移动并）暂存移动： gmv 文件 文件夹       ；用于替代mv

guam(){
    if [ $# = 0 ] || [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ] ; then
        echo 'Usage: 撤销对 已跟踪文件 的修改与暂存，无法撤销修改先前未跟踪的文件'
        echo ' gum  <filename> [ <filename> [ <filename> ...]]'
        echo ' gum  -a|--all : 所有为暂存的修改'
    elif [ "$1" = '-a' ] || [ "$1" = "--all" ]; then
        # cd `git_root`
        # git checkout HEAD .
        gua -a
        gum -a
    else
        # git checkout HEAD "$@"
        gua "$@"
        gum "$@"
    fi
}
gua(){
    if [ $# = 0 ] || [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
        echo 'Usage: 撤销暂存，对 `git add` `git rm`有效 '
        echo ' gua  <filename> [ <filename> [ <filename> ...]]'
        echo ' gua   -a|--all : 撤销所有暂存'
    elif [ "$1" = '-a' ] || [ "$1" = "--all" ]; then
        # 无需 cd `git_root`, 直接重置整个repo
        git reset HEAD
    else
        # 有一个文件不存在, 不影响其他文件被清理
        for i in "$@"; do
            git reset HEAD "$i"
        done

        # 有一个文件不存在, 整个命令就无法执行, 不会有文件被清理
        # git reset HEAD "$@"
    fi
}
gum(){
    if [ $# = 0 ] || [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ] ; then
        echo 'Usage: 撤销对 已跟踪文件 [未`git add`]的修改，无法撤销修改先前未跟踪的文件'
        echo ' gum  <filename> [ <filename> [ <filename> ...]]'
        echo ' gum  -a|--all : 所有为暂存的修改'
    elif [ "$1" = '-a' ] || [ "$1" = "--all" ]; then
        (cd `git_root`
        git checkout  .
        git clean -df .)
    else
        # 有一个文件不存在, 不影响其他文件被清理
        for i in "$@"; do
            git checkout -- "$i"
            git clean -df "$i"
        done

        # 有一个文件不存在, 整个命令就无法执行, 不会有文件被清理
        # git checkout -- "$@"
        # git clean -df "$@"
    fi
}

gcln()
{
    if [ $# -eq 0 ] || [[ "$1" =~ '^(-h|--help|help)$' ]]; then
        cat << EOF
Usage: git clean的封装, 清理未被跟踪也未被忽略的文件(夹)
gcln <path>s   : 若<path>s中有 未跟踪也未忽略 的文件(夹), 则rm之
gcln -a|--all  : 整个repo中的 未跟踪也未忽略 的文件(夹), 皆rm之
EOF
    elif [[ "$1" =~ '^(-a|--all)$' ]]; then
        (cd `git_root`
        git clean -df .)
    else
        for i in "$@"; do
            git clean -df "$i"
        done
    fi
}



