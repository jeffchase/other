pos = 0
dep = 0

with open('input.txt') as f:
    for line in f.readlines():
        cmd, amt = line.split()
        amt = int(amt)
        if cmd == 'forward':
            pos += amt
        elif cmd == 'down':
            dep += amt
        elif cmd == 'up':
            dep -= amt

print(pos * dep)

pos = 0
dep = 0
aim = 0

with open('input.txt') as f:
    for line in f.readlines():
        cmd, amt = line.split()
        amt = int(amt)
        if cmd == 'forward':
            pos += amt
            dep += amt * aim
        elif cmd == 'down':
            aim += amt
        elif cmd == 'up':
            aim -= amt

print(pos * dep)
