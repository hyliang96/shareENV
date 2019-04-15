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
