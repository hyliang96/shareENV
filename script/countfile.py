# -*- coding: utf-8 -*-
from __future__ import print_function
# 计算 指定目录下 含有某字符串的 文件/文件夹 的个数
# 或 列出 指定目录下子目录 含有某字符串的 文件/文件夹 的个数


import argparse
import os
from hidden_cmd import hidden_command

parser = argparse.ArgumentParser()
parser.add_argument("path", nargs='?', default='.', help="give one path or default(`.`), e.g. `..`, `../`, `xxx/xxx/`, `xx/xxx`")
parser.add_argument("-l", "--list", action="store_true", help='list out dirs under the path')
parser.add_argument("-r", "--recursive", action="store_true")
parser.add_argument("-a", "--all", action="store_true", help='take hidden dir/files into count')
parser.add_argument("-f", "--format", type=str, default="all", help="`file`, `dir`, RegEx like `.json`")
args = parser.parse_args()


def get_subdir(path):
    all_file_dir_name = os.listdir(path)

    subdir_list = []
    subpath_list = []

    file_list = []

    for name in all_file_dir_name:
        subpath = os.path.join(path,name)
        if os.path.isdir(subpath):
            subdir_list.append(name)
            subpath_list.append(subpath)
        else:
            if args.format in ['all','file']:
                file_list.append(name)
            elif args.format == 'dir':
                pass
            else:
                if args.format in name:
                    file_list.append(name)


    return [subdir_list,subpath_list,file_list]

def count(path):
    command = "ls "+path + " -l "
    if args.recursive:
        command+='-R '
    if args.all:
        command+='-a '

    command+="| grep "

    if args.format=='file':
        command+='"^-"'
    elif args.format=='dir':
        command+='"^d"'
    elif args.format=='all':
        command+='"^[d-]"'
    else:
        command+='"%s"'%args.format

    command+="|wc -l"

    num = int(hidden_command(command).split('\n')[0])
    if args.all and args.format in ['all','dir']:
        num-=2 # 去掉 ls -a 得到的 `.` `..`

    return num

if __name__ == '__main__':
    if args.list:
        subdir_list,subpath_list,file_list = get_subdir(args.path)
        num_list = []
        for subdir, subpath in zip(subdir_list,subpath_list):
            num = count(subpath)
            num_list.append(num)
        subdir_list = [subdir+'/' for subdir in subdir_list]
        subdir_list += ['./-files-']
        num_list += [len(file_list)]

        subdir_list += ['./']
        num_list += [count('./')]

        subdir_num_lsit = sorted(zip(subdir_list,num_list),
            key=lambda subdir_num:subdir_num[1],reverse=True)

        subdir_num_lsit = [[subdir,format(num,',')] for subdir,num in subdir_num_lsit]

        dirlen = max([len(subdir) for subdir,numstr in subdir_num_lsit])
        numlen = max([len(numstr) for subdir,numstr in subdir_num_lsit])

        for subdir, numstr in subdir_num_lsit:
            print( ('%%-%ds'%dirlen) % subdir, ('%%%ds'%numlen) % numstr)
    else:
        print(count(args.path))

