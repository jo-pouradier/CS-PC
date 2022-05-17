import multiprocessing as mp
import random


def travailleur(queue):
    for i in range(50):
        a = random.randint(0, 100)
        queue.put(a)


def consommateur(queue, lock):
    S = 0
    with lock:
        while not queue.empty():
            S += queue.get()
    queue.put(S)


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
    P1.join()
    P2.join()

    C1.start()
    C2.start()
    C1.join()
    C2.join()

    print(Q1.get(), Q2.get())