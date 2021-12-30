import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]


#Virtual Class,
# stepper needs to be defined
class Cucumber:
    def __init__(self,board,row,col):
        self.pos = [row,col]
        self.board = board
    
    def prepare(self):
        self.next_pos = self.board.next_el(self.pos, self.stepper)
        self.is_movable = self.board.is_free(self.next_pos)
    
    def move(self):
        if self.is_movable:
            self.board.swap(self.pos, self.next_pos)
            self.pos = self.next_pos
            self.board.moves += 1

class CucumberR(Cucumber):
    stepper = [0,1]

class CucumberD(Cucumber):
    stepper = [1,0]

class Board:
    def __init__(self, lns):
        self.board = [list(i) for i in lns]
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.size = [self.rows, self.cols]
        self.CR = []
        self.CD = []
        for row in range(self.rows):
            for col in range(self.cols):
                el = self.board[row][col]
                if el == ">":
                    self.CR.append(CucumberR(self, row, col))
                if el == "v":
                    self.CD.append(CucumberD(self, row, col))

    def next_el(self, pos, step):
        return [(pos[i]+step[i]) % self.size[i] for i in range(2)]

    def is_free(self, pos):
        return self.board[pos[0]][pos[1]] == '.'

    def swap(self, pos, nex):
        temp = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = self.board[nex[0]][nex[1]]
        self.board[nex[0]][nex[1]] = temp

    def step(self):
        self.moves = 0
        for c in self.CR:
            c.prepare()
        for c in self.CR:
            c.move()
        for c in self.CD:
            c.prepare()
        for c in self.CD:
            c.move()

    def solve(self):
        ans = 0
        self.moves = 100
        while self.moves != 0:
            self.step()
            ans += 1
        return ans

b = Board(lines)
print(b.solve())