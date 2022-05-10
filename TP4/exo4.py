import multiprocessing as mp
import os
import time
import signal


def F(s, frame):
    while True:
        time.sleep(1)
        print("boucle du fils")


if __name__ == "__main__":
    Proc = mp.Process(target=F, args=(None, None))
    Proc.start()

    for i in range(5):
        time.sleep(1)
        print(f"tour n° {i}")
        if i == 3:
            print(Proc.pid)
            print("Processus [%d] envoi le signal %d au processus %d" % (
                os.getpid(), signal.SIGKILL, Proc.pid))
            os.kill(Proc.pid, signal.SIGKILL)
