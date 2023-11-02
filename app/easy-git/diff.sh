#!/usr/bin/env bash


__gdf_help__()
{
    local cmd="gdf"
    cat << EOF
Usage:
当前节点内:
  ${cmd}                [options] [[--] (诸)文件(夹)] : 跟踪文件未暂存的修改
  ${cmd}-s[tage]        [options] [[--] (诸)文件(夹)] : ........已暂存......
  ${cmd}-a[ll]          [options] [[--] (诸)文件(夹)] : ........一切的......

节点之间:
  ${cmd}    <node>      [options] [[--] (诸)文件(夹)] : 工作目录 与 <node>提交版本 的区别
  ${cmd}-s  <node>      [options] [[--] (诸)文件(夹)] : 索引 与 <node>提交版本 的区别
  ${cmd}  <node> <node> [options] [[--] (诸)文件(夹)] : 两个node的区别
<node> = 分支名/glg中的版本哈希/HEAD/HEAD^/HEAD~n/HEAD@{n}

以上\`gdf\`换成\`gdfl\`, 则只列出相异文件的路径, 不显示文件diff的内容
EOF
}



gdf() {
    if [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
        __gdf_help__
    else
        git diff "$@"
    fi
}

gdfl() {
    if [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
        __gdf_help__
    else
        git diff --name-only "$@"
    fi
}

alias gdf-s='git diff --staged'
alias gdfl-s='git diff --name-only --staged'

alias gdf-a='git diff HEAD'
alias gdfl-a='git diff HEAD --name-only'

