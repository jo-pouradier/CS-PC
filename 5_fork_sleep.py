import os
import sys
import time

N = int(sys.argv[1])

for i in range(N):
    fils_pid = os.fork()
    
    if fils_pid > 0:
        etat = os.wait()
        print(f"mon fils numéro {i} a pour pid: {fils_pid}, etat : {etat}")
        
    else:
        time.sleep(i*2)
        sys.exit(i)
    
    