import multiprocessing as mp
import sys
import ctypes
import random as rdm

from numpy import nbytes


def qsort_serie_sequentiel_avec_listes(liste, Tableau_trier, bool_trier, lock):
    if bool_trier.value:
        sys.exit(0)

    Pivot = liste[0]
    gche = [X for X in liste[1:] if X <= Pivot]
    drte = [X for X in liste[1:] if X > Pivot]
    if len(gche) == 0:
        bool_trier.value = True

    tableau_fini = gche + [liste[0]] + drte
    lock.acquire()
    # Trier chaque moitié "gauche" et "droite" pour regrouper en plaçant "gche" "Pivot" "drte"
    for i in range(len(Tableau_trier)):
        if Tableau_trier[i] == 0:
            Tableau_trier[i:(i+len(tableau_fini)-1)] = tableau_fini
    lock.release()


if __name__ == '__main__':
    longueur_tableau = 1000
    Tableau = []
    Tableau_trier = mp.Array('i', longueur_tableau)
    bool_trier = mp.Value(ctypes.c_bool, False)
    lock = mp.Lock()

    # creation du tableau a trier
    for i in range(longueur_tableau):
        Tableau.append(rdm.randint(0, 100))

    Nb_process = 8
    processes = [i for i in range(Nb_process)]
    for i in range(Nb_process):
        processes[i] = mp.Process(target=qsort_serie_sequentiel_avec_listes, args=(
            Tableau[i:int((i+1)*longueur_tableau / Nb_process)], Tableau_trier, bool_trier, lock))
        processes[i].start()

    for i in range(Nb_process):
        processes[i].join()

    print(f"Le tableau est trier : {Tableau_trier[:]}")
