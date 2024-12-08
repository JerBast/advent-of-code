from itertools import combinations
from collections import defaultdict

from aocd import get_data


DATA = get_data(year=2024, day=8).splitlines()

W = len(DATA[0])
H = len(DATA)

NODES = defaultdict(list)
for y, row in enumerate(DATA):
    for x, cell in enumerate(row):
        if cell != '.':
            NODES[cell].append((x, y))


def part1():
    anti_nodes = set()
    for nodes in NODES.values():
        for n1, n2 in combinations(nodes, 2):
            x1, y1 = n1
            x2, y2 = n2
            ax1, ay1 = 2 * x1 - x2, 2 * y1 - y2
            if 0 <= ax1 < W and 0 <= ay1 < H:
                anti_nodes.add((ax1, ay1))
            ax2, ay2 = 2 * x2 - x1, 2 * y2 - y1
            if 0 <= ax2 < W and 0 <= ay2 < H:
                anti_nodes.add((ax2, ay2))
    print(len(anti_nodes))


def part2():
    anti_nodes = set()
    for nodes in NODES.values():
        for n1, n2 in combinations(nodes, 2):
            x1, y1 = n1
            x2, y2 = n2
            xi, yi = n1
            while 0 <= xi < W and 0 <= yi < H:
                anti_nodes.add((xi, yi))
                xi -= x2 - x1
                yi -= y2 - y1
            xi, yi = n2
            while 0 <= xi < W and 0 <= yi < H:
                anti_nodes.add((xi, yi))
                xi -= x1 - x2
                yi -= y1 - y2
    print(len(anti_nodes))


if __name__ == '__main__':
    part1()
    part2()
