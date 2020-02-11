#!/usr/bin/env bash


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
        git ls-files -o -i --exclude-standard | sed 's/\/$//g'
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


