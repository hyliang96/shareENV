# -------------------------------------------------------------------------
# 分支操作

gb()                      # 新建分支并检出到此分支： gb 分支名
{
    git branch $1 && git checkout $1
}
alias gbrm='git branch -D' # 删除分支：gbrm 分支名
alias gbls='git branch -avv' # 列出所有本地枝，及其关联的远枝： gbls
# alias gch='git checkout'    # 切换分支：gch 分支名/历史提交编号/HEAD^/HEAD/HEAD~n/HEAD@{n}, 要先git commit一次才能gch
alias gff='git merge'         # 快进式merge
alias gmg='git merge --no-ff' # 将当前枝与此分支合并（非快进）
alias gmgc='git commit' # 解决完冲突, 运行此以继续merge
# alias gmgc='git merge --continue'   # git已废弃之


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

