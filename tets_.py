import os, sys

os.execv("/bin/ls", ('ls', '-l'))