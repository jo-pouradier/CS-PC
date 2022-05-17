import multiprocessing as mp
import random


def travailleur(queue, lock):
    for i in range(50):
        a = random.randint(0, 100)
        queue.put(a)


def consommateur(queue, lock):
    S = 0
    with lock:
        S += queue.get()


if __name__ == '__main__':
    Q1 = mp.Queue()
    Q2 = mp.Queue()

    lock = mp.Semaphore()

    P1 = mp.Process(target=travailleur, args=(Q1,))
    P2 = mp.Process(target=travailleur, args=(Q2,))
    C1 = mp.Process(target=consommateur, args=(Q1, lock))
    C2 = mp.Process(target=consommateur, args=(Q2, lock))

    P1.start()
    P2.start()
    C1.start()
    C2.start()

    while not Q1.empty() or not Q2.empty():
        C1.start()
        

    P1.join()
    P2.join()
    C1.join()
    C2.join()
