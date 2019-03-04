#!/usr/bin/env python2.7
#coding: utf-8

# 修改expect，
# * 能够实时输出终端显示的东西
# * 实时改变child窗口大小，使它和终端窗口等大

import pexpect
import struct, fcntl, termios, signal, sys

# * 能够实时输出终端显示的东西
def spawn(*argv,**argv_dict):
    # interact前输出child的输出
    child = pexpect.spawn(*argv,**argv_dict)
    child.logfile_read = sys.stdout.buffer
    return child

# * 实时改变child窗口大小，使它和终端窗口等大
# 参考 http://blog.51cto.com/smileyouth/1869482
def make_a_sigwinch_passthrough(child):
    def sigwinch_passthrough(sig, data):
    # 监听窗口变化
        winsize = getwinsize()
        child.setwinsize(winsize[0],winsize[1])
    return sigwinch_passthrough

def getwinsize():
    # 获取窗口大小
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912 # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

def interact(child):
    # interact后不再输出child的输出，不然会双重输出
    child.logfile_read = None

    # 调整child窗口大小到填满终端窗口大小
    # 若端窗口大小变化，动态更新child窗口大小
    sigwinch_passthrough = make_a_sigwinch_passthrough(child)
    signal.signal(signal.SIGWINCH, sigwinch_passthrough) # 监听窗口变化

    winsize = getwinsize();
    child.setwinsize(winsize[0], winsize[1]) 
    # 设置窗口大小, 这句命令必需在.interact()之前执行，不然无效
    child.interact()
