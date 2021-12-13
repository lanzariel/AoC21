with open("input.txt", "r") as f:
    lines = f.readlines()

tab = [list(i.strip()) for i in lines]

n = len(tab[0])

gamma = []
epsilon = []
for col in range(n):
    number_ones = 0
    number_zeros = 0
    for row in range(len(tab)):
        if tab[row][col] == "1":
            number_ones += 1
        else:
            number_zeros += 1
    if number_ones > number_zeros:
        gamma.append(1)
        epsilon.append(0)
    else:
        gamma.append(0)
        epsilon.append(1)

def debinarize(li):
    mul = 2**(len(li)-1)
    ans = 0
    for i in range(len(li)):
        ans += mul * li[i]
        mul = mul/2
    return ans

print(debinarize(gamma) * debinarize(epsilon))

