import os,sys

(dfr,dfw) = os.pipe( ) 
(dfr2,dfw2) = os.pipe( )
pid = os.fork()

file_name = "3_.py"

if pid == 0 :
    print ("[Le processus %d] : sort \n" %os.getpid() )
    os.close(dfr)
    os.close(dfw2)
    os.close(dfr2)
    os.dup2(dfw , 1)
    os.close(dfw)
    os.execlp("sort" , "sort",file_name) 
else :
    pid = os.fork()
    if pid == 0 :
        print ("[Le processus %d] : grep \n" %os.getpid() )
        os.close(dfw)
        os.close(dfr2)
        os.dup2(dfr , 0)
        os.dup2(dfw2 , 1)
        os.close(dfw2)
        os.close(dfr)
        os.execlp("grep" , "grep","chaine")
    else :
        print ("[Le processus %d] : tail \n" %os.getpid() )
        os.close(dfw) ; os.close(dfr)
        os.close(dfw2)
        os.dup2(dfr2 ,0 ) 
        os.close(dfr2)
        os.execlp("tail" ,"tail" , "-n" ,"5")
        

