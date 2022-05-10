import signal
import sys


def arreterProgramme(signal, frame):
    """Fonction appelée quand vient l'heure d’arrêter notre programme"""
    print("  C'est l'heure d’arrêt !")
    sys.exit(0)


# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, arreterProgramme)
# Notre programme...
print("Le programme va boucler...")

while True:
    continue
