import sys
import numpy as np

from enum import Enum
from aocd import get_data


sys.setrecursionlimit(2500)

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


visited = set()
dir_visited = set()
def reflect(x: int, y: int, direction: Direction, data: np.array):
    if y < 0 or y >= data.shape[0] or x < 0 or x >= data.shape[1]:
        return

    if (x, y, direction) in dir_visited:
        return
    dir_visited.add((x, y, direction))
    
    if data[y][x] == '.' or data[y][x] == '#':
        data[y][x] = '#'
        if direction == Direction.NORTH:
            reflect(x, y - 1, direction, data)
        elif direction == Direction.SOUTH:
            reflect(x, y + 1, direction, data)
        elif direction == Direction.EAST:
            reflect(x + 1, y, direction, data)
        else:
            reflect(x - 1, y, direction, data)
    elif data[y][x] == '/':
        visited.add((x, y))
        if direction == Direction.EAST:
            reflect(x, y - 1, Direction.NORTH, data)
        elif direction == Direction.WEST:
            reflect(x, y + 1, Direction.SOUTH, data)
        elif direction == Direction.NORTH:
            reflect(x + 1, y, Direction.EAST, data)
        else:
            reflect(x - 1, y, Direction.WEST, data)
    elif data[y][x] == '\\':
        visited.add((x, y))
        if direction == Direction.EAST:
            reflect(x, y + 1, Direction.SOUTH, data)
        elif direction == Direction.WEST:
            reflect(x, y - 1, Direction.NORTH, data)
        elif direction == Direction.NORTH:
            reflect(x - 1, y, Direction.WEST, data)
        else:
            reflect(x + 1, y, Direction.EAST, data)
    elif data[y][x] == '|':
        visited.add((x, y))
        if direction == Direction.EAST or direction == Direction.WEST:
            reflect(x, y - 1, Direction.NORTH, data)
            reflect(x, y + 1, Direction.SOUTH, data)
        elif direction == Direction.NORTH:
            reflect(x, y - 1, Direction.NORTH, data)
        else:
            reflect(x, y + 1, Direction.SOUTH, data)
    elif data[y][x] == '-':
        visited.add((x, y))
        if direction == Direction.NORTH or direction == Direction.SOUTH:
            reflect(x - 1, y, Direction.WEST, data)
            reflect(x + 1, y, Direction.EAST, data)
        elif direction == Direction.EAST:
            reflect(x + 1, y, Direction.EAST, data)
        else:
            reflect(x - 1, y, Direction.WEST, data)


data = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""
data = get_data(year=2023, day=16)
data = np.array(list(map(list, data.split('\n'))))
data_cpy = np.copy(data)

# Part 1
reflect(0, 0, Direction.EAST, data)
print(np.count_nonzero(data == '#') + len(visited))

# Part 2
ans = 0
sz = data_cpy.shape[0]

for i in range(sz):
    visited = set()
    dir_visited = set()
    data = data_cpy.copy()
    reflect(i, 0, Direction.SOUTH, data)
    ans = max(ans, np.count_nonzero(data == '#') + len(visited))

    visited = set()
    dir_visited = set()
    data = data_cpy.copy()
    reflect(i, sz - 1, Direction.NORTH, data)
    ans = max(ans, np.count_nonzero(data == '#') + len(visited))

    visited = set()
    dir_visited = set()
    data = data_cpy.copy()
    reflect(0, i, Direction.EAST, data)
    ans = max(ans, np.count_nonzero(data == '#') + len(visited))

    visited = set()
    dir_visited = set()
    data = data_cpy.copy()
    reflect(sz - 1, i, Direction.WEST, data)
    ans = max(ans, np.count_nonzero(data == '#') + len(visited))
print(ans)
