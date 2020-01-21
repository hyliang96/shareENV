# -------------------------------------------------------------------------
# 分支操作

gb()                      # 新建分支并检出到此分支： gb 分支名
{

    [ $# -ne 0 ] && git branch $1 && git checkout $1
}
alias gbrm='git branch -D' # 删除分支：gbrm 分支名
alias gbls='git branch -avv' # 列出所有本地枝，及其关联的远枝： gbls
# alias gch='git checkout'    # 切换分支：gch 分支名/历史提交编号/HEAD^/HEAD/HEAD~n/HEAD@{n}, 要先git commit一次才能gch
alias gff='git merge'         # 快进式merge

# 在A分支, 挑选一或多次别的分支的任意提交的增量, 依次apply到HEAD, 在A分支生成一次提交
# 可能需要多次解决冲突, 每次解决冲突后`gaa`再`gcm`
# 解决完所有冲突后, 当前目录干净, 此时需执行一次 `gpkc`
# 然后目录里出现所有被挑选来的节点的文件, 均已经add, 直接`gcm '<信息>'`即完成提交
alias gpk='git cherry-pick -x -n' # gpk [文件夹名]'s
alias gpkc='git cherry-pick --continue'
alias gpka='git cherry-pick --abort'
alias gpko='gmgo' # git checkout --ours [文件夹名]'s
alias gpkt='gmgt' # git checkout --theirs [文件夹名]'s


gsq() # git merge --squash
{
    local target="$1"
    local current="$(get_node_name HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow merge'."
        return
    fi
    git checkout "$target"
    git merge --squash "$current"
    git commit
    # 弹出vim, 编辑commit信息
    git checkout "$current"
}


alias gmg='git merge --no-ff' # 将当前枝与此分支合并（非快进）
alias gmgc='git commit' # 解决完冲突, 运行此以继续merge
# alias gmgc='git merge --continue'   # 老版本git没有之, 如git 2.7.4没有,  git2.20.1有
alias gmga='git merge --abort'
# 在A分支, gmg B分支, 若冲突, 要留A分支的文件, 则gmgo; 要留B分支的文件, 则gmgt
gmgo() {  # ours
    if [ $# -eq 0 ] || [[ "$1" =~ '^(-a|--all)$' ]]; then
        git checkout --ours "$(git_root)"
    else
        git checkout --ours "$@"
    fi
}
gmgt() { # theirs
    if [ $# -eq 0 ] || [[ "$1" =~ '^(-a|--all)$' ]]; then
        git checkout --theirs "$(git_root)"
    else
        git checkout --theirs "$@"
    fi
}

alias grb='git rebase'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'

# 在A分支, grb B分支, 若冲突, 要留A分支的文件, 则grbo; 要留B分支的文件, 则grbt
# 原生的git rebase后, 若冲突, theirs和ours所指, 与merge的正好相反
grbo() {  # ours
    if [ $# -eq 0 ] || [[ "$1" =~ '^(-a|--all)$' ]]; then
        git checkout --theirs  "$(git_root)"
    else
        git checkout --theirs  "$@"
    fi
}
grbt() { # theirs
    if [ $# -eq 0 ] || [[ "$1" =~ '^(-a|--all)$' ]]; then
        git rebase --skip  # 若某文件, B 分支删除 而A分支当前冲突的commit有, 则此命令会删除此文件
        # git checkout --ours "$(git_root)" # 若某文件, B 分支删除 而A分支当前冲突的commit有, 则此命令不会删除此文件
    else
        git checkout --ours "$@"
    fi
}


# 个人分支: debug 和 feature 分支 commit 前, 先 pull 或 rebase
# 提交到 公共(dev 和 master) 分支前, 先 pull 公共分支
# push 公共和个人分支 前, 先 pull

# 弯弓提交到目标分支
# 用于:
#     当前分支           目标分支
#   在 debug 分支,   提交到 master 分支:   `gbmg master`
#   在 feature 分支, 提交到 dev 分支:    `gbmg dev`

# 提交前的分支图
#  r: 旧根, R: 新根
#  t=[目标分支] -r-o-o-R(t)
#                 \
#  c=[当前分支]    o-o-o-o(c)

# 提交后的分支图
#  t=[目标分支] -r-o-o-R---------o(t)
#                       \       /
#  c=[当前分支]          o-o-o-o(c)

gbmg () {
    local target="$1"
    local current="$(get_node_name HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow merge'."
        return
    fi
    git rebase ${target}
    git checkout ${target}
    git merge --no-ff --no-edit ${current}
    git checkout ${current}
    # git merge ${target}
}

# 三角形提交到目标分支
# 用于:
#    在 dev 分支, 提交 到 master 分支:   `gbmg dev`

# 提交前的分支图
#  r: 根
#  t=[目标分支] -r-o-o-o-R(t)
#                 \
#  c=[当前分支]    o-o-o(c)

# 提交后的分支图
#  t=[目标分支] -r-o-o-o---o(t)
#                 \     \ /
#  c=[当前分支]    o-o-o-o(c)

gtmg() {
    local target="$1"
    local current="$(get_node_name HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow merge'."
        return
    fi
    git merge ${target}
    git checkout ${target}
    git merge --no-ff --no-edit ${current}
    git checkout ${current}
}

