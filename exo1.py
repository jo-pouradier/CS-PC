import sys 

print ("nom prog: " , sys.argv[0])
print("nbr arg:", len(sys.argv)-1)
print("les arg sont: ")
for arg in sys.argv[1:]:
    print (arg)
    