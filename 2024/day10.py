from typing import Optional

from aocd import get_data


DATA = get_data(year=2024, day=10)
GRID = [list(map(int, row)) for row in DATA.splitlines()]
W = len(GRID[0])
H = len(GRID)


def impl(x: int, y: int, height: int, visited: Optional[set[tuple[int, int]]] = None) -> int:
    if height == 9:
        score = 1
        if visited is not None:
            score = 0 if (x, y) in visited else 1
            visited.add((x, y))
        return score

    res = 0
    if x > 0 and GRID[y][x - 1] == height + 1:
        res += impl(x - 1, y, height + 1, visited)
    if y > 0 and GRID[y - 1][x] == height + 1:
        res += impl(x, y - 1, height + 1, visited)
    if x + 1 < W and GRID[y][x + 1] == height + 1:
        res += impl(x + 1, y, height + 1, visited)
    if y + 1 < H and GRID[y + 1][x] == height + 1:
        res += impl(x, y + 1, height + 1, visited)
    return res


def part1():
    print(sum(impl(x, y, 0, set()) for y in range(H)
          for x in range(W) if GRID[y][x] == 0))


def part2():
    print(sum(impl(x, y, 0) for y in range(H)
          for x in range(W) if GRID[y][x] == 0))


if __name__ == '__main__':
    part1()
    part2()
