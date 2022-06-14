import multiprocessing as mp
import random
import time
import sys
import os
import signal
import random as rand


def Travailleur(k_billes, nbr_billes_disponible, nbr_travailleur, semaphore):
    # Chaque travailleur possede son semaphore
    m = rand.randint(3, 7)
    for k in range(m):
        Demander(k_billes, semaphore, nbr_billes_disponible)
        #fausse tache a effectuer
        time.sleep(0.2*k_billes)
        Rendre(k_billes, nbr_billes_disponible, semaphore)
    print(f"{os.getpid()} a finit")
    with semaphore:
        nbr_travailleur.value -= 1
    sys.exit(0)


def Demander(k_billes, semaphore, nbr_billes_disponible):
    # section critique
    semaphore.acquire()
    while nbr_billes_disponible.value < k_billes:
        semaphore.release()
        time.sleep(0.1) # on laisse du temps pour les autre process
        semaphore.acquire()
        
    nbr_billes_disponible.value -= k_billes
    print(f"{os.getpid()} a reussi a avoir {k_billes} billes")
    semaphore.release()
    # fin de la section critique
        

def Rendre(k_billes, nbr_billes_disponible, semaphore):
    # section critique pour rendre les billes
    with semaphore:
        nbr_billes_disponible.value += k_billes
    print(f"{os.getpid()} a rendu {k_billes}")


def Controlleur(lst_travailleur, nbr_billes_disponible, lock, nbr_travailleur, nbr_max_billes):
    while True:
        #creation du booleen pour savoir si il y a un probleme
        with lock:
            prbl = (nbr_billes_disponible.value < 0 or nbr_billes_disponible.value > nbr_max_billes)
        if not prbl:
            time.sleep(0.2)
            print(f"tt est bon, il a encore {nbr_travailleur.value} trvailleur")
        else:
            # arret si probleme sur le nombre de billes
            print("prbl nbr de billes disponible")
            print("On arrete tout")
            for p in lst_travailleur:
                os.kill(p, 9)
            sys.exit(0)
        # arret du controlleur si il n'y a plus de travailleur
        if nbr_travailleur.value == 0:
            print("Finito Pipo :)")
            sys.exit(0)


def arreterProgramme(signal, frame):
    lst = mp.active_children()
    for p in lst:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, arreterProgramme)


if __name__ == '__main__':
    # Mise en place des billes et de la liste des travailleurs
    nbr_max_billes = 9
    nbr_billes_disponible = mp.Value('i', nbr_max_billes, lock=True)
    nbr_travailleur = mp.Value('i', 4, lock=True)
    lst_travailleur = [0 for i in range(nbr_travailleur.value)]

    # Mise en place du controlleur
    lock = mp.Lock()
    controlleur = mp.Process(target=Controlleur, args=(lst_travailleur, nbr_billes_disponible, lock, nbr_travailleur, nbr_max_billes))
    controlleur.start()

    # Mise en place des process travailleurs
    semaphore = mp.Semaphore()
    for i in range(nbr_travailleur.value):
        nbr_billes_demander = random.randint(3, 8)
        lst_travailleur[i] = mp.Process(target=Travailleur, args=(nbr_billes_demander, nbr_billes_disponible, nbr_travailleur, semaphore))
        lst_travailleur[i].start()

    # attente des Process
    for i in range(nbr_travailleur.value):
        lst_travailleur[i].join()
    controlleur.join()
