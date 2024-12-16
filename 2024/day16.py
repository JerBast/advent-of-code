import sys
import numpy as np

from collections import defaultdict

from aocd import get_data


DATA = get_data(year=2024, day=16)
DATA = np.array([np.array(list(row)) for row in DATA.splitlines()])
S_Y, S_X = np.argwhere(DATA == 'S')[0]
E_Y, E_X = np.argwhere(DATA == 'E')[0]
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def shortest_path(start: tuple[int, int]):
    distances = defaultdict(lambda: sys.maxsize)
    distances[(*start, 1)] = 0
    visited = set()

    for _ in range(4 * (DATA.shape[0] - 2) * (DATA.shape[1] - 2)):
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
        x, y, d = state

        nd = d
        dx, dy = DIRECTIONS[nd]
        nx, ny = x + dx, y + dy
        if DATA[ny, nx] != '#' and (nx, ny, nd) not in visited and dist + 1 < distances[(nx, ny, nd)]:
            distances[(nx, ny, nd)] = dist + 1

        nd = (d + 1) % 4
        dx, dy = DIRECTIONS[nd]
        nx, ny = x + dx, y + dy
        if DATA[ny, nx] != '#' and (nx, ny, nd) not in visited and dist + 1001 < distances[(nx, ny, nd)]:
            distances[(nx, ny, nd)] = dist + 1001

        nd = (d + 3) % 4
        dx, dy = DIRECTIONS[nd]
        nx, ny = x + dx, y + dy
        if DATA[ny, nx] != '#' and (nx, ny, nd) not in visited and dist + 1001 < distances[(nx, ny, nd)]:
            distances[(nx, ny, nd)] = dist + 1001

    return distances


def trace(distances, cost: int, pos: tuple[int, int], end: tuple[int, int], visited: set[tuple[int, int]]):
    visited.add(pos)

    if pos == end:
        return visited

    x, y = pos
    d = next(d for d in range(4) if distances[(x, y, d)] == cost)

    dx, dy = DIRECTIONS[d]
    nx, ny = x - dx, y - dy

    for nd in range(4):
        dist = distances[(nx, ny, nd)]
        if dist == cost - 1 or dist == cost - 1001:
            trace(distances, distances[(nx, ny, nd)], (nx, ny), end, visited)
    return visited


if __name__ == '__main__':
    # Part 1
    distances = shortest_path((S_X, S_Y))
    print(min(distances[(E_X, E_Y, d)] for d in range(4)))

    # Part 2
    visited = set()
    print(len(trace(distances, min(distances[(E_X, E_Y, d)] for d in range(
        4)), (E_X, E_Y), (S_X, S_Y), visited)))
