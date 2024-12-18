import sys
import numpy as np

from collections import defaultdict

from aocd import get_data


DATA = get_data(year=2024, day=18)


def shortest_path(matrix: np.ndarray):
    distances = defaultdict(lambda: sys.maxsize)
    distances[(0, 0)] = 0
    visited = set()

    for _ in range(matrix.shape[0] * matrix.shape[1]):
        state = None
        dist = sys.maxsize
        for k, v in distances.items():
            if k in visited or v >= dist:
                continue
            state = k
            dist = v

        if state is None:
            return distances

        visited.add(state)
        x, y = state

        if x > 0 and matrix[y, x - 1] != 1 and (x - 1, y) not in visited and dist + 1 < distances[(x - 1, y)]:
            distances[(x - 1, y)] = dist + 1
        if y > 0 and matrix[y - 1, x] != 1 and (x, y - 1) not in visited and dist + 1 < distances[(x, y - 1)]:
            distances[(x, y - 1)] = dist + 1
        if x + 1 < matrix.shape[1] and matrix[y, x + 1] != 1 and (x + 1, y) not in visited and dist + 1 < distances[(x + 1, y)]:
            distances[(x + 1, y)] = dist + 1
        if y + 1 < matrix.shape[0] and matrix[y + 1, x] != 1 and (x, y + 1) not in visited and dist + 1 < distances[(x, y + 1)]:
            distances[(x, y + 1)] = dist + 1

    return distances


def path_exists(matrix: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> bool:
    visited = set()
    queue = [start]
    while len(queue):
        pos = queue.pop(0)
        if pos == end:
            return True
        visited.add(pos)
        x, y = pos
        if x > 0 and matrix[y, x - 1] != 1 and (x - 1, y) not in visited:
            queue.append((x - 1, y))
        if y > 0 and matrix[y - 1, x] != 1 and (x, y - 1) not in visited:
            queue.append((x, y - 1))
        if x + 1 < matrix.shape[1] and matrix[y, x + 1] != 1 and (x + 1, y) not in visited:
            queue.append((x + 1, y))
        if y + 1 < matrix.shape[0] and matrix[y + 1, x] != 1 and (x, y + 1) not in visited:
            queue.append((x, y + 1))
    return False


def part1():
    sz = 70
    matrix = np.zeros((sz + 1, sz + 1))
    for row in DATA.splitlines()[:1024]:
        x, y = map(int, row.split(','))
        matrix[y, x] = 1

    ds = shortest_path(matrix)
    print(ds[(sz, sz)])


def part2():
    sz = 70
    matrix = np.zeros((sz + 1, sz + 1))
    corrupted = [tuple(map(int, row.split(','))) for row in DATA.splitlines()]

    for c in corrupted:
        x, y = c
        matrix[y, x] = 1

    for i in range(len(corrupted))[::-1]:
        x, y = corrupted[i]
        matrix[y, x] = 0
        if path_exists(matrix, (0, 0), (sz, sz)):
            x, y = corrupted[i]
            print(f'{x},{y}')
            break


if __name__ == '__main__':
    part1()
    part2()
