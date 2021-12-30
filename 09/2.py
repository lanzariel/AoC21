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
    
    def neighbors(self):
        ans = [self.l, self.r, self.u, self.d]
        ans = [i for i in ans if i.val != -1]
        return ans

    def valid_neighbors(self):
        return [i for i in self.neighbors() if i.val != 9]

    def __str__(self):
        return str(self.val) + "(" +str(self.row) + ", " + str(self.col) +  ")"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return self.val + other.val

    def __radd__(self, other):
        return self.val + other

outbound = Location(-1, -1, -1)
tab = [[int(i) for i in j.strip()] for j in lines]



class Board:
    def __init__(self):
        self.chessboard = []

    def addrow(self, row):
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

    def find_basins(self):
        to_process = set([i for j in self.chessboard for i in j if i.val != 9])
        basins = []
        while(len(to_process)>0):
            el = to_process.pop()
            processed = set([el])
            to_process_basin = set(el.neighbors())
            while len(to_process_basin) > 0:
                new_el = to_process_basin.pop()
                if new_el in to_process:
                    to_process.remove(new_el)
                if new_el.val != 9 and new_el.val != -1:
                    nbs = new_el.neighbors()
                    valid_nbs = [i for i in nbs if i.val !=9 and (i in to_process)]
                    for neighbor in valid_nbs:
                        if neighbor in to_process:
                            to_process.remove(neighbor)
                    to_process_basin.update(valid_nbs)
                    processed.add(new_el)
            basins.append(processed)
        return basins

    def ans_2(self):
        b = self.find_basins()
        b_l = [len(i) for i in b]
        b_l.sort(reverse = True)
        return b_l[0] * b_l[1] * b_l[2]

my_board = Board()
my_board.tab_fill(tab)
my_board.compute_n()
print(my_board.ans_2())
