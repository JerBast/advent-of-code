import sys
import numpy as np

from aocd import get_data
from collections import defaultdict


DATA = get_data(year=2024, day=20)
DATA = np.array([np.array(list(row)) for row in DATA.splitlines()])

CHEATS = []
for y in range(1, DATA.shape[0] - 1):
    for x in range(1, DATA.shape[1] - 1):
        if DATA[y, x] == '#':
            CHEATS.append((x, y))


def shortest_path(matrix: np.ndarray):
    s_y, s_x = np.argwhere(matrix == 'S')[0]

    distances = defaultdict(lambda: sys.maxsize)
    distances[(s_x, s_y)] = 0
    visited = set()

    for _ in range(matrix.shape[0] * matrix.shape[1]):
        pos = None
        dist = sys.maxsize
        for k, v in distances.items():
            if k in visited or v >= dist:
                continue
            pos = k
            dist = v

        if pos is None:
            break

        visited.add(pos)
        x, y = pos

        if x > 0 and matrix[y, x - 1] != '#' and (x - 1, y) not in visited and dist + 1 < distances[(x - 1, y)]:
            distances[(x - 1, y)] = dist + 1
        if y > 0 and matrix[y - 1, x] != '#' and (x, y - 1) not in visited and dist + 1 < distances[(x, y - 1)]:
            distances[(x, y - 1)] = dist + 1
        if x + 1 < matrix.shape[1] and matrix[y, x + 1] != '#' and (x + 1, y) not in visited and dist + 1 < distances[(x + 1, y)]:
            distances[(x + 1, y)] = dist + 1
        if y + 1 < matrix.shape[0] and matrix[y + 1, x] != '#' and (x, y + 1) not in visited and dist + 1 < distances[(x, y + 1)]:
            distances[(x, y + 1)] = dist + 1

    return distances


def part1():
    matrix = DATA.copy()
    distances = list(shortest_path(matrix).items())

    ans = 0
    for idx, i in enumerate(distances):
        p1, v1 = i
        for p2, v2 in distances[idx+1:]:
            d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            if d == 2 and abs(v1 - v2) - d >= 100:
                ans += 1
    print(ans)


def part2():
    matrix = DATA.copy()
    distances = list(shortest_path(matrix).items())

    ans = 0
    for idx, i in enumerate(distances):
        p1, v1 = i
        for p2, v2 in distances[idx+1:]:
            d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            if 2 <= d <= 20 and abs(v1 - v2) - d >= 100:
                ans += 1
    print(ans)


if __name__ == '__main__':
    part1()
    part2()
