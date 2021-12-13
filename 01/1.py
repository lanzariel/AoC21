with open("input.txt", "r") as f:
    lines = f.readlines()

v = [int(i) for i in lines]

ans = 0
prev = v[0]
for v_it in v:
    if v_it>prev:
        ans += 1
    prev = v_it
print(ans)
