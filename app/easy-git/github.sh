#!/usr/bin/env bash

alias gcl='git clone'           # 克隆远枝：gcl 远仓网址
                                # 请用http格式，若用ssh格式则需要验证密钥

# -------------------------------------------------------------------------
# github api
gh_help()
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
        echo $(curl -H "Authorization: token $(cat ~/.ssh/github/github.token)" \
               "https://api.github.com/user/repos?per_page=100" 2>/dev/null |
        grep -E '^    "name":|^    "private": ' ) |
        sed 's/"name": "/'$'\\\n''/g' |
        sed 's/"\, "private": false\,//g' |
        sed 's/"\, "private": true,/ \[private\]/g'
    elif [ "$1" = 'new' ]; then
    # create new remote repo
        local repo_name="$2"
        if [ $# -eq 3 ]  && [ "$3" = 'public' ]; then
            local ifPrivate=false
        else
            local ifPrivate=true
        fi
        curl -H "Authorization: token $(cat ~/.ssh/github/github.token)" \
            "https://api.github.com/user/repos?per_page=100"  \
            --data "{ \"name\": \"$repo_name\",  \"private\": $ifPrivate }"
    elif [ "$1" = 'add' ]; then
        shift
        grgh "$@"
    elif [[ "$1" =~ '^(clone|cl)$'  ]]; then
        shift
        ghcl "$@"
    else
        gh_help
    fi
}

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


