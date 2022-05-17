import multiprocessing as mp

def incrementer_protection_avec_Sem(variable_partagee, verrou, nbr_iterations):
    with verrou :
        for i in range(nbr_iterations):
            variable_partagee.value += 1
    print(variable_partagee.value)
        


if __name__ == "__main__" :
    nbr_iterations = 5000
    verrou = mp.Semaphore(1) # Val init=1 par défaut
    variable_partagee = mp.Value('i', 0) # ce sera un entier initialisé à 0
    print("la valeur de variable_partagee AVANT les incrémentations : ", variable_partagee.value)

    # On crée 2 process
    pid1 = mp.Process(target=incrementer_protection_avec_Sem, args=(variable_partagee, verrou, nbr_iterations)) 
    pid2 = mp.Process(target=incrementer_protection_avec_Sem, args=(variable_partagee, verrou, nbr_iterations)) 
    pid1.start()
    pid2.start()

    pid1.join() 
    pid2.join()

    print("la valeur de variable_partagee APRES les incrémentations %d (attendu %d) " %(variable_partagee.value, nbr_iterations * 2))