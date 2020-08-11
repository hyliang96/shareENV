#!/usr/bin/env bash

# git [要忽略的文件(夹) 的 相对当前目录的路径 或 绝对路径] x n，将其添加到repo根目录下的.gitignore
gi() { # git ignore
    local i
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


