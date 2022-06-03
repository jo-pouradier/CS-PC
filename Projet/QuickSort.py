import multiprocessing as mp
import sys
import ctypes
import random as rdm
import array


def qsort_serie_parrallel_avec_listes(liste, lock, Nb_process):
    if len(liste) < 2:
        return liste
    # Pivot = liste[0]
    gche = [X for X in liste[1:] if X <= liste[0]]
    drte = [X for X in liste[1:] if X > liste[0]]
    # Trier chaque moitié "gauche" et "droite" pour regrouper en plaçant "gche" "Pivot" "drte"
    if Nb_process.value <= 8:
        tab = qsort_serie_sequentiel_avec_listes(
            gche) + [liste[0]] + qsort_serie_sequentiel_avec_listes(drte)
    else:
        p1 = mp.Process(target=qsort_serie_sequentiel_avec_listes,
                        args=(gche+liste[0], lock))
        p2 = mp.Process(target=qsort_serie_sequentiel_avec_listes,
                        args=(drte, lock))
        p1.start()
        p2.start()

        p1.join()
        p2.join()
    

def qsort_serie_sequentiel_avec_listes(liste):
    if len(liste) < 2:
        return liste
    # Pivot = liste[0]
    gche = [X for X in liste[1:] if X <= liste[0]]
    drte = [X for X in liste[1:] if X > liste[0]]
    # Trier chaque moitié "gauche" et "droite" pour regrouper en plaçant "gche" "Pivot" "drte"
    return qsort_serie_sequentiel_avec_listes(gche) + [liste[0]] + qsort_serie_sequentiel_avec_listes(drte)


if __name__ == '__main__':
    longueur_tableau = 1000
    Tableau_desordre = []
    # liste qui va recevoir les bouts de tableau trier:
    Tableau_trier = array.array('i', [])
    Nb_process = mp.Value('i', 0)
    lock = mp.Lock()
    # creation du tableau a trier:
    for i in range(longueur_tableau):
        Tableau_desordre.append(rdm.randint(0, 100))
    print(f"Notre tableau de d'épart: {Tableau_desordre}")
    qsort_serie_parrallel_avec_listes(Tableau_desordre, lock, Nb_process)
    # on a un compteur de process partagée qui ne peut pas dépaser 8
    # si on a moin de 8 process, on en fait qui ont pour fonction qsort et une partie du tableau
    # fonctionnement comme les racines d'un arbre
