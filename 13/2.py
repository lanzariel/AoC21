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
            if b[1]>=n:
                newboard.append((b[0], 2*n-b[1]))
            elif b[1]<n:
                newboard.append(b)
        self.board = newboard

    def foldx(self, n):
        newboard = []
        for b in self.board:
            if b[0]>=n:
                newboard.append((2*n - b[0], b[1]))
            elif b[0]<n:
                newboard.append(b)
        self.board = newboard

    def get_visibles(self):
        dots = set(self.board)
        return len(dots)

    def print(self):
        x_max = 0
        y_max = 0
        for b in self.board:
            x_max = max(x_max, b[0])
            y_max = max(y_max, b[1])
        lans = []
        for y in range(y_max+1):
            lrow = []
            for x in range(x_max+1):
                if (x,y) in self.board:
                    lrow.append("#")
                else:
                    lrow.append(".")
            row = "".join(lrow)
            lans.append(row)
        ans = "\n".join(lans)
        print(ans)


p = Paper(dots)
for i in instructions:
    p.process_instruction(i)
p.print()
