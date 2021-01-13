#!/usr/bin/env bash

# git utils
git_root() {
    git rev-parse --show-toplevel 2>/dev/null
}
git_path_to_root() {
    local abs_path="$(abspath $1)"
    local git_path="$(git_root)"
    echo "${abs_path/${git_path}/}"
}
git_current_branch()
{
    # git branch | grep \* | cut -d ' ' -f2
    git rev-parse --abbrev-ref HEAD
}
get_hash()
{
    git rev-parse --short "$@"
}
get_long_hash()
{
    git rev-parse "$@"
}

# 返回HEAD的最高祖宗的 长hash
git_root_commit()
{
    git rev-list --max-parents=0 HEAD 2>/dev/null
}

# 若HAED指向某分支的结尾, 返回此分支的名称; 否则返回HEAD
get_node_name()
{
    git rev-parse --abbrev-ref "$@"
}


git-local-branch-exists()
{
    if git show-ref --verify --quiet refs/heads/"$1" 2>/dev/null; then
        echo yes
    fi
}

git-remote-branch-exists()
{
    if git show-ref --verify --quiet refs/remotes/"$1" 2>/dev/null; then
        echo yes
    fi
}

git-branch-exists()
{
    if [ "$(git-local-branch-exists "$1")" = 'yes' ]; then
        echo local_branch
    elif  [ "$(git-remote-branch-exists "$1")" = 'yes' ]; then
        echo remote_branch
    fi
}

