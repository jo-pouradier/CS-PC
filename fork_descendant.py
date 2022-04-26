import os, sys, time

N=5
i=0
while os.fork()==0 and i<=N:
    i+=1
    print(i)
    print("je suis ", os.getpid(), " et mon pere est ", os.getppid())
sys.exit(0)