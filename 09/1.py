import sys
path = sys.argv[1]
with open(path, "r") as f:
    lines = f.readlines()

class Location:
    def __init__(self, r, c, v):
        self.row = r
        self.col = c
        self.val = v

    def is_lower(self, other_v):
        if other_v.val == -1:
            return True
        else:
            return self.val < other_v.val
    
    def is_low(self):
        c1 = self.is_lower(self.l)
        c2 = self.is_lower(self.r)
        c3 = self.is_lower(self.u)
        c4 = self.is_lower(self.d)
        return c1 and c2 and c3 and c4

outbound = Location(-1, -1, -1)

tab = [[int(i) for i in j.strip()] for j in lines]



class Board:
    def __init__(self):
        self.chessboard = []

    def addrow(row):
        self.chessboard.append(row)

    def relative_position(self, el, d_r, d_c):
        r_new = el.row + d_r
        c_new = el.col + d_c
        if r_new < 0 or r_new >= len(self.chessboard):
            return outbound
        elif c_new < 0 or c_new >= len(self.chessboard[0]):
            return outbound
        else:
            return self.chessboard[r_new][c_new]

    def tab_fill(self, tab):
        for row in range(len(tab)):
            new_row = []
            for col in range(len(tab[0])):
                new_row.append(Location(row,col,tab[row][col]))
            self.chessboard.append(new_row)

    def compute_n(self):
        for row in self.chessboard:
            for el in row:
                el.u = self.relative_position(el, 0, -1)
                el.d = self.relative_position(el, 0 , 1)
                el.r = self.relative_position(el, 1, 0)
                el.l = self.relative_position(el, -1, 0)

    def ans_1(self):
        ans = 0
        for row in self.chessboard:
            for el in row:
                if el.is_low(): 
                    ans += 1+el.val
        return ans

my_board = Board()
my_board.tab_fill(tab)
my_board.compute_n()
print(my_board.ans_1())
