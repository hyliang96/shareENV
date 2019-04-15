#!/usr/bin/env bash

# run `openssl rand -base64 24` to get 密码

# then `sudo <path-to-this-script> 用户名 真名 uid 密码`
# user_add () {
username=$1
realname=$2
uid=$3
password=$4
useradd "$username" -m -c "$realname" -s /usr/bin/zsh -u $uid
echo "$username:$password" | chpasswd
# }


# 一键多个服务器开用户
# ssh c3
# run `openssl rand -base64 24` to get 密码
# ANSIBLE_SSH_ARGS="-F ~/.ssh/config_JUN1" ansible jungpuall -m user -a 'name=用户名 uid=用户的UID值需要统一制定 password=密码' --sudo --ask-sudo-pass
# jungpuall 指gpu1-gpu24，可以换成其他的，详见/etc/ansible/hosts
