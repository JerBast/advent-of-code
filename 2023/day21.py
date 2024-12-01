import numpy as np

from aocd import get_data


data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
data = get_data(year=2023, day=21)
data = np.array([np.array(list(row)) for row in data.split('\n')])

# Extract position of 'S' and replace with '.'
s_y, s_x = np.where(data == 'S')
s_y, s_x = s_y[0], s_x[0]
data[s_y, s_x] = '.'

# Perform BFS
STEP_LIMIT = 64
mem = [0] * (STEP_LIMIT + 1)
visited: set[tuple[int, int]] = {(s_y, s_x)}
queue: list[tuple[int, int, int]] = [(0, s_y, s_x)]

while len(queue):
    step, y, x = queue.pop(0)
    mem[step] += 1

    if step == STEP_LIMIT: continue

    if y > 0 and data[y - 1, x] == '.' and (y - 1, x) not in visited:
        visited.add((y - 1, x))
        queue.append((step + 1, y - 1, x))
    if x > 0 and data[y, x - 1] == '.' and (y, x - 1) not in visited:
        visited.add((y, x - 1))
        queue.append((step + 1, y, x - 1))
    if y < data.shape[0] - 1 and data[y + 1, x] == '.' and (y + 1, x) not in visited:
        visited.add((y + 1, x))
        queue.append((step + 1, y + 1, x))
    if x < data.shape[1] - 1 and data[y, x + 1] == '.' and (y, x + 1) not in visited:
        visited.add((y, x + 1))
        queue.append((step + 1, y, x + 1))

# Update memory
for i in range(2, STEP_LIMIT + 1):
    mem[i] += mem[i - 2]

# Part 1
print(mem[-1])
