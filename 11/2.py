import sys
path = sys.argv[1]

with open(path, "r") as f:
    lines = [[int(j) for j in list(i.strip())] for i in f.readlines()]

class board:
    def __init__(self, board):
        self.board = board

    def neighbors(self, row, col):
        ans = []
        for d_row in [-1, 0 ,1]:
            for d_col in [-1, 0 ,1]:
                ans.append((row+d_row, col+d_col))
        ans = [i for i in ans if i[0]>=0 and i[1]>=0]
        ans = [i for i in ans if i[0] < len(self.board) and i[1] < len(self.board[1])]
        ans = [i for i in ans if i!=(row,col)]
        return ans

    def step(self):
        glowing = set()
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                self.board[row][col] += 1
                if self.board[row][col] == 10:
                    self.board[row][col] = 0
                    glowing.add((row,col))
        to_process = list(glowing)
        while len(to_process)>0:
            el = to_process.pop()
            for n in self.neighbors(el[0], el[1]):
                if self.board[n[0]][n[1]]!=0:
                    self.board[n[0]][n[1]] += 1
                    if self.board[n[0]][n[1]] >= 10:
                        self.board[n[0]][n[1]] = 0
                        glowing.add(n)
                        to_process.append(n)
        return len(glowing)

    def answer(self):
        ans = 0
        for i in range(1000000):
            flashing = self.step()
            if flashing ==100 :
                print(i+1)
                break
            ans += flashing 
        return ans

b = board(lines)
b.answer()
