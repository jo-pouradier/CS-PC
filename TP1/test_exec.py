import os
import sys
import psutil


commands = [["who", "who"], ["ps", "ps"], ["ls", "ls -l"]]
i=-1
while os.fork()==0 and i <= len(commands)+1:
    i+=1	
    os.execlp(commands[i][0], commands[i][1]) 

#print(psutil.cpu_count())


