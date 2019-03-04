# -*- coding: utf-8 -*-
from __future__ import print_function

# 用法：
#   python sizelist.py 一个路径（缺省则为'.')
#   返回该路径及其下各个文件和文件夹的大小，降序排列，按TGMK单位表示


import os, sys
from hidden_cmd import hidden_command

def human_size(num, suffix=''):
    for unit in ['K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def get_subdir(path):
    all_file_dir_name = os.listdir(path)

    name_list = []
    subpath_list = []

    for name in all_file_dir_name:
        subpath = os.path.join(path,name)
        subpath_list.append(subpath)

        if os.path.isdir(subpath):
            name+='/'

        name_list.append(name)

    return [subpath_list,name_list]

def getsize(path):
    command = "du '"+path + "' -d 0"
    size = int( hidden_command(command).split('\t')[0])
    return size

if __name__ == '__main__':
    if len(sys.argv)==1:
        path = '.'
    else:
        path = sys.argv[1]

    if path[-1]!='/':
        path+='/'

    if not os.path.isdir(path):
        print(path,'is not a directory')

    subpath_list,name_list = get_subdir(path)

    size_list = [ getsize(subpath) for subpath in subpath_list ]

    sumsize = getsize(path)

    size_name_list = sorted(zip(size_list,name_list),
            key=lambda size_name:size_name[0],reverse=True)

    size_name_list = [(sumsize,path)]+size_name_list
    hsize_name_list = [(human_size(size),name) for size, name in size_name_list]

    hsizelen = max([len(hsize) for hsize,name in hsize_name_list])
    namelen  = max([len(name)  for hsize,name in hsize_name_list])

    for hsize, name in hsize_name_list:
        print( ('%%%ds'%hsizelen) % hsize ,'  ',('%%-%ds'%namelen) % name)





