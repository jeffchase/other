from collections import defaultdict
import sys

# num -> line count, board total

boards = []

with open('input') as f:
    draws = [int(x) for x in f.readline().strip().split(',')]
    while f.readline() != '':
        board = []
        for _ in range(5):
            board.append([int(x) for x in f.readline().split()])
        boards.append(board)

index = defaultdict(list)

for board in boards:
    total = [sum(map(sum, board))]
    rows = [[5] for _ in range(5)]
    cols = [[5] for _ in range(5)]
    won = [False]
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            index[v].append((rows[r], cols[c], total, won))

winners = 0

for draw in draws:
    for row, col, total, won in index[draw]:
        if won[0]:
            continue
        row[0] -= 1
        col[0] -= 1
        total[0] -= draw
        if row[0] == 0 or col[0] == 0:
            winners += 1
            won[0] = True
            if winners == len(boards):
                print(total[0] * draw)
                sys.exit()
