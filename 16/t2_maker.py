with open("T2.txt", "r") as f:
    lines = [i.strip() for i in f.readlines()]

for i in range(len(lines)):
    with open("T2_" + str(i) +".txt", "w") as f:
        f.write(lines[i])