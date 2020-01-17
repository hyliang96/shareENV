#!/usr/bin/env bash

# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
easy_git_dir=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"; pwd)

if [ "$(uname)" = "Darwin" ]; then
    if ! [ -x "$(command -v tig)" ]; then
        echo 'to install tig, run `brew install tig`'
    fi
else
    export PATH=$PATH:${easy_git_dir}/bin
fi

. $easy_git_dir/utils.sh

. $easy_git_dir/ignore.sh
. $easy_git_dir/git-mkdir.sh
. $easy_git_dir/git-ls.sh
. $easy_git_dir/diff.sh
. $easy_git_dir/log.sh

. $easy_git_dir/in_version.sh
. $easy_git_dir/version.sh
. $easy_git_dir/branch.sh
. $easy_git_dir/stash.sh
. $easy_git_dir/remote.sh
. $easy_git_dir/github.sh


# release this variable in the end of file
unset -v easy_git_dir



