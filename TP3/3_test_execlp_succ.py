import os,sys

if os.fork() == 0 :
    os.execlp('who','who')
if os.fork() == 0 :
    os.execlp('ps','ps')
os.execlp('ls','-l')