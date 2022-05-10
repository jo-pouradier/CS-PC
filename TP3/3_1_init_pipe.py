import multiprocessing as mp


def print_truc(send):
    send.send([42, None, 'hello'])
    send.close()
    

if __name__=='__main__':
    send, receive = mp.Pipe()

    fils = mp.Process(target=print_truc, args=(send,))
    fils.start()
    fils.join()

    truc_pipe = receive.recv()
    receive.close()
    print(truc_pipe)

