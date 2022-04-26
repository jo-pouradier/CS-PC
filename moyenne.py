from math import fabs
import sys

from numpy import True_


moyenne = 0
test = True
if len(sys.argv[1:]) == 0:
    print("aucune moyenne")

else:
    for arg in sys.argv[1:]:
        if not arg.isdigit():
            print("note non valide")
            test = False
            break
        if (int(arg) < 0) or (int(arg) > 20):
            print("note non valide")
            test = False
            break
        else:
            moyenne += int(arg)
    if test:
        moy = moyenne / len(sys.argv[1:])
        print("moyenne: %.2f" % moy)
