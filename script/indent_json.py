# -*- coding: utf-8 -*-

import json
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='rewrite .josn file(s) with indent')
parser.add_argument('jsonfiles', nargs='+', help='exact json files, or `<path>/*.json`')
parser.add_argument('-i','--indent', default=4, type=int,help='how many spaces for an indent')
parser.add_argument('-c','--check', action="store_true" ,help='just check if .json can be loaded, do not rewrite')

args = parser.parse_args()


def space_zhuanyi(string):
    return string.replace(' ', '\ ')

def getpath_and_file(file):
    path = '/'.join(file.split('/')[:-1])
    file = file.split('/')[-1]
    if path == '':
        path = '.'
    return [path,file]

def rewrite_indent(filepath,indent):
    if not args.check:
        path, file = getpath_and_file(filepath)
        backup = path+'/backup_'+file
        command = 'cp'+' '+space_zhuanyi(filepath)+' '+space_zhuanyi(backup)
        os.system(command)

    with open(filepath, "r") as f:
        try:
            dic = json.load(f)
        except:
            print(filepath, "can't be loaded, please check if it is a .json and in correct grammar.")

    if not args.check:
        with open(filepath, "w") as f:
            json.dump(dic,f,indent=indent)

        command = 'rm'+' '+space_zhuanyi(backup)
        os.system(command)


if __name__ == '__main__':

    for filepath in args.jsonfiles:
        if not os.path.exists(filepath):
            print(filepath, "doesn't exist")
            sys.exit(1)

    for filepath in args.jsonfiles:
        rewrite_indent(filepath,args.indent)
