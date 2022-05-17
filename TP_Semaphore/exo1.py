import multiprocessing as mp
import math


def SumImpaire(T, variable_partagee, sem):
    i = 1
    sem.acquire()
    while i <= len(T)-1:
        variable_partagee.value += T[i]
        i += 2
    sem.release()


def SumPaire(T, variable_partagee, sem):
    i = 0
    sem.acquire()
    while i <= len(T)-1:
        variable_partagee.value += T[i]
        i += 2
    sem.release()


if __name__ == '__main__':
    nb = 10001
    T = [i for i in range(nb)]
    variable_partagee = mp.Value('i', 0)
    Sem = mp.Semaphore()
    P1 = mp.Process(target=SumImpaire, args=(T, variable_partagee, Sem))
    P2 = mp.Process(target=SumPaire, args=(T, variable_partagee, Sem))
    P1.start()
    P2.start()
    P1.join()
    P2.join()

    print(f"total {variable_partagee.value}")
    print(f"en fait {sum([i for i in range(nb)])}")
