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
    git branch | grep \* | cut -d ' ' -f2
}
get_hash()
{
    git rev-parse --short "$@"
}

# 若HAED指向某分支的结尾, 返回此分支的名称; 否则返回HEAD
get_node_name()
{
    git rev-parse --abbrev-ref "$@"
}
