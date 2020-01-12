#!/usr/bin/env zsh

# ------------------ git ----------------------------
# git utils
git_root() {
    git rev-parse --show-toplevel
}
git_path_to_root() {
    local abs_path="$(abspath $1)"
    local git_path="$(git_root)"
    echo "${abs_path/${git_path}/}"
}

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
# alias gaa="git add -A "
# alias gaa='git add -A .'  # 暂存所有增删改文件：gaa



# 查看跟踪的文件和文件夹，并自动着色
# list files or dirs traced or ignored by git
# subrepo|git-ls-r|git-ls [<path> [<path> ...]] [<git-type>] [<other-args-of-ls>]

# git-ls   : ls all files/dirs directly under <path>
# git-ls-r : ls all files (no dirs) recursively under <path>
# subrepo  : ls all direct sub-repo (i.e. sub-sub-repo is not listed)
#            no necessary to be in .gitsubmodule

#   <path> [default=current path]
#   <git-type>
#       --all        : ls files/dirs
#       --track[default]: ls tracked files/dirs
#       --untrack    : ls untracked files/dirs = ignored + unadd
#       --ignore     : ls ignored files/dirs
#       --has-ignore : ls ignored files/dirs, and dirs contain ignored files/dirs
#       --unadd      : ls unadded (i.e. untracked and not in .gitignore ) files/dirs
#       --has-unadd  : ls unadded files/dirs, and dirs contain unadded files/dirs

# auto colored
# .git is always ignored


has_dot_git() {
    while read data; do
        echo -E "$data"
    done | \
    sed 's/\/$//g' | \
    sed 's/$/&\/.git/g' | \
    sed 's/\ /\\\ /g' | xargs ls -d1 2>/dev/null | \
    sed 's/\/.git$//g' | \
    sort | uniq
}

subrepo_() {
    if [ "$1" = '--all' ]; then
        (git ls-files & git ls-files -o) | has_dot_git
    elif [ "$1" = '--track' ]; then
        git ls-files | has_dot_git
    elif [ "$1" = '--untrack' ]; then
        git ls-files -o | has_dot_git
    elif [ "$1" = '--ignore' ]; then
        subrepo_ --untrack | sed 's/\ /\\\ /g' | xargs git check-ignore 2>&1 | grep -v  'fatal: no path specified'
    elif [ "$1" = '--unadd' ]; then
        (subrepo_ --ignore & subrepo_ --untrack) | sort | uniq -u
    else
        echo "wrong args $@ for \`subrepo_\`." >&2
    fi
}

subrepo() {
    local git_type='--track'
    local ls_args=()
    local dir_paths=()
    while test $# -gt 0 ; do
        case "$1" in
            --all|--track|--untrack|--ignore|--unadd) git_type="$1" ;;
            -*|--*)    ls_args+=("$1") ;;
            *)         dir_paths+=("$1");;
        esac
        shift
    done

    if [ ${#dir_paths} -eq 0 ]; then
        subrepo_ "$git_type" |  sed 's/\ /\\\ /g' | xargs ls -d --color=auto "${ls_args[@]}" | grep -v -E '^.$'
    else
        local here_path="$(pwd | sed 's/\ /\\\ /g')"
        for dir_path in "${dir_paths[@]}"; do
            echo
            echo -E "$dir_path:" | sed 's/\ /\\\ /g'
            cd $dir_path
            subrepo_ "$git_type" |  sed 's/\ /\\\ /g' | xargs ls -d --color=auto "${ls_args[@]}" | grep -v -E '^.$'
            cd $here_path
        done
    fi
}

git-ls-r_() {
    if [ "$1" = '--all' ]; then
        (git-ls-r_ --track & git-ls-r_ --untrack) | sort | uniq
    elif [ "$1" = '--track' ] ; then
        git ls-files
    elif [ "$1" = '--untrack' ]; then
        git ls-files -o | sed 's/\/$//g'
    elif [ "$1" = '--ignore-file' ]; then
        git ls-files -o -i --exclude-standard
    elif [ "$1" = '--ignore-repo' ]; then
        subrepo_ --ignore
    elif [ "$1" = '--ignore' ]; then
        ( git-ls-r_ --ignore-file & git-ls-r_ --ignore-repo) | sort | uniq
    elif [ "$1" = '--unadd' ]; then
        (git-ls-r_ --ignore & git-ls-r_ --untrack) | sort | uniq -u
    else
        echo "wrong args $@ for \`git-ls-r_\`." >&2
    fi
}

git-ls-r() {
    local git_type='--track'
    local ls_args=()
    local dir_paths=()
    while test $# -gt 0 ; do
        case "$1" in
            --all|--track|--untrack|--ignore-file|--ignore-repo|--ignore|--unadd) git_type="$1" ;;
            -*|--*)    ls_args+=("$1") ;;
            *)         dir_paths+=("$1");;
        esac
        shift
    done

    if [ ${#dir_paths} -eq 0 ]; then
        git-ls-r_ "$git_type" |  sed 's/\ /\\\ /g' | xargs ls -d --color=auto "${ls_args[@]}"
        # | grep -v -E '^.$'
    else
        local here_path="$(pwd | sed 's/\ /\\\ /g')"
        for dir_path in "${dir_paths[@]}"; do
            echo
            echo -E "$dir_path:" | sed 's/\ /\\\ /g'
            cd $dir_path
            git-ls-r_ "$git_type" |  sed 's/\ /\\\ /g' | xargs ls -d --color=auto "${ls_args[@]}"
            # | grep -v -E '^.$'
            cd $here_path
        done
    fi
}


first_layer() {
    while read data; do
        echo -E "$data"
    done | awk -F / '{print $1}' | sort | uniq
}

git-ls() {
    local git_type='--track'
    local ls_args=()
    local dir_paths=()
    while test $# -gt 0 ; do
        case "$1" in
            --all|--track|--untrack|--has-untrack|--ignore|--has-ignore|--unadd|--has-unadd) git_type="$1" ;;
            -*|--*)    ls_args+=("$1") ;;
            *)         dir_paths+=("$1");;
        esac
        shift
    done

    if [ "$git_type" = '--all' ]; then
        \ls -1a | grep -v -E '^(.|..|.git)$'
    elif [ "$git_type" = '--track' ]; then
        git ls-files | first_layer
    elif [ "$git_type" = '--untrack' ]; then
        (git-ls --all & git-ls --track) | sort | uniq -u
    elif [ "$git_type" = '--has-untrack' ]; then
        git ls-files -o | first_layer

    elif [ "$git_type" = '--ignore' ]; then
        git-ls --all | sed 's/\ /\\\ /g' | xargs git check-ignore
    elif [ "$git_type" = '--has-ignore' ]; then
        git-ls-r_ --ignore | first_layer
    elif [ "$git_type" = '--unadd' ]; then
        (git-ls --ignore & git-ls --untrack) | sort | uniq -u
    elif [ "$git_type" = '--has-unadd' ]; then
        git-ls-r_ --unadd | first_layer
    else
        echo "wrong arg $git_type for \`git-ls\`." >&2
    fi | sed 's/\ /\\\ /g' | xargs ls -d --color=auto "${ls_args[@]}"
    # | grep -v -E '^.$'
}

gls()
{
    local ls_args=()
    local dir_paths=()
    # declare -a dir_paths
    while test $# -gt 0
    do
        case "$1" in
            -*|--*)    ls_args+=("$1") ;;
            *)         dir_paths+=("$1");;
        esac
        shift
    done

    # local gls_command="git-ls $file_type  | awk -F / '{print \$1}' | uniq | sed 's/\ /\\\ /g' | xargs ls -dh --color=auto $ls_args"

    if [ ${#dir_paths} -eq 0 ]; then
        git-ls $ls_args
        # eval "$gls_command"
    else
        local here_path="$(pwd | sed 's/\ /\\\ /g')"
        for dir_path in "${dir_paths[@]}"; do
            echo
            echo -E "$dir_path:" | sed 's/\ /\\\ /g'
            cd $dir_path
            git-ls "${ls_args[@]}"
            # eval "$gls_command"
            cd $here_path
        done
    fi
}

# --------------------

# 几个文件一行，不显示文件详细信息
alias gl='gls'
alias gli='gls --ignore'
alias glhi='gls --has-ignore'
# 一个文件一行，显示详细信息
alias gll='gls -lh'
alias glli='gls -lh --ignore'
alias gllhi='gls -lh --has-ignore'

# alias gll='git ls-files | awk -F / '\''{print $1}'\'' | uniq | sed '\''s/\ /\\\ /g'\'' | xargs ls -dl --color=auto'

alias grm='git rm -rf'    # （删除并）暂存删除： grm 文件             ；用于替代rm
alias gmv='git mv'        # （移动并）暂存移动： gmv 文件 文件夹       ；用于替代mv

gdf() {
    if [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
        echo 'Usage:'
        echo '当前节点内:'
        echo '  gdf                [options] [[--] (诸)文件(夹)] : 跟踪文件未暂存的修改 '
        echo '  gdf-s[tage]        [options] [[--] (诸)文件(夹)] : ........已暂存...... '
        echo '  gdf-a[ll]          [options] [[--] (诸)文件(夹)] : ........一切的...... '
        echo
        echo '节点之间:'
        echo '  gdf    <node>      [options] [[--] (诸)文件(夹)] : 工作目录 与 <node>提交版本 的区别'
        echo '  gdf-s  <node>      [options] [[--] (诸)文件(夹)] : 索引 与 <node>提交版本 的区别'
        echo '  gdf  <node> <node> [options] [[--] (诸)文件(夹)] : 两个node的区别'
        echo
        echo '<node> = 分支名/glg中的版本哈希/HEAD/HEAD^/HEAD~n/HEAD@{n}'
    else
        git diff "$@"
    fi
}
alias gdf-s='git diff --staged'
alias gdf-stage='git diff --staged'
alias gdf-a='git diff HEAD'
alias gdf-all='git diff HEAD'

guam(){
    if [ $# = 0 ] || [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ] ; then
        echo 'Usage: 撤销对 已跟踪文件 的修改与暂存，无法撤销修改先前未跟踪的文件'
        echo ' gum  <filename> [ <filename> [ <filename> ...]]'
        echo ' gum  -a|--all : 所有为暂存的修改'
    elif [ "$1" = '-a' ] || [ "$1" = "--all" ]; then
        # cd `git rev-parse --show-toplevel`
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
        git reset HEAD
    else
        for i in "$@"; do
            git reset HEAD "$i"
        done
    fi
}
gum(){
    if [ $# = 0 ] || [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ] ; then
        echo 'Usage: 撤销对 已跟踪文件 [未`git add`]的修改，无法撤销修改先前未跟踪的文件'
        echo ' gum  <filename> [ <filename> [ <filename> ...]]'
        echo ' gum  -a|--all : 所有为暂存的修改'
    elif [ "$1" = '-a' ] || [ "$1" = "--all" ]; then
        cd `git rev-parse --show-toplevel`
        git checkout  .
    else
        for i in "$@"; do
            git checkout -- "$i"
        done
    fi
}


# git untrack
alias gut='git rm -r --cached'

# 提交
alias gacm='git commit -am' # 即先gaa, 然后gcm
alias gcm='git commit -m'  # 提交：gcm "xxx" [options]
alias gcma='git commit --amend' # 先add，再覆盖上一次提交：gcma，然后弹出文本编辑器，编辑上次提交的说明
gucm() # 直接回到历史版本
{
    if [ $# = 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        echo 'gumc: 封装了 `git reset --hard`'
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
    elif ! [ -z "$(git status --porcelain)" ]; then
        echo '请先git commit再gucm, 以使得目录clean(无未跟踪的文件, 无未提交的修改)'
        # `git reset --hard 版本`的原理: 将目标节点的跟踪文件全部拷贝到过来并暂存之, 然后commit
        #      无增量的跟踪文件 : 替换为目标节点的文件
        #      有增量(不论 跟踪未暂存/跟踪且暂存)的跟踪文件 : 全部删除增量, 不留档, 然后替换为目标节点的文件
        #      未跟踪的文件, 且在目标节点中有被跟踪同路径的文件, 则删除此未跟踪文件, 不存档, 然后替换为目标节点的文件
        #      未跟踪的文件, 且在目标节点中无被跟踪同路径的文件, 则保留此文件
    else
        # local answer=$(bash -c "read  -n 1 -p '请先git commit再reset，不然抛弃暂存和修改 无法恢复。是否继续reset [Y|N]' c; echo \$c")
        # echo
        # if [ "$answer" = "y" ] || [  "$answer" = "Y"  ]; then
        local target_version=$1
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
        # fi
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
        #       将HEAD 重置为 目标节点 : 即HEAD中跟踪文件全部git rm, 再将目标节点文件都拷贝过来, HEAD跟踪拷过来的文件
        #       工作目录中有增量(不论 未跟踪/跟踪未暂存/跟踪且暂存)的文件尽可能原样不变, 除非重新计算增量发生冲突 则[拒绝执行]
        #       工作目录中无增量的跟踪文件直接被替换成目标节点的文件
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
        local old_hash="$(git rev-parse ${old_name} | cut -c 1-7)"
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
        # echo '所有被跟踪文件(不论 修改未add/修改并add)必需先commit, 不然拒绝执行'
        # echo '未被跟踪的文件不必commit, 若被检出的同名文件覆盖,  则拒绝执行'
        # echo '未被跟踪的文件不必commit, 若未被检出的同名文件覆盖,  检出后保持不变'
        echo
        echo '检出部分文件: '
        echo '  gch <node> <file-or-dir>(s) : 将指定节点的指定文件(夹)拷到当前节点 并git add'
        echo '  gch <node> --all            : 将指定节点的所有跟踪文件(夹)拷到当前节点 并git add'
        echo '不论拷过来的文件, 在当前是什么状态(未跟踪/跟踪且未暂存/跟踪且已暂存/跟踪且无增量), 均可直接执行'
        echo
        echo '<node> = 分支名/glg中的版本哈希/HEAD/HEAD^/HEAD~n/HEAD@{n}'
    elif [ "$2" = '--all' ]; then
        cd `git rev-parse --show-toplevel`
        git checkout "$1" .
    elif [ "$2" = '--replace' ]; then
        git read-tree -um HEAD "$1"
    else
        git checkout "$@"
    fi
}

# git [要忽略的文件(夹) 的 相对当前目录的路径 或 绝对路径] x n，将其添加到repo根目录下的.gitignore
gi() { # git ignore
    for i in "$@"; do
        local target_path_to_git_root="$(git_path_to_root $i)"
        local gitignore="$(git_root)/.gitignore"
        echo "$target_path_to_git_root" >> $gitignore
    done
}

# 显示repo到repo根目录下的.gitignore
gic() { # git ignroe cat
    local gitignore="$(git_root)/.gitignore"
    cat $gitignore
}

# 编辑repo到repo根目录下的.gitignore
giv() { # git ignore vim
    local gitignore="$(git_root)/.gitignore"
    default_editor "$gitignore"
}

# 依照最新的.gitignore文件 忽略整个repo中的文件(夹)
giu()   # git ignore update: 修改.gitignore 后，忽略其中的文件，commit一版
{
    git rm -r --cached .  #清除缓存
    git add "$(git_root)" #重新trace file
    git commit -m "update .gitignore" #提交和注释
}

# 分支
gb()                      # 新建分支并检出到此分支： gb 分支名
{
    git branch $1 && git checkout $1
}
alias gbrm='git branch -d' # 删除分支：gbrm 分支名
alias gbls='git branch -avv' # 列出所有本地枝，及其关联的远枝： gbls
# alias gch='git checkout'    # 切换分支：gch 分支名/历史提交编号/HEAD^/HEAD/HEAD~n/HEAD@{n}, 要先git commit一次才能gch
alias gmg='git merge --no-ff' # 将当前枝与此分支合并（非快进）
alias gmgc='git merge --continue'
# 历史
# alias glg="git log --graph --oneline --all --pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cr %C(bold blue)%an%Creset %s' --abbrev-commit --date=short"  #列出提交历史图谱，含远仓、本仓
# alias glg="git log  --graph --abbrev-commit --oneline --pretty=format:'%C(yellow)%h%C(reset)%C(auto)%d%C(reset) %C(green)%cr %C(bold blue)%an%C(reset) %s' --date=short --all"  #列出提交历史图谱，含远仓、本仓
# alias glg1="git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset)%>|(20)%<(1)%<(15)%C(bold green)%ar%C(reset) %<(17,trunc)%C(bold blue)%an%C(reset) %C(white)%s%C(reset)%n%C(auto)%d%C(reset)' --all" #
# alias glg2="git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset)%C(auto)%d%C(reset)%>|(50)%<(1)%>(14)%C(bold green)%ar%C(reset) %C(bold cyan)%ad%C(reset) %C(dim white)%an%C(reset)%n%>|(25)%<(1)%s'  --date=format:'%Y-%m-%d' --all"
# # '%Y-%m-%d 周%w %H:%M:%S'
# alias glg=" "
glg()
{
    if [ $# -eq 0 ]; then
        local cmd=' --all'
    elif [ "$1" = '--all-stash' ]; then
        local cmd=' --all $(git reflog show --format="%h" stash)'
    elif [ "$1" = '--no-stash' ]; then
        local cmd=' --exclude=refs/stash --all'
    else
        cat << EOF
glg                  : show the current one stash on each node
glg --all-stash      : show all stashes on each node
glg --no-stash       : show no stash on each node
EOF
        return
    fi
    alias _glg="git log --graph --abbrev-commit --decorate=no --date=format:'%Y-%m-%d %H:%I:%S' --pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cr %C(bold blue)%an%Creset %C(bold 0)%s%C(reset)' $cmd"
    alias _glg_table="git log --graph --abbrev-commit --decorate=no --date=format:'%Y-%m-%d %H:%I:%S' --format=format:'%C(yellow)%h%C(reset) %C(auto)%d%C(reset) %C(green)%>|(50)%ad%C(reset)  %C(blue)%<(16,trunc)%an%C(reset) %C(bold 0)%>|(1)%s%C(reset)' $cmd"
    eval _glg
}
# "$(git for-each-ref --format="%(refname)" refs/heads/ refs/remotes/ | grep -v "\.stgit$")"
#
alias glgs='glg --simplify-by-decoration'               #列出简化历史图谱
alias ghs='git reflog'   # 按时间顺序列出 版本重置（git reset）、提交（git commit）
# 远仓
alias gra='git remote add'        # 关联远仓：gra 远仓名（即远程repo在本地的名字） 远程repo的网址

alias grrm='git remote rm'      # 取关远仓：    grrm 远仓名
alias grrn='git remote rename'  # 重命名远仓：  grrn 远仓名
alias grls='git remote show'    # 列出远仓：    grls
                             # 显示远仓信息： grls 远仓名
# 远枝
# alias gbu='git branch -u'                # 将当前枝关联远枝：           gup 远仓名 远枝名
git_current_branch()
{
    git branch | grep \* | cut -d ' ' -f2
}
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


# 推拉



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

#  初次推送用，关联远枝并推送，若远仓无此远枝，则创建之
# gpsu [远仓名 [远枝名]]，  默认远仓名=origin， 默认远枝名=本地现枝名
# gpsu()
# {
    # gbu $*
    # git push
# }
alias gps='git push'     # 推送当前枝：            gps [ 远仓名 [远枝名]]
alias gfc='git fetch'           # 拉去到当前枝：          gfc [ 远仓名 [远枝名]]
# gplu [远仓名 [远枝名]],   初次拉用
gplu()
{
    gbu $*
    git pull
}
alias gpl='git pull'            # 拉去到当前枝并与之合并：  gpl [ 远仓名 [远枝名]]
                                # gps，gfc，gpl皆可省参数：
                                # 若该远仓的远枝已关联，则[远枝名]不写
                                # 若还只关联一个远仓，则[ 远仓名 [远枝名]]不写
alias gcl='git clone'           # 克隆远枝：gcl 远仓网址
                                # 请用http格式，若用ssh格式则需要验证密钥
ghcl() {
    local url="$1"; shift
    local protocol="${url%%://*}"  # 第一个'://'左侧
    local user_repo="${url#*://}"  # 第一个'://'右侧
    if [ "$protocol" = "$url" ]; then
        local protocol='ssh'
    fi
    if ! [[ "$protocol" =~ '^(https|ssh)$' ]]; then
        echo 'invaslid $protocol' >&2
    fi

    local user="${user_repo%%:*}"  # 第一个':'左侧
    local repo="${user_repo#*:}"   # 第一个':'右侧
    if [ "$user" = "$user_repo" ]; then
        local user='hyliang96'
    fi

    if [ "$protocol" = 'ssh' ]; then
        git clone "git@github.com:${user}/${repo}" "$@"
    elif [ "$protocol" = 'https' ]; then
        git clone https://github.com/${user}/${repo} "$@"
    fi
}

gmed()  # 修改提交信息：  gmed <版本id>
#    只接收一个版本id
#    只接收版本hash，不接受HEAD, HEAD^, HEAD@{n}
#    不能是第一个版本
{
    local commitid=$1
    GIT_SEQUENCE_EDITOR="sed -i -re 's/^pick ${commitid}/r ${commitid}/'" git rebase -i ${commitid}^
}


alias gpr='git pull --rebase'
alias grbc='git rebase --continue'

# 弯弓提交到上游分支
gbps() {
    local current="$(git rev-parse --abbrev-ref HEAD)"
    if [ "$current" = 'HEAD' ]; then
        echo "You are not at the end of a branch, please checkout to a branch before 'bow push'."
        return
    fi
    git pull --rebase
    local upstream="$(git rev-parse --abbrev-ref ${current}@{upstream})"
    local remote=$(echo "${upstream}" | awk -F '/' '{print $1}')
    local remote_repo=$(echo "${upstream}" | awk -F '/' '{print $2}')
    git checkout $upstream
    git merge --no-ff $current
    git push $remote HEAD:$remote_repo
    git checkout $current
    git merge $upstream
}

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
# -------------------------------------------------------------
# -- 自动添加.gitkeep到文件夹下，以使得git add能加入空文件夹

# _level a/b/c/d （只接受一个参数）
# 输出
# a
# a/b
# a/b/c
_level()
{
    local SAVE_IFS=$IFS
    IFS=$(echo -en "\n\b")
    local apath=$1
    while [ 1 ]; do
        echo $apath
        local newpath=$(dirname $apath)
        if [ "$newpath" == "$apath" ]; then
            break
        else
            apath=$newpath
        fi
    done
    IFS=$SAVE_IFS
}

# _not_exist_dir path1 [path2 [path3 ....]]
# 输出 一行一个路径，只输出存在的路径
_not_exist_dir()
{
    local SAVE_IFS=$IFS
    IFS=$(echo -en "\n\b")
    local i=
    for i in $*; do
        local tmp=($(_level $i))
        for j in ${tmp[@]}; do
            ! [ -d $j ] &&  echo $j
        done
    done
    IFS=$SAVE_IFS
}

# _getpath path ... -x=xxx path -xxx path  --xx=xx path --xxx
# -x --xxx -x=xxx --xx=xxx 都是参数
# 输出 path path .. path
_getpath()
{
    local SAVE_IFS=$IFS
    IFS=$(echo -en "\n\b")
    local i=
    for i in $* ; do
        ! [ "${i:0:1}" = "-" ] && echo $i
    done

    IFS=$SAVE_IFS
}

# gmd path [path [path ..]]] [-参数]
# 每创建一个新文件夹，会在其下自动加一个.gitkeep文件
# 参数需要写成  -x -xyz --xxx -x=abc --xx=abc
# 不可写成 -x abc 或 --xx abc, 即必须有等号，等号前后不能有空格
# 参数含义同mkdir
gmd()
{
    local SAVE_IFS=$IFS
    IFS='
'
    local tmp=($(_not_exist_dir $(_getpath $*)))

    mkdir $*

    local i=
    for i in ${tmp[@]}; do
        echo 2: $i
        if [ -d $i ]; then
            touch $i/.gitkeep
        else
            echo $i not exist
        fi
    done

    IFS=$SAVE_IFS
}

# gitkeep [path [path ..]] # 缺省为当前目录
# 将当前目录下的所有空文件夹下创建.gitkeep文件
gitkeep()
{
    if [ $# -eq 0 ]; then
        find . -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;
    else
        find $* -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;
    fi
}

# -------------------------------------------------------------------------
# github api
gh-help()
{
cat << EOF
gh test                   : test github ssh connection
gh ls                     : list all your repo, show whether is private
gh new {repo_name}        : create a private repo
gh new {repo_name} public : create a public repo
gh cl|clone [{protocol}://][{github_username}:]{remote_repo_name} [git_clone_options]
                          : git clone from github
    {protocol} = https | ssh(default)
gh add [{remote} [{github_username}]] {remote_repo_name}
                          : add a github repo as
    default {remote} = origin
    default {github_username} = local git username, see \`git config user.name\`
EOF
}

gh()
{
    if [ "$1" = 'test' ]; then
        ssh -T git@github.com # 测试github的ssh连接
    elif [ "$1" = 'ls' ]; then
    # list all remote repo
        echo $(curl -H "Authorization: token $(<~/.ssh/github/github.token)" "https://api.github.com/user/repos?per_page=100" 2>/dev/null | \
        grep -E '^    "name":|^    "private": ' ) | \
        sed 's/"name": "/\
/g' | \
        sed 's/"\, "private": false\,//g' | \
        sed 's/"\, "private": true,/ \[private\]/g'
    elif [ "$1" = 'new' ]; then
    # create new remote repo
        local repo_name="$2"
        if [ $# -eq 3 ]  && [ "$3" = 'public' ]; then
            local ifPrivate=false
        else
            local ifPrivate=true
        fi
        curl -H "Authorization: token $(<~/.ssh/github/github.token)" "https://api.github.com/user/repos?per_page=100" --data "{ \"name\": \"$repo_name\",  \"private\": $ifPrivate }"
    elif [ "$1" = 'add' ]; then
        shift
        grgh "$@"
    elif [[ "$1" =~ '^(clone|cl)$'  ]]; then
        shift
        ghcl "$@"
    else
        gh-help
    fi
}
# git remote git hub
grgh()  # 关联github上的远程repo
# 先在github上建立一个repo
# 然后用此，用法见下
{
    if [ $# = 1 ]; then
        local user=`git config user.name`
        local name=origin
        local repo=$1
    elif [ $# = 2 ]; then
        local user=`git config user.name`
        local name=$1
        local repo=$2
    elif [ $# = 3 ]; then
        local name=$1
        local user=$2
        local repo=$3
    else
        echo 'Usage: gh [remote [github_username]] remote_repo_name'
        echo '    default remote: origin'
        echo '    default github_username: local git username, see in `git config user.name`'
        return
    fi
    echo $user $name $repo
    git remote add $name git@github.com:$user/$repo.git
}



