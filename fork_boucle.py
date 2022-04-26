import os
import sys

for i in range(3):
    pid = os.fork()
    if pid ==0:
        print(i, "je suis ", os.getpid(), ", mon pere est ", os.getppid(), ", retour :", pid)
        sys.exit(0)
