import sys
import numpy as np

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

i1 = [1, 0, 0]
i2 = [0, 1, 0]
i3 = [0, 0, 1]

positive_t = [[i1,i2,i3], [i1,i3,i2], [i2,i1,i3],[i2,i3,i1],[i3,i1,i2],[i3,i2,i1]]
id = np.identity(3,dtype=int)
print(id)
for i in range(8):
    print(i&4, i&2, i&1)
print(transforms)
print(len(transforms))


class Scanner:
    def __init__(self, number):
        self.number = number
        self.beacons = set()

    def add_b(self, b):
        self.beacons.add(b)

    def add_b_from_str(self, b_str):
        x,y,z = [int(i) for i in b_str.split(",")]
        self.add_b((x,y,z))

    def n_of_b(self):
        return len(self.beacons)

sc_list = []

it = 0
while it < len(lines):
    if lines[it]=="":
        it += 1
    if lines[it][0:2]=="--":
        current_scanner = Scanner(len(sc_list))
        sc_list.append(current_scanner)
    else:
        current_scanner.add_b_from_str(lines[it])
    it += 1

print([i.n_of_b() for i in sc_list])