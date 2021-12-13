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
                self.dots.append(new_el)
                if new_el in self.d:
                    self.d[new_el] += 1
                else:
                    self.d[new_el] = 1
        if y_A == y_B:
            for j in range(min(x_A, x_B), max(x_A, x_B) + 1):
                new_el = (j, y_A)
                self.dots.append(new_el)
                if new_el in self.d:
                    self.d[new_el] += 1
                else:
                    self.d[new_el] = 1

    def ans_1(self):
        ans = 0
        for key, val in self.d.items():
            if val>=2:
                ans += 1
        return ans


b = Board(lines)
print(b.ans_1())
