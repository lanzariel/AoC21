import sys
path = sys.argv[1]

with open(path, 'r') as f:
    lines = f.readlines()

class Board:
    def __init__(self, lln):
        self.dots = []
        self.d = dict()
        for l in lln:
            self.add_line(l)

    def add_line(self, l):
        A, B = l.split(" -> ")
        x_A, y_A = [int(i) for i in A.split(',')]
        x_B, y_B = [int(i) for i in B.split(',')]
        if x_A == x_B:
            for j in range(min(y_A, y_B), max(y_A, y_B) + 1):
                new_el = (x_A, j)
                self.add_el(new_el)
        elif y_A == y_B:
            for j in range(min(x_A, x_B), max(x_A, x_B) + 1):
                new_el = (j, y_A)
                self.add_el(new_el)
        else:
            length = abs(x_A - x_B)
            d_y = (y_B-y_A)//length
            d_x = (x_B-x_A)//length
            for j in range(length + 1):
                new_el = (x_A + j*d_x, y_A + j*d_y)
                self.add_el(new_el)

    def add_el(self, new_el):
        self.dots.append(new_el)
        if new_el in self.d:
            self.d[new_el] += 1
        else:
            self.d[new_el] = 1


    def ans_2(self):
        ans = 0
        for key, val in self.d.items():
            if val>=2:
                ans += 1
        return ans


b = Board(lines)
print(b.ans_2())
