#!/usr/bin/env bash

# run `openssl rand -base64 24` to get 密码

# then `sudo <path-to-this-script> 用户名 真名 uid 密码`
user_add() {
    username=$1
    realname=$2
    uid=$3
    password=$4
    useradd "$username" -m -c "$realname" -s /usr/bin/zsh -u $uid
    echo "$username:$password" | chpasswd
}


alladduser(){
    username=$1
    realname=$2
    uid=$3
    password=$4
    echo 'sudo password:'
    read -rs sudo_passeord
    echo $sudo_passeord | sudo -S echo 'sudo password correct'
    all 'echo sudo密码 | sudo -S useradd "用户名" -m -c "真名" -s /usr/bin/zsh -u 统一的UID && echo sudo密码 | sudo -S echo "用户名:密码" | chpasswd'

}
# 所有机器上创建新用户
# all 'echo sudo密码 | sudo -S useradd "用户名" -m -c "真名" -s /usr/bin/zsh -u 统一的UID && echo sudo密码 | sudo -S echo "用户名:密码" | chpasswd'


# 一键多个服务器开用户
# ssh c3
# run `openssl rand -base64 24` to get 密码
# sudo adduser test   使用上述生成的密码
# id test
# ANSIBLE_SSH_ARGS="-F $HOME/.ssh/config_JUN1" ansible jungpuall -m user -a 'name=用户名 uid=用户的UID值需要统一制定 password=密码' --sudo --ask-sudo-pass
# jungpuall 指gpu1-gpu24，可以换成其他的，详见/etc/ansible/hosts
