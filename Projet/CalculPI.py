import multiprocessing as mp
import os
import sys
import time
import random
import math
from matplotlib import pyplot as plt


def CalculSequentiel(N: int):
    count = 0
    for i in range(int(N)):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1:
            count += 1
    return count


def CalculParallel(N: int, Pipe_PI):
    count = 0
    for i in range(int(N)):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1:
            count += 1
    Pipe_PI.send(count)


if __name__ == '__main__':
    N = 1e6
    start = time.time()
    estimation_pi_monoP = CalculSequentiel(N)*4/N
    end = time.time()
    print(f"estimation de pi en mono process : PI = {estimation_pi_monoP}")
    print(
        f"Durée du calcul mono Process : {math.floor(10000*(end-start))/10000} s")

    temps_calcul_multi = []
    approximation = 0
    nbr_iterations = 10
    for o in range(nbr_iterations):
        Nb_process = 2
        Process = [i for i in range(Nb_process)]
        Pipe_PI_receive, Pipe_PI_send = mp.Pipe()

        startP = time.time()
        for i in range(Nb_process):
            Process[i] = mp.Process(target=CalculParallel,
                                    args=(N/Nb_process, Pipe_PI_send))
            Process[i].start()
        for i in range(Nb_process):
            Process[i].join()
        endP = time.time()

        estimation_pi_multiP = 0
        for i in range(Nb_process):
            estimation_pi_multiP += Pipe_PI_receive.recv()/N * 4

        print(f"test num {o}")
        print(
            f"estimation de pi en multi Process : PI = {estimation_pi_multiP}")
        print(
            f"Durée du calcul multi Process : {math.floor(10000*(endP-startP))/10000} s\n")
        temps_calcul_multi.append(math.floor(10000*(endP-startP))/10000)
        approximation += estimation_pi_multiP

    plt.plot([i for i in range(10)], temps_calcul_multi)
    plt.xlabel("nbr de process")
    plt.ylabel("temps de calcul")
    plt.title(
        f"Temps de calcul d'une approximation de PI : {approximation/nbr_iterations}\navec {N} iterations")
    plt.show()
