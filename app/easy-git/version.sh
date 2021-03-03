#!/usr/bin/env bash


# -----------------------------------------------------------
# 单分支版本操作

# 提交
alias gacm='git commit -am' # 即先gaa, 然后gcm
# alias gcm='git commit -m'  # 提交：gcm "xxx" [options]
gcm() 
{
    if [ $# -eq 0 ] || [[ "$1" =~ ^- ]]; then
        git commit "$@"
    else
        git commit -m "$@"
    fi
}
alias gcma='git commit --amend' # 先add，再覆盖上一次提交：gcma，然后弹出文本编辑器，编辑上次提交的说明

__git_rebase_i()
{
    local commitid="$1"
    echo $commitid
    local git_seq_editor="$2"
    echo $git_seq_editor

    local root_long_hash="$(git_root_commit)"
    echo $root_long_hash

    local commit_long_hash="$(get_long_hash "$commitid")"
    echo $commit_long_hash

    if [ "$root_long_hash" = "$commit_long_hash" ]; then
        GIT_SEQUENCE_EDITOR="$git_seq_editor" git rebase -i --root
    else
        GIT_SEQUENCE_EDITOR="$git_seq_editor" git rebase -i ${commitid}^
    fi
}


# 把连续的几个历史提压缩成一个, 时间顺序为 [起始提交, 结束提交] 闭区间
# `gcms 起始提交 结束提交`,   可用hash, 或HEAD, HEAD^, EHAD~n表示
# 然后弹出vim, 请编辑压缩后的节点的message, 保存退出即可

gcms() {
    local first_commmit=${1}
    local last_commmit=${2}
    git --no-pager log --pretty=format:'%h' ${first_commmit}..${last_commmit}
    echo
    local commitids=($(git --no-pager log --pretty=format:'%h' ${first_commmit}..${last_commmit}))
    if [ ${#commitids} -eq 0 ]; then
        echo "empty commit range ${first_commmit}..${last_commmit}" >&2
        return
    fi
    # commitids=("$first_commmit" "${commitids[@]}")
    declare -p commitids
    local git_seq_editor="sed -i -re '"
    for commitid in "${commitids[@]}"; do
        git_seq_editor+="s/^pick ${commitid}/squash ${commitid}/; "
    done
    git_seq_editor="${git_seq_editor:0:${#git_seq_editor}-2}"
    git_seq_editor+="'"
    echo -E $git_seq_editor
    __git_rebase_i "$first_commmit" "$git_seq_editor"
}

# 修改提交信息：  gcmr <版本id> -> 弹出vim, 需改message, 保存退出即可
#    接收一个版本hash, 或HEAD, HEAD^, HEAD~n, 或branch名(表示这个分支最末的commit)
gcmr() {
    local commitid="$(get_hash $1)"
    local git_seq_editor="sed -i -re 's/^pick ${commitid}/reword ${commitid}/'"
    __git_rebase_i "$commitid" "$git_seq_editor"
}

# 修改提交信息：  gcme <版本id>  ->  gaa -> gcma -> grbc 即可
#    接收一个版本hash, 或HEAD, HEAD^, HEAD~n, 或branch名(表示这个分支最末的commit)
gcme() {
    local commitid="$(get_hash $1)"
    local git_seq_editor="sed -i -re 's/^pick ${commitid}/edit ${commitid}/'"
    __git_rebase_i "$commitid" "$git_seq_editor"
    # GIT_SEQUENCE_EDITOR="sed -i -re 's/^pick ${commitid}/edit ${commitid}/'" git rebase -i ${commitid}^
}

# gcms, gcme, gcmr, 只能对当前一个分支奏效, 其他分支的祖先commmit都保留原样, 不会一起被改动;
# 因此当前分支和其他分支的分叉节点可能会挪动

gucm() # 直接回到历史版本
{
    if [ $# = 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        echo 'gucm: 封装了 `git reset --hard`'
        echo 'Usage: 恢复到历史上某个时间点, glg会复原, ghs会增加一个版本操作'
        echo
        echo ' glg                  : git log, 查看版本关系图, 选择要恢复到哪'
        echo '                        最后一次commit为HEAD, HEAD的n父版本为HEAD{n}'
        echo '   gucm 0  | HEAD     : 恢复到最近一次git commit后'
        echo '   gucm ^  | HEAD^    : 恢复到父版本'
        echo '   gucm ^n | HEAD~n   : 恢复到n父版本'
        echo '   gucm 哈希码        : 恢复到指定哈希码的版本'
        echo
        echo ' ghs                  : git reflog, 查看版本操作的历史, 选择要恢复到哪'
        echo '                        依时间顺序显示, HEAD{0}为最后一次版本操作, 再往前第n个版本操作为HEAD@{n}'
        echo '   gucm -  | HEAD@{1} : 恢复到1次版本操作之前, 即HEAD@{1}版本操作完成后'
        echo '   gucm -n | HEAD@{n} : 恢复到n次版本操作之前, 即HEAD@{n}版本操作完成后'
        echo '   gucm ghs中的哈希码 : 恢复到指定哈希码的版本操作完成后'
        return
    fi

    # `git reset --hard 版本`的原理: 回到目标节点所在的历史时刻, 具体操作为
    # * 以目标节点跟踪的文件, 均取代当前工作目录/暂存索引/HEAD索引
    # * 工作目录/暂存索引被取代不留档, 其余未被取代的文件则保留
    # * 未被取代文件只能是: 当前未被跟踪的文件, 且在目标节点中无此文件
    # * 这一操作总能执行, 不会发生冲突拒绝执行

    if ! [ -z "$(git status --porcelain)" ]; then
        local waring=$'请先git commit再gucm, 以使得目录clean(无未跟踪的文件, 无未提交的修改)\n是否继续reset [Y|N] '
        local answer=$(bash -c "read -p '$waring' c; echo \$c"); echo
        ( ! [[ "$answer" =~ "^(y|Y)$" ]] )  && return
    fi

    local target_version="$1"
    if [ "$1" = "0" ]; then
        echo git reset --hard HEAD
        git reset --hard HEAD
    elif [ "$1" = "^" ]; then
        echo git reset --hard HEAD^
        git reset --hard HEAD^
    elif [ "${target_version:0:1}" = "^" ]; then
        local n=${target_version:1:${#target_version}}
        echo git reset --hard HEAD~$n
        git reset --hard HEAD~$n
    elif [ "$1" = "-" ]; then
        echo git reset --hard HEAD@{1}
        git reset --hard HEAD@{1}
    elif [ "${target_version:0:1}" = "-" ]; then
        local n=${target_version:1:${#target_version}}
        echo git reset --hard HEAD@{$n}
        git reset --hard HEAD@{$n}
    else
        echo git reset --hard $1
        git reset --hard $1
    fi
}
grcm() # 反向提交到某个版本
{
    if [ $# = 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        echo 'grcm: 封装了`git revert`'
        echo 'Usage: 反向提交以返回历史版本'
        echo
        echo ' glg                  : git log, 查看版本关系图, 选择要恢复到哪'
        echo '                        最后一次commit为HEAD, HEAD的n父版本为HEAD{n}'
        echo ' grcm ^   | HEAD^     : 到上一版本'
        echo ' grcm ^n  | HEAD~n    : 到前n版本'
        echo ' grcm glg中的哈希码   : 回到指定哈希的版本, 必需是HEAD的祖宗版本'
        echo
        echo ' 若有暂存、修改，则无法执行，需先git commit 或 抛弃暂存与修改（即`gucm 0`）'
    elif ! [ -z "$(git status --porcelain)" ]; then
        echo '需先git commit再grcm, 以使得目录clean(无未跟踪的文件, 无未提交的修改)'
        # `git revert` 的 原理:
        #  if 当前不干净的文件(不论 未跟踪/跟踪未暂存/跟踪且暂存), 在HEAD与目标节点中不一样(是否被跟踪, 文件内容), 则拒绝执行
        #  除了当前不干净的文件, 目标节点中的文件, 均替换当前工作目录/暂存index
        #  自动 git commit
    else
        local target_version=$1
        if [ "${target_version}" = "^" ]; then
            local old_name="HEAD^"
        elif [ "${target_version:0:1}" = "^" ]; then
            local n=${target_version:1:${#target_version}}
            local old_name="HEAD~${n}"
        else
            local old_name="$1"
        fi
        git revert ${old_name}..HEAD --no-edit  --no-commit     # 反向提交一次，回到上一版本
        local old_hash="$(get_hash ${old_name})"
        git commit -m "Revert ${old_name}..HEAD; now same as ${old_hash}"
    fi
}

gch()
{
    if [ $# = 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        echo '检出整个节点:'
        echo '  gch <node>                  : 前往指定节点'
        echo '  gch <node> --replace        : git rm 当前节点所有跟踪文件(夹), 再将指定节点的所有跟踪文件(夹)拷贝过来 并git add'
        echo '需先git commit再gch, 以使得目录clean(无未跟踪的文件, 无未提交的修改)'
        # 执行上述两命令成功的充要条件为: 一切当前工作目录中不干净的文件(未跟踪/跟踪未暂存/暂存未提交), 在去往节点和HEAD节点中完全一样(是否被跟踪一样, 文件内容一样)
        # 执行后, 原来不干净的文件, 其内容/是否被跟踪/是否被暂存 均完全未变
        echo
        echo '检出部分文件: '
        echo '  gch <node> <file-or-dir>(s) : 将指定节点的指定文件(夹)拷到当前节点 并git add'
        echo '  gch <node> --all            : 将指定节点的所有跟踪文件(夹)拷到当前节点 并git add'
        echo '不论拷过来的文件, 在当前是什么状态(未跟踪/跟踪且未暂存/跟踪且已暂存/跟踪且无增量), 均可直接执行'
        echo
        echo '<node> = 分支名/glg中的版本哈希/HEAD/HEAD^/HEAD~n/HEAD@{n}'
    elif [ "$2" = '--all' ]; then
        (cd `git_root`
        git checkout "$1" .)
    elif [ "$2" = '--replace' ]; then
        git read-tree -um HEAD "$1"
    else
        git checkout "$@"
    fi
}



