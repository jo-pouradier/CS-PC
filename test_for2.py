import sys, os

for i in range(4):
    pid = os.fork()
    if pid != 0:
        print("ok")
    print("bonjour")

sys.exit(0)