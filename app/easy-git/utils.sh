#!/usr/bin/env bash

# git utils
git_root() {
    git rev-parse --show-toplevel
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
