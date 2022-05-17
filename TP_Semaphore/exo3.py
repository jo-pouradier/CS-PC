import multiprocessing as mp


def travailleur(queue_pour_echanger_des_choses):
    
    queue_pour_echanger_des_choses.put([42, None, 'hello']) 
    
    
if __name__ == '__main__':
    Q1 = mp.Queue()
    Q2 = mp.Queue()

    P1 = mp.Process(target=travailleur, args=(Q1,))
    P2 = mp.Process(target=travailleur, args=(Q2,))

    P1.start()
    P2.start() 

    P1.join()
    P2.join()