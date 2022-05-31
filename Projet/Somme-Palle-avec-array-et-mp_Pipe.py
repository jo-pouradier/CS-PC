# CPE concurrent Python
# Exemple du cours 
# Somme parallèle avec fork d'abord
# Ici  somme avec "array" + Pipe (pas "Array" mais "array" comme dans numpy)
"""
Extrait doc Python sur mp.Pipe() :
Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write 
to the same end of the pipe at the same time. Of course there is no risk of corruption from processes 
using different ends of the pipe at the same time.
"""
import array
import os
import multiprocessing as mp # pour Value, Pipe

# La fonction des fils
def somme(num_process, table, debut, fin_exclue, pour_fils_to_write) :
    #print("Je suis le fils num ", num_process, "et je fais la somme du tableau ", tableau[debut: fin_exclue] )
     
    # On enlève print du tableau, il est trop grand
    print("Je suis le fils num ", num_process, "et je fais la somme du tableau de taille ", int(fin_exclue-debut))
    S_local=0
    for i in range(debut, fin_exclue) :
        S_local += tableau[i]
    
    pour_fils_to_write.send(S_local) # Non bloquant
    print(f"le fils num {num_process}, envoie par send {S_local}")
    
if __name__ == "__main__" :
    taille = 10**6  # nbr d'éléments 
    
    # Plus efficace que les listes
    tableau = array.array('i',[i for i in range(taille)])
    #print(tableau[:]) # Attention : tableau trop grand
    
    pour_pere_to_read, pour_fils_to_write=mp.Pipe()
     
    id_fils1 = mp.Process(target=somme,args=(1, tableau, 0, taille // 2, pour_fils_to_write,))
    id_fils2 = mp.Process(target=somme,args=(2, tableau, taille // 2, taille, pour_fils_to_write,))
    id_fils1.start(); id_fils2.start()

    moitie1=pour_pere_to_read.recv() # Bloquant jsq à ce qu'il y ait qq chose à recevoir
    moitie2=pour_pere_to_read.recv()
    
    # On laisse "join" mais ce sera inutile dans ce cas car "recv()" est bloquant et les fils terminent 
    # avec send (non bloquants)
    id_fils1.join(); id_fils2.join()
    print("La somme totale du tableau obtenue : ", moitie1+moitie2)
    print(f"On vérifie la même somme par Python : {sum(tableau)}")
    assert (moitie1+moitie2 == sum(tableau)), "Il y a eu un Pb. !"

