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
#print(v)
#print(d)
min_val = min(d)
min_ind = d.index(min_val)
print(min_val, min_ind)
print(sum(v)/len(v))
#print(min_ind)
#print(v[min_ind])
