
lines = []

with open('input') as f:
    for line in f.readlines():
        a, b = line.strip().split(' -> ')
        lines.append((a.split(','), b.split(',')))

g = [[0] * 1000 for _ in range(1000)]

count = 0

for a, b in lines:
    if a[0] == b[0]:
        z = a[0]
        x, y = a[1], b[1]
    elif a[1] == b[1]:
        z = a[1]
        x, y = a[0], b[0]
    else:
        continue

    if x > y:
        x, y = y, x

