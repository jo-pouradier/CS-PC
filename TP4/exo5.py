import multiprocessing as mp
import os, time, signal

def F(rien):
    while True:
        time.sleep(1)
        print("boucle du fils")

def sendSignal(pid, sig) : 
    os.kill(pid,sig)
    print("Processus [%d] envoi le signal %d au processus %d" %(os.getpid(), sig, pid)) 

    

Process = mp.Process(target= F, args =(None,))

Process.start()

for i in range(5):
    time.sleep(1)
    print(f"tour n° {i}")