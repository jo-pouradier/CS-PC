import os
import sys

n=0

for i in range(1,5):
    fils_pid = os.fork() #ce fork peut echouer si on a plus de process diponible
    if fils_pid > 0 : #on est dans le fils (fils_pid est nulle pour le fils)
        os.wait() # ce wait fait  qu'in est deterministe, sans on ne l'est plus
        n = i*2
        break

print("n= ", n)
sys.exit(0)