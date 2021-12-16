import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [[int(j) for j in i.strip()] for i in f.readlines()]

#print(lines) 

class Board:
    def __init__(self, lns):
        self.board = lns
        b_val = 1e20
        self.cols = len(self.board[0])
        self.rows = len(self.board)
        self.mindist = [[b_val for i in range(self.cols)] for j in range(self.rows)]
        self.mindist[0][0] = 0
        self.toprocess = [(0,0)]
    
    def get_neighbors(self, element):
        row, col = element
        ans = []
        if row>0:
            ans.append((row-1, col))
        if row < self.rows-1:
            ans.append((row+1, col))
        if col > 0:
            ans.append((row, col-1))
        if col < self.cols-1:
            ans.append((row, col+1))
        return ans

    def get_val(self, element):
        return self.board[element[0]][element[1]]
    
    def get_curdist(self, element):
        return self.mindist[element[0]][element[1]]
    
    def set_curdist(self, element, value):
        self.mindist[element[0]][element[1]] = value

    def process_layer(self):
        new_toprocess = []
        for element in self.toprocess:
            el_val = self.get_curdist(element)
            for neighbor in self.get_neighbors(element):
                n_val = self.get_curdist(neighbor)
                delta = self.get_val(neighbor)
                if n_val > el_val + delta:
                    new_toprocess.append(neighbor)
                    self.set_curdist(neighbor, el_val + delta)
        self.toprocess = new_toprocess

    def solve(self):
        while len(self.toprocess)>0:
            self.process_layer()
    
    def give_ans(self):
        return self.mindist[self.rows-1][self.cols-1]

b = Board(lines)
b.solve()
print(b.give_ans())