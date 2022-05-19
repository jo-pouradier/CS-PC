import multiprocessing as mp

def rdv1(cond1, cond2):
    cond1.release()
    cond2.acquire()
    print("rdv1")


def rdv2(cond1, cond2):
    cond2.release()
    cond1.acquire()
    print("rdv2")


if __name__ == "__main__":
    cond1 = mp.Semaphore()
    cond2 = mp.Semaphore()

    P1 = mp.Process(target=rdv1, args=(cond1, cond2))
    P2 = mp.Process(target=rdv2, args=(cond1, cond2))

    P1.start()
    P2.start()

    P1.join()
    P2.join()
