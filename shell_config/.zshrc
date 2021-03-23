#!/usr/bin/env zsh

# DotFileDebug=1
[ $DotFileDebug -ne 0 ] && echo share .zshrc >&2
# -------------------------------------------------------------------------
# 定义安装函数

# Install antigen.zsh if not exist
check_antigen_install()
{
    [ $DotFileDebug -ne 0 ] && echo share .zshrc - instal zsh >&2

    if [ ! -f "$ANTIGEN" ]; then
        echo "Installing antigen ..."
        [ ! -d "$HOME/.local" ] && mkdir -p "$HOME/.local" 2> /dev/null
        [ ! -d "$HOME/.local/bin" ] && mkdir -p "$HOME/.local/bin" 2> /dev/null
        [ ! -f "$HOME/.z" ] && touch "$HOME/.z"
        local URL="http://git.io/antigen"
        local TMPFILE="/tmp/antigen.zsh"
        if [ -x "$(which curl)" ]; then
            curl -L "$URL" -o "$TMPFILE"
        elif [ -x "$(which wget)" ]; then
            wget "$URL" -O "$TMPFILE"
        else
            echo "ERROR: please install curl or wget before installation !!"
            exit
        fi
        if [ ! $? -eq 0 ]; then
            echo ""
            echo "ERROR: downloading antigen.zsh ($URL) failed !!"
            exit
        fi;
        echo "move $TMPFILE to $ANTIGEN"
        mv "$TMPFILE" "$ANTIGEN"
    fi

    [ $DotFileDebug -ne 0 ] && echo share .zshrc -  Initialize command prompt >&2
}

check_jump_install()
{
    [ $DotFileDebug -ne 0 ] && echo share .zshrc - load autojump >&2

    # antigen bundle autojump # 自动跳转
    if [ "$(uname)" = "Darwin" ]; then
        # mac
        if [  -x "$(command -v autojump)"  ]; then
            # if [ -f /usr/local/etc/profile.d/autojump.sh ]; then
                # # . /usr/local/etc/profile.d/autojump.sh
            # else
                # echo 'can not find the path to autojump' >&2
            # fi
            antigen bundle autojump
        else
            echo 'no `autojump` on your mac, run `brew instal autojump` to install it' >&2
        fi
    else
        # linux
        if ! [ -d ~/.autojump ]; then
            # 安装autojump
            cd $my
            git clone git://github.com/joelthelion/autojump.git
            cd autojump
            ./install.py
            cd $my
            rm autojump -rf
        fi
        # linux上用户装在自己的home下，则用bundle加载不了，要在这里手动加载
        [ -f ~/.autojump/etc/profile.d/autojump.sh ] && . ~/.autojump/etc/profile.d/autojump.sh
    fi

    [ $DotFileDebug -ne 0 ] && echo share .zshrc - antigen bundle >&2
}

check_fzf_install()
{
    if [ "$(uname)" = "Darwin" ]; then
        if ! [ -x "$(command -v fzf)" ]; then
        # if ! builtin type fzf >/dev/null 2>&1; then
            if [ -x "$(command -v brew)" ]; then
                brew install fzf
            else
                echo 'there is no brew on your mac; cannot `brew  install fzf`' >&2
            fi
        fi
    else
        export FZF_BASE="${HOME}/.fzf"
        # export FZF_BASE="$serverENV/app/fzf"
        if [ ! -x $FZF_BASE/bin/fzf ] 2>&1; then
            echo 'There is no fzf. Installing to '"$FZF_BASE" >&2
            git clone --depth 1 https://github.com/junegunn/fzf.git $FZF_BASE
            ${FZF_BASE}/install --bin
        fi
    fi
}


# -------------------------------------------------------------------------
# shell 基础设置

# Initialize command prompt
export PS1="%n@%m:%~%# "

# Enable 256 color to make auto-suggestions look nice
export TERM="xterm-256color"

# Load local bash/zsh compatible settings
_INIT_SH_NOFUN=1
[ -f "$HOME/.local/etc/init.sh" ] && source "$HOME/.local/etc/init.sh"

# exit for non-interactive shell
[[ $- != *i* ]] && return

# WSL (aka Bash for Windows) doesn't work well with BG_NICE
[ -d "/mnt/c" ] && [[ "$(uname -a)" == *Microsoft* ]] && unsetopt BG_NICE

# 禁用bracketed-paste-magic, 避免zsh5.1.1中把unicode字符粘到zsh命令行下时出乱码, 必需在加载oh-my-zsh前写本行
# 详见：https://github.com/robbyrussell/oh-my-zsh/issues/5569#issuecomment-491504337
DISABLE_MAGIC_FUNCTIONS=true


# -------------------------------------------------------------------------
# antigen

# Antigen: https://github.com/zsh-users/antigen
ANTIGEN="$HOME/.local/bin/antigen.zsh"
# install zsh
check_antigen_install

[ $DotFileDebug -ne 0 ] && echo share .zshrc - Initialize antigen >&2
# Initialize antigen
source "$ANTIGEN"
# -------------------------------------------------------------------------
# zsh 插件
[ $DotFileDebug -ne 0 ] && echo share .zshrc - antigen boundle >&2

# Initialize oh-my-zsh
antigen use oh-my-zsh

# 历史命令搜索
# antigen bundle zsh-users/zsh-history-substring-search
check_fzf_install
antigen bundle fzf   # 模糊搜索, 可以搜文件夹下路径,历史命令,历史路径
antigen bundle marlonrichert/zsh-hist

# default bundles
# visit https://github.com/unixorn/awesome-zsh-plugins
# antigen bundle git
# antigen bundle heroku
antigen bundle pip
antigen bundle svn-fast-info
# antigen bundle command-not-find

antigen bundle colorize
antigen bundle github
antigen bundle python
# antigen bundle z               # 跳转历史目录
# antigen bundle rupa/z z.sh
antigen bundle skywind3000/z.lua # https://www.v2ex.com/t/532304

export _ZL_ADD_ONCE=1   # 若为0 则prompt显示一次则计数加1, 若为1则 cd到目录一次则计数加1
export _ZL_MATCH_MODE=1 # 启用增强匹配模式
export _ZL_NO_ALIASES=0 # 不用预设alias, 用自己定义的alias


antigen bundle zdharma/fast-syntax-highlighting    # zsh 命令的语法高亮
# antigen bundle zsh-users/zsh-syntax-highlighting # zsh 命令的语法高亮
antigen bundle zsh-users/zsh-autosuggestions     # 根据命令开头 补全历史命令,右键使用补全,上下键翻历史
antigen bundle zsh-users/zsh-completions         # tab键自动补全
# antigen bundle supercrabtree/k
antigen bundle Vifon/deer

antigen bundle willghatch/zsh-cdr
# antigen bundle zsh-users/zaw

# 换主题
# 更多主题见：https://github.com/robbyrussell/oh-my-zsh/wiki/themes
# bureau, ys, agnoster, apjanke/agnosterj-zsh-theme
# antigen theme apjanke/agnosterj-zsh-theme
# source /Users/mac/.antigen/bundles/apjanke/agnosterj-zsh-theme/agnosterj.zsh-theme

antigen theme hyliang96/my_agnoster # https://github.com/hyliang96/my_agnoster.git
# set option to '' to disable it
agnoster_time=1
agnoster_env=1
# agnoster_newline=1

[ $DotFileDebug -ne 0 ] && echo share .zshrc antigen apply >&2
antigen apply


# -------------------------------------------------------------------------
# fzf的原生快捷键
# ctrl+r: 历史命令命令, 时间排序, 模糊搜索, 选中结果paste到终端
# ctrl+t: 当前路径往下, 模糊搜索文件或目录, 选中结果paste到终端
# esc+c: 当前路径往下, 模糊搜索命令, cd到选择目录
# -------------------------------------------------------------------------
# 我的alias
# z : fzf搜索目录跳转
# z.. foo : fzf搜索, 跳转到父目录中 名称含foo的那一级
# zh / ctrl+h : fzf搜索历史路径并跳转
# h : fzf搜索历史命令 多选 输出到终端

# 快速跳转的alias

[ "$(alias z)" != '' ] && unalias z     # 解绑antigen bundle z.lua当中的alias z, 换为zz
alias zz=_zlua

z()
{
    if [[ "$1" =~ '^(-h|--help)$' ]]; then
        cat << EOF
_zlua [-c] 的封装的帮助:
    z [options] [.] 路径中间字段 路径中间字段 路径结尾字段
    z [options] [.] 路径中间字段 路径中间字段 路径未必结尾字段 $
    z [options] [.] 路径中间字段 路径中间字段 /
    加 . : 从当前路径往下匹配
_zlua [其他option] 没有封装
EOF
        echo
        echo 原生的帮助:
        _zlua -h
    elif [ "$1" = '.' ]; then
        shift  # z匹配当前路径 的历史子路径 -> fzf模糊匹配
        if [ $# -eq 0 ]; then
            _zlua -I -c .
        else
            _zlua -I -c "$@"
        fi
    elif ! [[ "$1" =~ '^-' ]]; then # z匹配历史路径, 按访问频率排序 -> fzf模糊匹配
        if [ $# -eq 0 ]; then
            _zlua -I .
        else
            _zlua -I "$@"
        fi
    else
        _zlua "$@"
    fi
}

alias z..='_zlua -b' # z.. foo : 跳转到父目录中 名称含foo的那一级

zh(){        # z匹配历史路径, 按之间排序 -> fzf模糊匹配
    if [ $# -eq 0 ]; then
        _zlua -I -t .
    else
        _zlua -I -t "$@"
    fi
}
zle -N zh
bindkey '^h' zh


# 再历史命令中模糊搜索, 多选 (tab选中,shift-tab取消选中), 回车输出终端
h()
{
    local if_number=false
    local if_no_fzf=false

    if [[ "$1" =~ ^(-h|--help|help)$ ]]; then
        cat <<-EOF
\`h\`:
    fuzzy search history command and multi select with \`tab\`/\`shift-tab\`
    \`enter\` to print according to your selecting order
Usage:
    h [option]           : fuzzy search history command
    h [option] <num>     : directly print the last <num> commands
Options:
    -n|--number          : with the line number of a command
EOF
    return
    fi

    while [ $# -ne 0 ]; do
        if [[ "$1" =~ ^(-n|--number)$ ]]; then
            local if_number=true
            shift
        elif [[ "$1" =~ ^[0-9]+$ ]]; then
            local if_no_fzf=true
            local line_number="$1"
            shift
        fi
    done

    if [ "${if_no_fzf}" = true  ];then
        if [ "${if_number}" = true  ]; then
            history -${line_number}
        else
            history  -${line_number} | sed 's/^ *[0-9]* *//'
        fi
    else
        if [ "${if_number}" = true  ]; then
            print "$(history | fzf --tac -m )"
        else
            print -z "$(history | sed 's/^ *[0-9]* *//' | fzf --tac -m )"
        fi
    fi
}

# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc set syntax highlighting >&2

# ------------
# zdharma/fast-syntax-highlighting 的主题
fast-theme $shareENV/shell_config/my_theme.ini >/dev/null

# -----------------
# # zsh-users/zsh-syntax-highlighting 的主题

# # syntax color definition
# ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)

# typeset -A ZSH_HIGHLIGHT_STYLES

# ZSH_HIGHLIGHT_STYLES[default]=none
# ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=009
# ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=red,bold  # =fg=009,standout
# ZSH_HIGHLIGHT_STYLES[alias]=fg=cyan,bold
# ZSH_HIGHLIGHT_STYLES[builtin]=fg=cyan,bold
# ZSH_HIGHLIGHT_STYLES[function]=fg=cyan,bold
# ZSH_HIGHLIGHT_STYLES[command]=fg=white,bold
# ZSH_HIGHLIGHT_STYLES[precommand]=fg=white,underline
# ZSH_HIGHLIGHT_STYLES[commandseparator]=none
# ZSH_HIGHLIGHT_STYLES[hashed-command]=fg=009
# ZSH_HIGHLIGHT_STYLES[path]=fg=214,underline
# ZSH_HIGHLIGHT_STYLES[globbing]=fg=063
# ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=white,underline
# ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=none
# ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=none
# ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=none
# ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=063
# ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=063
# ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=009
# ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=009
# ZSH_HIGHLIGHT_STYLES[assign]=none


# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc - set bindkey >&2

# 10ms for key sequences
KEYTIMEOUT=1

# setup for deer
autoload -U deer
zle -N deer

# default keymap
bindkey -s '\ee' 'vim\n'
bindkey '\eh' backward-char
bindkey '\el' forward-char
bindkey '\ej' down-line-or-history
bindkey '\ek' up-line-or-history
bindkey '\e[A' up-line-or-search
bindkey '\e[B' down-line-or-search
# bindkey '\eu' undo
bindkey '\eH' backward-word
bindkey '\eL' forward-word
bindkey '\eJ' beginning-of-line
bindkey '\eK' end-of-line

bindkey -s '\eo' 'cd ..\n'
bindkey -s '\e;' 'll\n'

bindkey '\e[1;3D' backward-word
bindkey '\e[1;3C' forward-word
bindkey '\e[1;3A' beginning-of-line
bindkey '\e[1;3B' end-of-line
bindkey '\e[1~' beginning-of-line # Home
bindkey '\e[4~' end-of-line # End
bindkey '\e[H' beginning-of-line # Home
bindkey '\e[F' end-of-line # End

bindkey '\ev' deer



# ctrl+u
bindkey \^U backward-kill-line
# iterm2 maps sfhit+backspace to  ᜤ , 删除一行




# bindkey '^f' fzf-history-widget

to-clipboard() { echo -n "$BUFFER" | timeout 0.1 nc localhost 8377; }
zle -N to-clipboard
# to-clipboard-clear() { echo -n "$BUFFER" | timeout 0.1 nc localhost 8377; BUFFER= ; }
# zle -N to-clipboard-clear
# to-history() { print -S "$BUFFER"; }
# zle -N to-history
# to-history-clear() { print -S "$BUFFER" ; BUFFER= ; }
# zle -N to-history-clear
# # bindkey '^s' to-history       # ctrl+s 保存到命令历史; 然后清空当前命令


# 解绑 ctrl+s ctrl+q
bindkey -r '^q'
bindkey -r '^s'
# stty start undef
# stty stop undef
# setopt noflowcontrol
# stty -ixon
# stty -ixoff
#
# 多行提示: 若显示形如"> ", "if>", "function> "的提示的代码块,
# 去掉多行提示: 按ctrl+q, 中断当前命令, 新起一个 转换为无'>'提示的多行命令

bindkey 'ç'  to-clipboard
# 若无多行提示: alt+c, 把当前目录复制到剪切板 (服务器剪切板可以与笔记本的同步)
# 若有多行提示: 先按alt+q, 新起一个 转换为无'> xx'提示的多行命令, 再按alt+c

bindkey œ push-line-or-edit  # 暂存当前 到命令栈(zsh-hist插件的栈) 和 命令到历史(~/.zsh_history)
# 触发:
# * 若无多行提示: 按一次alt+q
# * 若有多行提示, 先按alt+q, 新起一个 转换为无'> xx'提示的多行命令, 再按alt+q
# 作用:
# * 触发后, 将当前命令保存到命令栈, 并清空当前行,
# * 在空行, 直接回车/输其他命令再回车/输其他命令再alt+q , 则前一命令保存到历史(~/.zsh_history)

bindkey © get-line           # alt+g, 命令栈出一个命令

# `hist l`                      罗列命令栈
# `hist g {-n|id|command}`      获取命令, 但不出栈
# `hist f {-n|id|command}`      获取命令, 但出栈
# `hist e {-n|id|command}`      编辑命令, 出栈, 编辑后保存到~/.zsh_history 和栈
# `hist d {-n|id|command}`      从栈与中~/.zsh_history 删除命令


bindkey Ω undo   # alt+z 撤销命令行下的文本操作
# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc - set option >&2

# options
unsetopt correct_all

setopt BANG_HIST                 # Treat the '!' character specially during expansion.
setopt INC_APPEND_HISTORY        # Write to the history file immediately, not when the shell exits.
setopt SHARE_HISTORY             # Share history between all sessions.
setopt HIST_EXPIRE_DUPS_FIRST    # Expire duplicate entries first when trimming history.
setopt HIST_IGNORE_DUPS          # Don't record an entry that was just recorded again.
setopt HIST_IGNORE_ALL_DUPS      # Delete old recorded entry if new entry is a duplicate.
setopt HIST_FIND_NO_DUPS         # Do not display a line previously found.
setopt HIST_IGNORE_SPACE         # Don't record an entry starting with a space.
setopt HIST_SAVE_NO_DUPS         # Don't write duplicate entries in the history file.
setopt HIST_REDUCE_BLANKS        # Remove superfluous blanks before recording entry.
setopt HIST_VERIFY               # Don't execute immediately upon history expansion.
# setopt interactivecomments       # 允许终端允许的命令行里带注释

# source function.sh if it exists
[ -f "$HOME/.local/etc/function.sh" ] && . "$HOME/.local/etc/function.sh"

# ignore complition
zstyle ':completion:*:complete:-command-:*:*' ignored-patterns '*.pdf|*.exe|*.dll'
zstyle ':completion:*:*sh:*:' tag-order files


# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc - Coreutils color scheme >&2

# 终端使用 Coreutils 配色方案
# 采用Coreutils的gdircolor配色，修改~/.dir_colors(自定义配色)
# 以修改ls命令使用的环境变量LS_COLORS（BSD是LSCOLORS）
# 效果：不同类型的文件有不同颜色，如图水红色，文件夹群青色...
#
# mac 上有gls，用以代替ls
# mac上ls不支持 --show-control-chars --color=auto
# 当安装了coreutils时， gls --color=auto 默认加载 coreutils 配色
# coreutils安装方法：brew install coreutils

if [ "$(uname)" = "Darwin" ]; then
    check_coreutils_install()
    {
        if [ -d /usr/local/opt/coreutils/libexec/gnubin ] && [ -x /usr/local/bin/gls ]; then
            return
        fi

        if [ -x "$(command -v brew)" ]; then
            echo 'You have installed `brew`'
        else
            echo 'You have not installed `brew`'
            return
        fi

        if [ "$(brew list | grep coreutils)" != "" ]; then
            echo 'You have installed `coreutils` with `brew`'
        else
            echo 'You have not installed `coreutils` with `brew`'
            echo 'without `coreutils`, `ls` will be colored vanillaly'
            echo 'To install `coreutils`, run `brew install coreutils`'
            brew install coreutils
            return
        fi

        if [  -x "$(command -v gls)"  ]; then
            echo 'You have command `gls`, which is a submodule of `coreutils`'
        else
            echo 'You have no command `gls`, which is a submodule of `coreutils`'
            echo '`command -v gls` returns'
            command -v gls
            echo 'To check gls link is alive, check if there is a link'
            echo '   /usr/local/bin/gls -> ../Cellar/coreutils/<version_number>/bin/gls'
            ls -l /usr/local/bin/gls
            return
        fi

        local coreutils_path="$(brew --prefix coreutils)/libexec/gnubin"
        if [ -d "$coreutils_path" ]; then
            echo "the path of \`coreutils\` is $coreutils_path, it should be added into PATH"
            echo "everything is ok with the gls's color scheme on your mac"
            echo 'You can alias `ls` as `gls` to use `gls`'\''s color scheme'
        else
            echo 'The  path of `coreutils` is missing, it should be $(brew --prefix coreutils)/libexec/gnubin/'
            echo 'while `brew --prefix coreutils` returns wrongly:'
            brew --prefix coreutils
            echo 'it might be "/usr/local/opt/coreutils"'
            return
        fi
    }

    check_coreutils_install
    if [ -d /usr/local/opt/coreutils/libexec/gnubin ] && [ -x /usr/local/bin/gls ]; then
        PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH" # 添加coreutils到PATH
        alias ls='/usr/local/bin/gls --show-control-chars  --color=auto' # gls 被 git ls-files 的alias占用了，使用上面写绝对路径
        eval `gdircolors -b $HOME/.dir_colors`   # 启用配色方案
    fi
fi
# linux 的 ls默认上色了，加载 coreutils 配色


# 将777权限的文件在ls时，显示为文灰底紫
LS_COLORS=`echo $LS_COLORS | sed -E 's/ow=[0-9;]+://g'`:'ow=1;34;7:' ; export LS_COLORS


# grep 上色
# if [ "$(uname)" = "Darwin" ]; then
    # [ ! -x "$(command -v ggrep)" ] && echo 'Running linux (BSD) grep: `brew install grep`' && brew install grep
    # alias grep='/usr/local/bin/ggrep --color'
# else
    # alias grep='grep --color'
# fi
alias grep='grep --color'
alias egrep='egrep --color'
alias fgrep='fgrep --color'

# 使得zsh的补全配色与ls一致
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}


# --------------------- 系统设置 -----------------------
# 系统自带的 python2
# alias python2='/usr/bin/python'

if [ "$(uname)" = "Darwin" ]; then
    # 开启sudo执行指纹命令
    sudo-fingerprint() {
        echo '开启指纹授权sudo'
        __check-sudo-fingerprint() {
            cat /etc/pam.d/sudo | grep -vE '^\s*#' | head -n 1| grep -E '^[ ]*auth[ ]+sufficient[ ]+pam_tid.so[ ]*$'
        }
        if [ "$(__check-sudo-fingerprint)" = '' ]; then
            sudo cp /etc/pam.d/sudo /etc/pam.d/sudo.bak
            (
                echo '# "auth sufficient pam_tid.so" 表示允许指纹验证sudo命令\nauth       sufficient     pam_tid.so'
                cat /etc/pam.d/sudo
            ) | sudo tee /etc/pam.d/sudo > /dev/null
            if [ "$(__check-sudo-fingerprint)" != '' ]; then
                echo 'sudo执行指纹命令 开启成功'
            else
                echo 'sudo执行指纹命令 开启识别'
            fi
        else
            echo 'sudo执行指纹命令 已经开启'
        fi
    }
    # 升级mac系统, 会重置/etc/pam.d/sudo, 初次开交互终端需要重新设置
    [[ ! "$(cat /etc/pam.d/sudo)" =~ 'pam_tid.so' ]] && sudo-fingerprint


    fix-etc-zprofile() {
        echo '设置/etc/zprofile, 使得其中的PATH不在~/.zshenv后再次加载'
        [ -f $shareENV/shell_config/etc_zprofile ] && sudo cp $shareENV/shell_config/etc_zprofile /etc/zprofile
    }
    # 升级mac系统, 会重置/etc/zprofile, 初次开交互终端需要重新设置
    [[ ! "$(cat /etc/zprofile)" =~ 'export PATH_SAVE=\$PATH' ]] && fix-etc-zprofile
fi
# -------------------------------------------------------------------------
# 其他

# 没有找到文件（夹），仍然继续执行
# 如 rm -rf 一个文件夹/{*,.*}, 即使没有 .* 文件，也会把 * 文件删了
setopt no_nomatch

# install_shell_integration_and_utilities, 如 imgcat
# `imgcat 图像文件` : 能在iterm2中显示图像
# 首次使用imgcat时iterm会弹出对话框, 大概问是否允许下载文件, 勾选"记住", 点"yes"
if [ ! -x "$(command -v imgcat)" ]; then
# if [ ! -x ${HOME}/.iterm2/imgcat ]; then
    mkdir -p ${shareENV}/shell_config/iterm_bin
    rm ${HOME}/.iterm2 -rf
    ln -s ${shareENV}/shell_config/iterm_bin ${HOME}/.iterm2
    curl -L https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh | bash
fi

# iterm2_shell_integration
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# -------------------------------------------------------------------------
# 自动补全的复用
[ $DotFileDebug -ne 0 ] && echo share .zshrc - reuse completions >&2
# 初始化zsh的自动补全，从而conpdef函数有定义了
autoload -U compinit && compinit

# 复用 rsync 等的补全函数
compdef _rsync autots
compdef _rsync download

tmux_itm() {   :;    }
compdef _tmux tmux_itm
alias itm='tmux_itm -CC attach -t'

tmux_tm() {   :;    }
compdef _tmux tmux_tm
alias tm='tmux_tm attach -t'

# git_gch() {   :;    }
# compdef _git git_gch
# alias gch='git_gch checkout'

ll_list() {   :;   }
la_list() {   :;   }
l_list() {   :;   }
compdef  _ls ll_list
compdef  _ls la_list
compdef  _ls l_list
alias ll='ll_list'
alias la='la_list'
alias l='l_list'

# timezone_ls() { :; }
# compdef _ls timezone_ls
# alias timezone='timezone_ls /usr/share/zoneinfo.default/'

# 允许在有`alias foo=...`时，再定义函数`foo() {  .... }`
set -o ALIAS_FUNC_DEF > /dev/null 2>&1


# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc load local zsh login/logout and local config >&2

# check login shell
if [[ -o login ]]; then
    [ -f "$HOME/.local/etc/login.sh" ] && source "$HOME/.local/etc/login.sh"
    [ -f "$HOME/.local/etc/login.zsh" ] && source "$HOME/.local/etc/login.zsh"
fi

# load local config
[ -f "$HOME/.local/etc/config.zsh" ] && source "$HOME/.local/etc/config.zsh"
[ -f "$HOME/.local/etc/local.zsh" ] && source "$HOME/.local/etc/local.zsh"


[ $DotFileDebug -ne 0 ] && echo share .zshrc end >&2
