import signal
import time
import sys
import os
import multiprocessing as mp


def arreterProgramme():
    """Fonction appelée quand vient l'heure d’arrêter notre programme"""
    print("  C'est l'heure d’arrêt !")
    sys.exit(0)


def F():
    while True:
        time.sleep(1)
        print("boucle du fils")
        signal.signal(signal.SIGINT, arreterProgramme)


if __name__ == "__main__":
    Process = mp.Process(target=F)

    Process.start()

    for i in range(50):
        time.sleep(1)
        print(f"tour n° {i}")
