with open('input.txt', 'r') as f:
    lines = f.readlines()

class Submarine:
    h=0
    d = 0
    def read_instruction(self, inst):
        word, number = inst.split()
        number = int(number)
        if word == "forward":
            self.h += number
        elif word == "down":
            self.d += number
        else:
            self.d -= number

    def read_many(self, lst):
        for el in lst:
            self.read_instruction(el)

    def ans_1(self):
        return self.h * self.d

s = Submarine()
s.read_many(lines)
print(s.ans_1())
