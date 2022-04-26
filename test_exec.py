import os
import sys

case = 1
i = -1

commands = [["/bin/ps", ("ps",)], ["/bin/ls", ('ls', '-l')]]

if case == 1:
    while os.fork() == 0 and i <= len(commands):
        i += 1
        print(i)
        os.execv(commands[i][0], commands[i][1])
    os.wait()
    sys.exit(0)
