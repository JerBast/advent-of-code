import numpy as np

from aocd import get_data


def print_d(data: np.array):
    for row in data:
        print(''.join(row))
    print()

def compute_cost(data: np.array):
    res = 0
    for idx, row in enumerate(data):
        res += (len(data) - idx) * sum(v == 'O' for v in row)
    return res

def saturate_up(data: np.array):
    height, width = data.shape
    for x in range(width):
        for y in range(1, height):
            j = y
            while j > 0 and data[j - 1, x] == '.' and data[j, x] == 'O':
                data[j - 1, x], data[j, x] = 'O', '.'
                j -= 1

def saturate_down(data: np.array):
    height, width = data.shape
    for x in range(width):
        for y in range(height - 2, -1, -1):
            j = y
            while j < height - 1 and data[j + 1, x] == '.' and data[j, x] == 'O':
                data[j + 1, x], data[j, x] = 'O', '.'
                j += 1

def saturate_right(data: np.array):
    height, width = data.shape
    for y in range(height):
        for x in range(width - 2, -1, -1):
            j = x
            while j < width - 1 and data[y, j + 1] == '.' and data[y, j] == 'O':
                data[y, j + 1], data[y, j] = 'O', '.'
                j += 1


def saturate_left(data: np.array):
    height, width = data.shape
    for y in range(height):
        for x in range(1, width):
            j = x
            while j > 0 and data[y, j - 1] == '.' and data[y, j] == 'O':
                data[y, j - 1], data[y, j] = 'O', '.'
                j -= 1

data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
data = get_data(year=2023, day=14)
data = np.array(list(map(list, data.split('\n'))))

# Part 1
saturate_up(data)
print(compute_cost(data))

# Part 2
res = 0
visited = {}
while True:
    # Perform cycle
    saturate_up(data)
    saturate_left(data)
    saturate_down(data)
    saturate_right(data)

    # Compare and update results
    h = hash(data.tobytes())
    if h in visited:
        break

    visited[h] = compute_cost(data)

# Find the start of the inner cycle
inner_cycle = []
start_cycle = False
offset = 0
h = hash(data.tobytes())

for k, v in visited.items():
    if k == h:
        start_cycle = True
    elif not start_cycle:
        offset += 1
    
    if start_cycle:
        inner_cycle.append(v)

# Now pretend like we did it 1_000_000_000 times
print(inner_cycle[(1_000_000_000 - offset - 1) % len(inner_cycle)])
