import multiprocessing as mp

def rdv1 (cond):
    with cond:
        cond.wait()
        print("rdv1")

def rdv2 (cond):
    with cond:
        cond.wait()
        print("rdv2")


if __name__ == "__main__":
    cond = mp.Condition()


    P1 = mp.Process(target = rdv1, args = (cond,))
    P2 = mp.Process(target = rdv2, args = (cond,))

    cond.notify_all()

    P1.join()
    P2.join()
