# -------------------------------------------------------------------------
# 分支操作

gb()                      # 新建分支并检出到此分支： gb 分支名
{
    git branch $1 && git checkout $1
}
alias gbrm='git branch -d' # 删除分支：gbrm 分支名
alias gbls='git branch -avv' # 列出所有本地枝，及其关联的远枝： gbls
# alias gch='git checkout'    # 切换分支：gch 分支名/历史提交编号/HEAD^/HEAD/HEAD~n/HEAD@{n}, 要先git commit一次才能gch
alias gmg='git merge --no-ff' # 将当前枝与此分支合并（非快进）
alias gmgc='git commit' # 解决完冲突, 运行此以继续merge
# alias gmgc='git merge --continue'   # git已废弃之

# 弯弓提交到目标分支
gbmg () {
    local target="$1"
    local current="$(git rev-parse --abbrev-ref HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow merge'."
        return
    fi
    git rebase ${target}
    git checkout ${target}
    git merge --no-ff ${current}
    git checkout ${current}
    git merge ${target}
}


