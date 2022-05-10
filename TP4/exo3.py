import signal
import time


def arreterProgramme(signal, frame):
    global fin
    fin = False


fin = True
signal.signal(signal.SIGINT, arreterProgramme)

print("Le programme va boucler...")

while fin:
    time.sleep(2)
    print("boucler...")
