import multiprocessing as mp
import random as rand
import sys
import time
import os
import signal
# Quelques codes d'echappement (tous ne sont pas utilises)
CLEARSCR = "\x1B[2J\x1B[;H"  # Clear SCreen
CLEAREOS = "\x1B[J"  # Clear End Of Screen
CLEARELN = "\x1B[2K"  # Clear Entire LiNe
CLEARCUP = "\x1B[1J"  # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH"  # ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"  # effacer apres la position du curseur
CRLF = "\r\n"  # Retour a la ligne

# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h"  # Curseur visible
CURSOFF = "\x1B[?25l"  # Curseur invisible

# Actions sur les caracteres affichables
NORMAL = "\x1B[0m"  # Normal
BOLD = "\x1B[1m"  # Gras
UNDERLINE = "\x1B[4m"  # Souligne


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK = "\033[22;30m"  # Noir. NE PAS UTILISER. On verra rien !!
CL_RED = "\033[22;31m"  # Rouge
CL_GREEN = "\033[22;32m"  # Vert
CL_BROWN = "\033[22;33m"  # Brun
CL_BLUE = "\033[22;34m"  # Bleu
CL_MAGENTA = "\033[22;35m"  # Magenta
CL_CYAN = "\033[22;36m"  # Cyan
CL_GRAY = "\033[22;37m"  # Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY = "\033[01;30m"  # Gris fonce
CL_LIGHTRED = "\033[01;31m"  # Rouge clair
CL_LIGHTGREEN = "\033[01;32m"  # Vert clair
CL_YELLOW = "\033[01;33m"  # Jaune
CL_LIGHTBLU = "\033[01;34m"  # Bleu clair
CL_LIGHTMAGENTA = "\033[01;35m"  # Magenta clair
CL_LIGHTCYAN = "\033[01;36m"  # Cyan clair
CL_WHITE = "\033[01;37m"  # Blanc
# -------------------------------------------------------

# Definition de qq fonctions de gestion de l'ecran


def effacer_ecran(): print(CLEARSCR, end='')
def erase_line_from_beg_to_curs(): print("\033[1K", end='')
def curseur_invisible(): print(CURSOFF, end='')
def curseur_visible(): print(CURSON, end='')
def move_to(lig, col): print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def en_couleur(Coul): print(Coul, end='')
def en_rouge(): print(CL_RED, end='')  # Un exemple !


def next_generation(LIGNES, COLONNES, GRID, s_grid):
    while True:
        # on passe a travers toutes les cases de la grid
        for l in range(LIGNES):
            for c in range(COLONNES):
                # on cherche le nombre de voisins vivant
                voisin_vivant = get_neighbours(l, c, LIGNES, COLONNES, GRID)
                # for i in range(-1, 2):
                #     for j in range(-1, 2):
                #         if ((l+i >= 0 and l+i < LIGNES) and (c+j >= 0 and c+j < COLONNES)):
                #             voisin_vivant += GRID[l + i][c + j]

                voisin_vivant -= GRID[l][c]

                if GRID[l][c] == 1 and (voisin_vivant < 2 or voisin_vivant > 3):
                    GRID[l][c] = 0
                if GRID[l][c] == 0 and voisin_vivant == 3:
                    GRID[l][c] = 1
        s_grid.send(GRID)


def get_neighbours(x, y, LIGNES, COLONNES, GRID):
    total = 0
    for n in range(-1, 2):
        for m in range(-1, 2):
            x_edge = (x+n+LIGNES) % LIGNES
            y_edge = (y+m+COLONNES) % COLONNES
            total += GRID[x_edge][y_edge]
    total -= GRID[x][y]
    return total


def areSame(A, B):
    for i in range(len(A)):
        for j in range(len(A[0])):
            if (A[i][j] != B[i][j]):
                return False
    return True


def display(GRID, LIGNES, COLONNES, r_grid, process, bool_rejouer):
    # Attention a la copie de la matrice
    GRID_before = [row[:] for row in GRID]
    gen_numb = 0

    while True:
        effacer_ecran()
        for p in range(COLONNES):
            for j in range(LIGNES):
                if GRID[p][j] == 1:
                    GRID[p][j] = '@'
                else:
                    GRID[p][j] = ' '

        for i in range(len(GRID)):
            move_to(i+5, 0)
            print(' '.join(GRID[i]))

        gen_numb += 1
        move_to(len(GRID)+7, 0)
        print(f"Génération n°{gen_numb}")
        # arret si pas de changemeent dans la grille
        test = areSame(GRID, GRID_before)
        if test:
            FinProgram(process, LIGNES, bool_rejouer)

        GRID_before[:] = GRID[:]
        GRID = r_grid.recv()
        time.sleep(0.03)


def FinProgram(process, LIGNES, bool_rejouer):
    move_to(LIGNES+8, 0)
    en_rouge()
    print("Pas de nouvelle generation")
    print("Fin de la generation")
    print("<CTRL + Z> pour rejouer")
    en_couleur(CL_WHITE)
    print("Le programme va s'arreter dans 5 secondes")
    os.kill(process, signal.SIGKILL)
    time.sleep(5)
    bool_rejouer.value = 0
    sys.exit(0)


# on arrete tout proprement
def arretForcerProgramme(signal, frame):
    bool_rejouer.value = 0
    lst = mp.active_children()
    for p in lst:
        p.kill()


def Rejouer(signal, frame):
    bool_rejouer.value = 1
    lst = mp.active_children()
    for p in lst:
        p.terminate()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, arretForcerProgramme)
    signal.signal(signal.SIGTSTP, Rejouer)

    en_couleur(CL_WHITE)
    LIGNES = 60
    COLONNES = 80
    GRID = [[rand.randint(0, 1) for i in range(COLONNES)]
            for j in range(LIGNES)]

    gen_numb = 0
    bool_rejouer = mp.Value('i', 0)
    r_grid, s_grid = mp.Pipe()

    next_gen = mp.Process(target=next_generation,
                          args=(LIGNES, COLONNES, GRID, s_grid))
    next_gen.start()
    disp = mp.Process(target=display, args=(
        GRID, COLONNES, LIGNES, r_grid, next_gen.pid, bool_rejouer))
    disp.start()

    next_gen.join()
    disp.join()

    if bool_rejouer.value:
        os.execl(sys.executable, sys.executable, * sys.argv)

    # ne pas oublier de close les deux semaphores
    r_grid.close()
    s_grid.close()
    sys.exit(0)
