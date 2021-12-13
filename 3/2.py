with open("input.txt", "r") as f:
    lines = f.readlines()

tab = [[int(j) for j in list(i.strip())] for i in lines]

n = len(tab[0])

def debinarize(li):
    mul = 2**(len(li)-1)
    ans = 0
    for i in range(len(li)):
        ans += mul * li[i]
        mul = mul/2
    return ans

class Parent:
    def __init__(self, tab):
        self.tab = [i.copy() for i in tab]

    def gamma_epsilon(self):
        gamma = []
        epsilon = []
        for col in range(n):
            number_ones = 0
            number_zeros = 0
            for row in range(len(self.tab)):
                if self.tab[row][col] == 1:
                  number_ones += 1
                else:
                    number_zeros += 1
            if number_ones >= number_zeros:
                gamma.append(1)
                epsilon.append(0)
            else:
                gamma.append(0)
                epsilon.append(1)
        self.gamma = gamma
        self.epsilon = epsilon

    def filter_byc(self, col):
        self.gamma_epsilon()
        newtab = []
        right_one = self.bit_criteria(col)
        for t in self.tab:
            if int(t[col]) == right_one:
                newtab.append(t)
        self.tab = newtab

    def solve(self):
        for i in range(len(self.tab[0])):
            if len(self.tab) == 1:
                return self.tab[0]
            self.filter_byc(i)
        return self.tab[0]

class Ox(Parent):
    def bit_criteria(self,col):
        return self.gamma[col]

class Co(Parent):
    def bit_criteria(self,col):
        return self.epsilon[col]

o = Ox(tab)
c = Co(tab)

print(debinarize(o.solve()))
print(debinarize(c.solve()))

print(debinarize(o.solve()) * debinarize(c.solve()))

