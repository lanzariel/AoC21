import sys
path = sys.argv[1]

with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]
    dots = []
    instructions = []
    it = 0
    while lines[it]!='':
        x, y = [int(i) for i in lines[it].split(',')]
        dots.append((x,y))
        it += 1
    it += 1
    for i in range(it, len(lines)):
        instructions.append(lines[i])

class Paper:
    def __init__(self, board):
        self.board = board
    def process_instruction(self, inst):
        what, number = inst.split("=")
        number = int(number)
        if what[-1]=="y":
            self.foldy(number)
        else:
            self.foldx(number)

    def foldy(self, n):
        newboard = []
        for b in self.board:
            if b[1]>n:
                newboard.append((b[0], 2*n-b[1]))
            elif b[1]<n:
                newboard.append(b)
        self.board = newboard

    def foldx(self, n):
        newboard = []
        for b in self.board:
            if b[0]>n:
                newboard.append((2*n - b[0], b[1]))
            elif b[0]<n:
                newboard.append(b)
        self.board = newboard

    def get_visibles(self):
        dots = set(self.board)
        return len(dots)

p = Paper(dots)
p.process_instruction(instructions[0])
print(p.get_visibles())
