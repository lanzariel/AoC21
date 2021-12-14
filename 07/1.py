import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = f.readlines()

v = [int(i) for i in lines[0].strip().split(',')]

d = [0 for i in lines[0]]

l = len(v)
for i in range(l):
    for j in range(l):
        d[i] += abs(v[i] - v[j])

print(d)
min_val = min(d)
min_ind = d.index(min_val)
print(min_val)
print(min_ind)
print(v[min_ind])
