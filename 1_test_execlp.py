import os
import sys

if os.fork()==0:
    #os.execlp("python", "python", "miroir.py", "test", "argument")
    os.execlp("ls", "ls -l")
sys.exit(0)
