#!/usr/bin/env bash


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
