import multiprocessing as mp
import random
from re import I


def generationN(N, send_NPaire, send_NImpaire):
    Paire = []
    Impaire = []
    for i in range(N):
        x = random.randrange(0, 5000, 1)
        if x % 2 == 0:
            Paire.append(x)
        else:
            Impaire.append(x)
    send_NPaire.send(Paire)
    send_NImpaire.send(Impaire)


def FiltrePaire(receive_NPaire, send_somme_paire):
    Paire = receive_NPaire.recv()
    send_somme_paire.send(sum(Paire))
    print(f"somme paire = {sum(Paire)}")


def FiltreImpaire(receive_NImpaire, send_somme_impaire):
    Impaire = receive_NImpaire.recv()
    send_somme_impaire.send(sum(Impaire))
    print(f"somme paire = {sum(Impaire)}")


if __name__ == "__main__":
    N = 500
    receive_NPaire, send_NPaire = mp.Pipe()
    receive_NImpaire, send_NImpaire = mp.Pipe()
    receive_somme_paire, send_somme_paire = mp.Pipe()
    receive_somme_impaire, send_somme_impaire = mp.Pipe()
    generator = mp.Process(target=generationN, args=(
        N, send_NPaire, send_NImpaire))
    filtr_paire = mp.Process(target=FiltrePaire, args=(
        receive_NPaire, send_somme_paire))
    filtr_impaire = mp.Process(target=FiltreImpaire, args=(
        receive_NImpaire, send_somme_impaire))

    generator.start()
    filtr_paire.start()
    filtr_impaire.start()

    generator.join()
    filtr_impaire.join()
    filtr_paire.join()

    Paire = receive_somme_paire.recv()
    Impaire = receive_somme_impaire.recv()

    print(f"somme total: {Paire+Impaire}")
