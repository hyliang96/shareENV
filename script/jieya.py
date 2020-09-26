#! /usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os


Tools = {
    #格式   解压命令 解压路径标记 是否自动创建同名文件夹
    'tar':["tar xvf",  "-C", True],
    'gz': ["tar zxvf", "-C", True],
    'tgz':["tar zxvf", "-C", True],
    'bz2':["tar jxvf", "-C", True],
    'zip':["unzip",    "-d", False]
}
Suffix = list(Tools.keys())

def Usage():
    print("python3 jieya.py 压缩文件的路径（可以有多个） 解压到的路径（缺省则为./）")
    print("支持",*Suffix)

def decompress(parsedfile,jieya_path):
    print(parsedfile)
    [file, main, suffix] = parsedfile
    try:
        tool,argv,auto_newdir = Tools[suffix]
        jieya_path_ = jieya_path + ("" if auto_newdir else "/"+main)
        os.system(" ".join([tool,file,argv,jieya_path_]))
    except KeyError:
        print(file,"can't be decompressed.")
        print(suffix,"is not supported in", *Suffix)

def depart(s,sep):
    parts = s.split(sep)
    return [sep.join(parts[:-1]), parts[-1]]

def files_parse(files):
    for file in files:
        if not os.path.isfile(file):
            print(file,"doesn't exist")
            sys.exit(1)

    ParsedFiles = []
    for file in files:
        path, name = depart(file,"/")
        main, suffix = depart(name,".")
        ParsedFiles.append([file, main, suffix])
        if not suffix in Suffix:
            print(file,"can't be decompressed.")
            print(suffix,"is not supported in", *Suffix)
            sys.exit(1)

    return ParsedFiles

if __name__ == '__main__':
    if len(sys.argv)==1 or \
        sys.argv[1] in ["-h",'--h','-help','--help']:
        Usage()
        sys.exit(1)

    if os.path.isdir(sys.argv[-1]):
        jieya_path = sys.argv[-1]
        files = sys.argv[1:-1]
    else:
        files = sys.argv[1:]
        jieya_path = "."

    ParsedFiles = files_parse(files)

    for parsedfile in ParsedFiles:
        decompress(parsedfile,jieya_path)
    