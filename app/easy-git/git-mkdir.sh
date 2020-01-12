#!/usr/bin/env bash


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



