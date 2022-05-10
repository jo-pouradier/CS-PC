import os
import sys
import math

dicoNotes = {"E1": [10, 15, 20], "E2": [12, 16, 15], "E3": [11, 13, 20]}
(dfr, dfw) = os.pipe()
listemoy = []
for i in dicoNotes:
    moy = 0
    if os.fork() == 0:
        for j in dicoNotes[i]:
            moy += j
        moy = math.floor(100*moy/len(dicoNotes[i]))/100
        moy_str = moy.hex().encode()
        length = len(moy_str)
        os.close(dfr)
        os.write(dfw, length.to_bytes(4, byteorder='little', signed=True))
        os.write(dfw, moy_str)
        os.close(dfw)
        break
    else:

        msgReception = os.read(dfr, 4)
        length = int.from_bytes(msgReception, byteorder='little', signed=True)
        msgReception = os.read(dfr, length)
        moy_recu = float.fromhex(msgReception.decode())
        listemoy.append(moy_recu)
        print(listemoy)
max = 0
min = 20
for h in listemoy:
    if h > max:
        max = h
    if h < min:
        min = h

print("max : ", max, "min : ", min)
