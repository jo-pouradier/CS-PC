import signal,time,sys,os
import multiprocessing as mp

def fin(je, frame): 
    print("RIP\ndommage")
    sys.exit(0)

def test():
    nb = input("entrez un entier : ")

    try:
        t=int(nb)
        print("cool")
    except :
        print("essaie encore")

        test()

if __name__ == "__main__":
    signal.alarm(5)
    signal.signal(signal.SIGALRM,fin)
    test()
    sys.exit(0)