#!/usr/bin/env bash


# -------------------------------------------------------------------------
# 远仓操作

# 远仓
alias gra='git remote add'      # 关联远仓：gra 远仓名（即远程repo在本地的名字） 远程repo的网址

alias grrm='git remote rm'      # 取关远仓：    grrm 远仓名
alias grrn='git remote rename'  # 重命名远仓：  grrn 远仓名
alias grls='git remote show'    # 列出远仓：    grls
                                # 显示远仓信息： grls 远仓名
# 远枝
# alias gbu='git branch -u'     # 将当前枝关联远枝：           gup 远仓名 远枝名
gbu()
{
    if [ $# = 0 ]; then
        local remote=origin
        local remote_branch=`git_current_branch`
    elif [ $# = 1 ]; then
        local remote=$1
        local remote_branch=`git_current_branch`
    elif [ $# = 2 ]; then
        local remote=$1
        local remote_branch=$2
    else
        echo 'Aruments: [remote [remote_branch]]'
        echo '    default remote=origin'
        echo '    default remote_branch=<current_local_branch_name>'
        echo 'if remote_branch does not exist on remote repo, it will be created'
        return
    fi
    echo "-----------------------------------------------------------------------"
    echo "remote: $remote; remote_branch: $remote_branch"
    echo "git fetch $remote $remote_branch"
    git fetch $remote $remote_branch
    echo "fetched"
    echo "-----------------------------------------------------------------------"
    echo "git branch --set-upstream-to=$remote/$remote_branch"
    git branch --set-upstream-to=$remote/$remote_branch
    echo "upstream branch has set"
    echo "-----------------------------------------------------------------------"
}
alias gbuu='git branch --unset-upstream' # 将当前枝取关远枝：   guu [本地分支名，默认为当前分支]


alias gps='git push'     # 推送当前枝：                   gps [ 远仓名 [远枝名]]
alias gfc='git fetch'           # 拉去到当前枝：          gfc [ 远仓名 [远枝名]]
# gplu [远仓名 [远枝名]],   初次拉用
gplu() {
    gbu $*
    git pull
}
alias gpl='git pull'            # 拉去到当前枝并与之合并：  gpl [ 远仓名 [远枝名]]
                                # gps，gfc，gpl皆可省参数：
                                # 若该远仓的远枝已关联，则[远枝名]不写
                                # 若还只关联一个远仓，则[ 远仓名 [远枝名]]不写

alias gpr='git pull --rebase'
alias grbc='git rebase --continue'


# 初次推送用，关联远枝并推送，若远仓无此远枝，则创建之
# gpsu [远仓名 [远枝名]]，  默认远仓名=origin， 默认远枝名=本地现枝名
gpsu()
{
    if [ $# = 0 ]; then
        local remote=origin
        local remote_branch=`git_current_branch`
    elif [ $# = 1 ]; then
        local remote=$1
        local remote_branch=`git_current_branch`
    elif [ $# = 2 ]; then
        local remote=$1
        local remote_branch=$2
    else
        echo 'Usgae: gpsu [remote [remote_branch]]'
        echo '    default remote=origin'
        echo '    default remote_branch=<current_local_branch_name>'
        echo 'if remote_branch does not exist on remote repo, it will be created'
        return
    fi
    echo $remote $remote_branch
    git push -u $remote $remote_branch
}



# 弯弓提交到上游分支
gbps() {
    local current="$(get_node_name HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow push'."
        return
    fi
    git pull --rebase
    local upstream="$(get_node_name ${current}@{upstream})"
    local remote=$(echo "${upstream}" | awk -F '/' '{print $1}')
    local remote_repo=$(echo "${upstream}" | awk -F '/' '{print $2}')
    git checkout $upstream
    git merge --no-ff --no-edit $current
    git push $remote HEAD:$remote_repo
    git checkout $current
    # git merge $upstream
}



