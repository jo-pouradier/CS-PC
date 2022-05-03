import os
import sys


i = -1

commands = [["who", "who"],
["ps", "ps"], ["ls", "ls -l"]]


for i in range(len(commands)):
    pid = os.fork()
    if pid == 0:
        os.execlp(commands[i][0], commands[i][1])

sys.exit(0)

