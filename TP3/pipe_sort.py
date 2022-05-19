import multiprocessing as mp
import os
import sys

# changer le nom du fichier a utilier
nom_fichier = "3_.py"
# mot a chercher
mot = "chaine"
# nom du fichier dasn le quel on ecrit
fichier_write = "sortie"

dfr, dfw = os.pipe()
dfr2, dfw2 = os.pipe()

if os.fork() == 0:
    if os.fork() == 0:
        os.close(dfr2)
        os.close(dfw2)
        os.close(dfr)
        os.dup2(dfw, sys.stdout.fileno())
        os.execlp("sort", "sort", nom_fichier)
    else:
        os.close(dfw)
        os.close(dfr2)
        os.dup2(dfw2, sys.stdout.fileno())
        os.dup2(dfr, sys.stdin.fileno())
        os.close(dfw2)
        os.close(dfr)
        os.execlp("grep", "grep", mot)
else:
    df = os.open(fichier_write, os.O_WRONLY | os.O_CREAT, 0o0644)
    os.dup2(df, 1)
    os.close(dfw)
    os.close(dfr)
    os.close(dfw2)
    os.dup2(dfr2, sys.stdin.fileno())
    os.close(dfr2)
    os.execlp("tail", "tail", "-n", "5")
