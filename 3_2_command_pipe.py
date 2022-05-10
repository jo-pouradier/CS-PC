import multiprocessing as mp
import os ,sys

(dfr,dfw) = mp.Pipe( ) 
pid = os.fork()
if pid!=0:
    print ("[Le processus %d] : ls \n" %os.getpid() )
    dfr.close() # ferme la sortie du tube
    os.dup2(dfw.fileno() , sys.stdout.fileno()) # copie l’entrée du tube vers la sortie standard (écran) dfw.close(dfw) # ferme le descripteur de l’entrée du tube
    os.execlp("cat" , "cat" , "3_.py") # recouvre avec ls
else :
    print ("[Le processus %d] : wc \n" %os.getpid() )
    dfw.close() # ferme l’entrée du tube
    os.dup2(dfr.fileno() , sys.stdin.fileno() ) # copie la sortie du tube vers l’entrée standard (clavier) dfr.close() # ferme le descripteur de la sortie du tube
    os.execlp("wc" , "wc" , "-l") # recouvre avec wc –l
