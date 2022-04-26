import os
import sys

N = 5

for n in range(N):
    if os.fork() == 0:
        print("je suis ", os.getpid(), " et mon pere est ", os.getppid())
        sys.exit(0)
