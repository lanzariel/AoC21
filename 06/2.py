import sys
path = sys.argv[1]

with open(path, "r") as f:
    line = f.readline()

vec = [int(i) for i in line.split(",")]

class Bank:
    def __init__(self, v):
        self.state = [0 for i in range(9)]
        for el in v:
            self.state[el]+=1

    def evolve(self):
        new_vec = self.state[1:]
        new_vec.append(self.state[0])
        new_vec[6] += self.state[0]
        self.state = new_vec

    def count(self):
        return sum(self.state)


b = Bank(vec)
for i in range(256):
    b.evolve()

print(b.count())
