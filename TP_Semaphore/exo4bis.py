import multiprocessing as mp
import time

def rdv1(cond1, cond2, cond3):
    time.sleep(2)
    print("P1 pret")
    cond2.release()
    cond3.release()
    cond1.acquire()
    cond1.acquire()
    print("P1 go")


def rdv2(cond1, cond2, cond3):
    time.sleep(1)
    print("P2 pret")
    cond1.release()
    cond3.release()
    cond2.acquire()
    cond2.acquire()
    print("P2 go")


def rdv3(cond1, cond2, cond3):
    time.sleep(0.2)
    print("P3 pret")
    cond2.release()
    cond1.release()
    cond3.acquire()
    cond3.acquire()
    print("P3 go")

def rdvgeneral(sem1, sem2, sem3, n):
    print(f"process {n} pret")
    sem3.release()
    sem2.release()
    sem1.acquire()
    sem1.acquire()
    print(f"process {n} go")

if __name__ == "__main__":
    cond1 = mp.Semaphore(0) #attention a la valeur des jetons presents de base
    cond2 = mp.Semaphore(0)
    cond3 = mp.Semaphore(0)

    # P1 = mp.Process(target=rdv1, args=(cond1, cond2, cond3))
    # P2 = mp.Process(target=rdv2, args=(cond1, cond2, cond3))
    # P3 = mp.Process(target=rdv3, args=(cond1, cond2, cond3))

    P1 = mp.Process(target=rdvgeneral, args=(cond1, cond2, cond3, 1))
    P2 = mp.Process(target=rdvgeneral, args=(cond2, cond1, cond3, 2))
    P3 = mp.Process(target=rdvgeneral, args=(cond3, cond2, cond1, 3))

    P1.start(); P2.start(); P3.start()
    P1.join(); P2.join(); P3.join()