with open("input.txt", "r") as f:
    lines = f.readlines()

v = [int(i) for i in lines]

ans = 0
prev = v[0]
for v_it in range(3,len(v)):
    v_it_val = v[v_it]
    prev = v[v_it-3]
    if v_it_val>prev:
        ans += 1
print(ans)
