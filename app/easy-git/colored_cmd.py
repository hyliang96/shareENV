import subprocess
import pty
import os
import sys
# import signal

# cmd = ['ls', '--color=auto', '/']
cmd = ['git', '--no-pager',"log",
# "--graph",
"--abbrev-commit",
"--decorate=no",
r"--date=format:'%Y-%m-%d %H:%I:%S'",
r'''--pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cd %C(bold blue)%an%Creset %C(bold 0)%s%C(reset)' ''',
'--all']

# Ignore SIGTTOU
# signal.signal(signal.SIGTTOU, signal.SIG_IGN)

# def colored_cmd(*cmd):
master, slave = pty.openpty()
# direct stderr also to the pty!
process = subprocess.Popen(
        cmd,
#        [os.getenv('SHELL'), '-i', '-c', cmd],
    stdout=slave,
    stderr=subprocess.STDOUT
)
os.close(slave) # close the slave descriptor! otherwise we will hang forever waiting for input


def read(fd):
    output = b''
    try:
        while True:
            buffer = os.read(fd, 1024)
            if not buffer:
                break
            output += buffer

    # Unfortunately with a pty, an
    # IOError will be thrown at EOF
    # On Python 2, OSError will be thrown instead.
    except (IOError, OSError) as e:
        pass
    return output

output = read(master)

    # Retrieve the terminal
    # os.tcsetpgrp(0,os.getpgrp())

    # return output

# output = colored_cmd("git", "log", "--graph", "--abbrev-commit", "--decorate=no", "--date=format:'%Y-%m-%d %H:%I:%S'", '''--pretty=format:'%C(yellow)%h%Creset%C(auto)%d%Creset %Cgreen%cd %C(bold blue)%an%Creset %C(bold 0)%s%C(reset)' ''')


# _ = os.write(1,output)
print(output.decode('utf-8'))
