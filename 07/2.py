import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = f.readlines()

v = [int(i) for i in lines[0].strip().split(',')]

d = [0 for i in range(max(v))]

dist = lambda x, y : ((x-y)**2 + abs(x-y))/2

l = len(v)
for i in range(len(d)):
    for j in range(l):
        d[i] += dist(i, v[j])
min_val = min(d)
min_ind = d.index(min_val)
print(int(min_val))
