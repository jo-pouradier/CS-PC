import multiprocessing as mp
import random
import time
import sys
import os
import signal
import random as rand


def Travailleur(k_billes, nbr_billes_disponible, nbr_travailleur):
    # Chaque travailleur possede son semaphore
    semaphore = mp.Semaphore()
    m = rand.randint(3, 7)
    for k in range(m):
        Demander(k_billes, semaphore, nbr_billes_disponible)
        #fausse tache a effectuer
        time.sleep(0.2*k_billes)
        Rendre(k_billes, nbr_billes_disponible, semaphore)
    print(f"{os.getpid()} a finit")
    with nbr_travailleur:
        nbr_travailleur.value -= 1
    sys.exit(0)


def Demander(k_billes, semaphore, nbr_billes_disponible):
    # section critique
    semaphore.acquire()
    while nbr_billes_disponible.value < k_billes:
        semaphore.release()
        semaphore.acquire()
    semaphore.release()
    # fin de la section critique
    print(f"{os.getpid()} a reussi a avoir {k_billes} billes")
    nbr_billes_disponible.value -= k_billes


def Rendre(k_billes, nbr_billes_disponible, semaphore):
    with semaphore:
        nbr_billes_disponible.value += k_billes
    print(f"{os.getpid()} a rendu {k_billes}")


def Controlleur(lst_travailleur, nbr_billes_disponible, lock, nbr_travailleur, nbr_max_billes):
    while True:
        with lock:
            prbl = (nbr_billes_disponible.value < 0 and nbr_billes_disponible.value > nbr_max_billes)
        if not prbl:
            time.sleep(1)
            print("tt est bon")
        else:
            # arret si probleme sur le nombre de billes
            print("prbl nbr de billes disponible")
            print("On arrete tout")
            for p in lst_travailleur:
                p.terminate()
            sys.exit(0)
        if nbr_travailleur.value == 0:
            print("tout est finie")
            sys.exit(0)


def arreterProgramme(signal, frame):
    lst = mp.active_children()
    for p in lst:
        p.terminate()

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
    for i in range(nbr_travailleur.value):
        nbr_billes_demander = random.randint(3, 8)
        lst_travailleur[i] = mp.Process(target=Travailleur, args=(nbr_billes_demander, nbr_billes_disponible, nbr_travailleur))
        lst_travailleur[i].start()

    # attente des Process
    for i in range(nbr_travailleur.value):
        lst_travailleur[i].join()
    controlleur.join()
