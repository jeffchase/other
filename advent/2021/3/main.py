import numpy as np
from operator import itemgetter

data = []
with open('input.txt') as f:
    for line in f.readlines():
        data.append(np.array(list(line.strip()), dtype=int))

# Part 1

total = len(data)
counts = sum(data)

gamma = 0
epsilon = 0

for bit in counts:
    gamma *= 2
    epsilon *= 2
    if bit >= total / 2:
        gamma += 1
    if bit <= total / 2:
        epsilon += 1

print(gamma * epsilon)

# Part 2

rem = data

def partition(a, p=bool):
    r1, r2 = [], []
    for v in a:
        if p(v):
            r1.append(v)
        else:
            r2.append(v)
    return (r1, r2)

for bit in range(len(data[0])):
    one, zero = partition(rem, itemgetter(bit))
    if len(one) >= len(zero):
        rem = one
    else:
        rem = zero

oxygen = int(''.join(map(str, rem[0])), base=2)

rem = data

for bit in range(len(data[0])):
    if len(rem) == 1:
        break
    one, zero = partition(rem, itemgetter(bit))
    if len(one) < len(zero):
        rem = one
    else:
        rem = zero

co2 = int(''.join(map(str, rem[0])), base=2)

print(oxygen * co2)
