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
        export FZF_BASE="$serverENV/app/fzf"
        # export PATH="$PATH:$serverENV/app/fzf/bin"
        if [ ! -x $FZF_BASE/bin/fzf ] 2>&1; then
            git clone --depth 1 https://github.com/junegunn/fzf.git $serverENV/app/fzf
            # $serverENV/app/fzf/install
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
antigen bundle fzf   # 模糊历史搜索

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
antigen bundle z               # 跳转历史目录
# antigen bundle rupa/z z.sh

antigen bundle zdharma/fast-syntax-highlighting
# antigen bundle zsh-users/zsh-syntax-highlighting # zsh 命令的语法高亮
antigen bundle zsh-users/zsh-autosuggestions     # 根据命令开头 补全历史命令,右键使用补全,上下键翻历史
antigen bundle zsh-users/zsh-completions         # tab键自动补全
# antigen bundle supercrabtree/k
antigen bundle Vifon/deer

antigen bundle willghatch/zsh-cdr
# antigen bundle zsh-users/zaw

# 换主题
# 更多主题见：https://github.com/robbyrussell/oh-my-zsh/wiki/themes
# bureau, ys, agnoster, pjanke/agnosterj-zsh-theme
antigen theme hyliang96/my_agnoster # https://github.com/hyliang96/my_agnoster.git
agnoster_time=1
agnoster_env=1
agnoster_newline=1


[ $DotFileDebug -ne 0 ] && echo share .zshrc antigen apply >&2
antigen apply

# -------------------------------------------------------------------------
[ $DotFileDebug -ne 0 ] && echo share .zshrc set syntax highlighting >&2

# syntax color definition
ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)

typeset -A ZSH_HIGHLIGHT_STYLES

ZSH_HIGHLIGHT_STYLES[default]=none
ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=009
ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=red,bold  # =fg=009,standout
ZSH_HIGHLIGHT_STYLES[alias]=fg=cyan,bold
ZSH_HIGHLIGHT_STYLES[builtin]=fg=cyan,bold
ZSH_HIGHLIGHT_STYLES[function]=fg=cyan,bold
ZSH_HIGHLIGHT_STYLES[command]=fg=white,bold
ZSH_HIGHLIGHT_STYLES[precommand]=fg=white,underline
ZSH_HIGHLIGHT_STYLES[commandseparator]=none
ZSH_HIGHLIGHT_STYLES[hashed-command]=fg=009
ZSH_HIGHLIGHT_STYLES[path]=fg=214,underline
ZSH_HIGHLIGHT_STYLES[globbing]=fg=063
ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=white,underline
ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=none
ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=none
ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=none
ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=063
ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=063
ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=009
ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=009
ZSH_HIGHLIGHT_STYLES[assign]=none


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



# 解绑 ctrl+s ctrl+q
stty start undef
stty stop undef
setopt noflowcontrol
# stty -ixon
# stty -ixoff

# bindkey -r '^r'
# bindkey '^f' fzf-history-widget

to-history() { print -S $BUFFER; }
zle -N to-history
# to-history-clear() { print -S $BUFFER ; BUFFER=; }
to-history-clear() { print -S $BUFFER ; BUFFER= }
zle -N to-history-clear
bindkey '^s' to-history      # ctrl+s 保存到命令历史
bindkey 'ç' to-history-clear # alt+c  保存到命令历史, 并清空当前命令

# autoload -Uz history-beginning-search-menu
# zle -N history-beginning-search-menu
# bindkey '^f' history-beginning-search-menu
# bindkey  'ᜅ' history-search-backward
# bindkey  'ᜆ'   history-search-forward

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
alias grep='grep --color'
alias egrep='egrep --color'
alias fgrep='fgrep --color'

# 使得zsh的补全配色与ls一致
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}

# -------------------------------------------------------------------------
# 其他

# 没有找到文件（夹），仍然继续执行
# 如 rm -rf 一个文件夹/{*,.*}, 即使没有 .* 文件，也会把 * 文件删了
setopt no_nomatch

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

tmux_itm() {   :    }
compdef _tmux tmux_itm
alias itm='tmux_itm -CC attach -t'

tmux_tm() {   :    }
compdef _tmux tmux_tm
alias tm='tmux_tm attach -t'

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
