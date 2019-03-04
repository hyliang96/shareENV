#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
run a line of command and get its return without outputing on displayer
'''
import subprocess
import platform

def ispython2():
    return platform.python_version()[0] <= '2'

def hidden_command(command, code = 'utf-8'):
    # command 可以是unicode 编码，或code 编码


    # command 转为 unicode 编码，type(output)
    #     <type 'unicode'> in python2
    #     <type 'str'>     in python3
    if  ( ispython2() and type(command).__name__ != 'unicode') or \
        ((not ispython2()) and type(command).__name__ != 'str'):
        command = command.decode(code)

    # command += ' 2>&1'
    p = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, close_fds=True)

    output_byte_line_list = p.stdout.readlines()

    # print(type(output_byte_line_list[0]))
    #     <type 'str'>      in python2
    #     <type 'bytes'>    in python3

    output = ''.join([
            line.decode(code) if not ispython2() else line
            for line in output_byte_line_list
        ])

    # output 用 unicode 编码，type(output)
    #     <type 'unciode'>      in python2
    #     <type 'str'>    in python2
    if len(output)>0 and output[-1]=='\n':
        output = output[:-1]

    return output

    # output 在python2、3 中 都是 str

# if __name__ == '__main__':
#     print(hidden_command('echo asdas萨达'))
