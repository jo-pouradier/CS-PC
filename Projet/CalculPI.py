import multiprocessing as mp
import os
import sys
import time
import random
import math


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

    Nb_process = 6
    Process = [i for i in range(Nb_process)]
    Pipe_PI_receive, Pipe_PI_send= mp.Pipe()

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
        estimation_pi_multiP += Pipe_PI_receive.recv()/N*Nb_process

    print(f"estimation de pi en mono process : PI = {estimation_pi_multiP}")
    print(
        f"Durée du calcul mono Process : {math.floor(10000*(endP-startP))/10000} s")
