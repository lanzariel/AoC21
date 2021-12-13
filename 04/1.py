import sys

path = sys.argv[1]

class Board:
    def __init__(self, filereader):
        self.board = []
        for i in range(5):
            self.board.append([int(i) for i in filereader.readline().strip().split()])
        self.checked = [['O' for i in range(5)] for j in range(5)]
        self.rows = [0 for i in range(5)]
        self.cols = [0 for i in range(5)]
    
    def check(self, number):
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == number:
                    self.checked[row][col] = 'X'
                    self.rows[row] += 1
                    self.cols[col] += 1

    def unchecked(self):
        ans = 0
        for row in range(5):
            for col in range(5):
                if self.checked[row][col] == 'O':
                    ans += self.board[row][col]
        return ans
    
    def is_winning(self):
        for row in range(5):
            if self.rows[row]==5:
                return True
        for col in range(5):
            if self.cols[col]==5:
                return True
        return False

    def score(self, number):
        self.check(number)
        if self.is_winning():
            return number*self.unchecked()
        else:
            return 0

    def __str__(self):
        return str(self.board)

class Game:
    def __init__(self, b_list):
        self.boards = b_list
    def score(self, number):
        ans = 0
        for b in self.boards:
            ans += b.score(number)
        return ans

boards = []

with open(path, "r") as f:
    numbers = [int(i) for i in f.readline().strip().split(',')]
    while f.readline():
        new_b = Board(f)
        boards.append(new_b)

g = Game(boards)
for n in numbers:
    s = g.score(n)
    if s > 0:
        print(s)
        break
