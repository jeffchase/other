import math

with open('input.txt') as f:
    data = list(map(int, f.readlines()))

prev = math.inf
count = 0

for depth in data:
    if depth > prev:
        count += 1
    prev = depth

print(count)

count = 0

for prev, depth in zip(data[:-3], data[3:]):
    if depth > prev:
        count += 1
print(count)
