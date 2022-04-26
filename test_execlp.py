import os
import sys

if os.fork()==0:
    os.execlp("python", "python", "miroir.py", "test", "argument")
sys.exit(0)
