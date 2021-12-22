with open("ans.txt", "r") as f:
    lines = f.readlines()

def get_n(line):
    bs = line.count("b")
    cs = line.count("c")
    ds = line.count("d")
    return 9*bs+3*cs+ds

res = [0 for i in range(28)]

for l in lines:
    res[get_n(l)] += 1
print(res[1:])