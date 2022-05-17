import multiprocessing as mp
import math


def SumImpaire(T, send):
    S = []
    i = 1
    while i <= len(T)-1:
        S.append(T[i])
        i += 2
    send.send(sum(S))


def SumPaire(T, send):
    S = []
    i = 0
    while i <= len(T)-1:
        S.append(T[i])
        i += 2
    send.send(sum(S))


if __name__ == '__main__':
    T = [i for i in range(103)]
    send, receive = mp.Pipe()
    P1 = mp.Process(target=SumImpaire, args=(T, send))
    P2 = mp.Process(target=SumPaire, args=(T, send))
    P1.start()
    P2.start()

    partP = receive.recv()
    partI = receive.recv()

    print(f"partie paire {partP}, partie impaire {partI}, total {partP+partI}")
    print(f"en fait {sum([i for i in range(103)])}")
