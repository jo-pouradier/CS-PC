import time
import os
import sys
import random
import multiprocessing as mp
import signal



def fils_calculette(commande, stockage):
    print("Bonjour du Fils calculateurs", os.getpid())
    while True:
        # reception d'une commande
        calcul = commande.get()
        id = calcul[0]
        cmd = calcul[1]
        res = eval(cmd)
        stockage.put([id, res])
        time.sleep(1)


def fils_demand(commands, stockage, lock):
    id = os.getpid()
    print('bonjour du fils demandeur', id)
    while True:
        # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
        opd1 = random.randint(1, 100)
        opd2 = random.randint(1, 100)
        operateur = random.choice(['+', '-', '*', '/', '**'])
        str_commande = f"{opd1} {operateur} {opd2}"
        #envoie du calcul aléatoire dans la Queue "commands"
        commands.put([id, str_commande])
        print(f"Le Pere {id} va demander à faire : ", str_commande)
        # attente du calcul
        lock.acquire()
        bool_getcalcul = True
        while bool_getcalcul:
            calcul = stockage.get()
            # vérification de l'id pour attendre le bon calcul
            if calcul[0] == id:
                res = calcul[1]
                bool_getcalcul = False
            else:
                stockage.put(calcul)
        lock.release()
        print(f"Le Pere {id} a recu ", res)
        print('-' * 60)
        #création d'un calcul après une seconde
        time.sleep(1)


def arreterProgramme(signal, frame):
    lst = mp.active_children()
    for p in lst:
        p.terminate()

signal.signal(signal.SIGINT, arreterProgramme)

if __name__ == "__main__":
    # Mise en place des variables utiles
    stockage = mp.Queue()
    commands = mp.Queue()
    nbr_demandeurs = 4
    lst_demandeurs = [0 for i in range(nbr_demandeurs)]
    nbr_calculateurs = 4
    lst_calculateurs = [0 for i in range(nbr_demandeurs)]

    # Création des Process Calculateurs
    lock = mp.Semaphore()
    for i in range(nbr_calculateurs):
        lst_calculateurs[i] = mp.Process(
            target=fils_calculette, args=(commands, stockage))
        lst_calculateurs[i].start()

    #Création des Process demandeurs
    for i in range(nbr_demandeurs):
        lst_demandeurs[i] = mp.Process(
            target=fils_demand, args=(commands, stockage, lock))
        lst_demandeurs[i].start()

    # Attente des Process
    for i in range(nbr_calculateurs):
        lst_calculateurs[i].join()
    for i in range(nbr_demandeurs):
        lst_demandeurs[i].join()
