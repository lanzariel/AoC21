import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

class Die:
    def __init__(self):
        self.value = 0
        self.thrown = 0
    def throw(self):
        self.value = self.value % 100
        self.value += 1
        self.thrown += 1
        return self.value

class Game:
    def __init__(self, ln):
        get_start = lambda x : int(x.split(": ")[1])
        self.positions = [get_start(i) for i in ln]
        self.scores = [0 for i in ln]
        self.turn = 0
        self.d = Die()
    
    def step(self):
        result = 0
        for i in range(3):
            result += self.d.throw()
        self.positions[self.turn] += result
        self.positions[self.turn] = ((self.positions[self.turn]-1) % 10) + 1
        self.scores[self.turn] += self.positions[self.turn]
        self.turn += 1
        self.turn = self.turn % 2
    
    def play(self):
        while self.scores[0] < 1000 and self.scores[1] < 1000:
            self.step()
        return self.d.thrown * self.scores[self.turn]

g = Game(lines)
print(g.play())

    