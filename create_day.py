import sys
import os 
import requests
n = str(int(sys.argv[1]))

n = n.zfill(2)
try:
    os.mkdir(n)
    paht = n + "/"
except:
    print("Already Existing Directory. Bye")
    exit()
with open(paht+"1.py", "w") as f:
    f.write("import sys\n")
    f.write("\n")
    f.write("path = sys.argv[1]\n")
    f.write("with open(path, 'r') as f:\n")
    f.write("    lines = [i.strip() for i in f.readlines()]\n")
    f.write("\n")