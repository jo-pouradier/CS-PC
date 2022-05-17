import signal
import time
import sys
import os
import multiprocessing as mp


def arreterProgramme(s, frame):
    """Fonction appelée quand vient l'heure d’arrêter notre programme"""
    print("  C'est l'heure d’arrêt !")
    sys.exit(0)


def F(s, frame):
    if s==signal.SIGUSR1:
        print("SIGUSR1 recu")
        while True:
            print("boucle fils")
            time.sleep(0.2)
            if s==signal.SIGUSR2:
                signal.signal(signal.SIGQUIT, arreterProgramme)
        
            

if __name__ == "__main__":
    Process = mp.Process(target=F, args=(None, None))
    Process.start()
    print(Process.pid)

    for i in range(50):
        time.sleep(0.5)
        print(f"tour n° {i}")
        if i == 3:
            os.kill(Process.pid, signal.SIGUSR1)
        if i==5:
            os.kill(Process.pid, signal.SIGUSR2)