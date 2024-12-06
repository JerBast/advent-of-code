from aocd import get_data


DATA = get_data(year=2024, day=6).splitlines()

START_X = 0
START_Y = 0
OBSTACLES = set()
for y, row in enumerate(DATA):
    for x, cell in enumerate(row):
        if cell == '#':
            OBSTACLES.add((x, y))
        elif cell == '^':
            START_X = x
            START_Y = y

H = len(DATA)
W = len(DATA[0])
INC = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def run() -> set[(int, int)]:
    inc_idx = 0
    visited = set()
    curr_x = START_X
    curr_y = START_Y

    while True:
        visited.add((curr_x, curr_y))
        inc_x, inc_y = INC[inc_idx]
        curr_x += inc_x
        curr_y += inc_y
        if curr_x < 0 or curr_x >= W or curr_y < 0 or curr_y >= H:
            break
        elif (curr_x, curr_y) in OBSTACLES:
            curr_x -= inc_x
            curr_y -= inc_y
            inc_idx = (inc_idx + 1) % 4

    return visited


def part1():
    print(len(run()))


def part2():
    loops = 0
    init_visited = run()
    init_visited.remove((START_X, START_Y))

    for (x, y) in init_visited:
        obstacles = OBSTACLES.copy()
        obstacles.add((x, y))

        inc_idx = 0
        visited = set()
        curr_x = START_X
        curr_y = START_Y

        while True:
            visited.add((curr_x, curr_y, inc_idx))
            inc_x, inc_y = INC[inc_idx]
            curr_x += inc_x
            curr_y += inc_y
            if curr_x < 0 or curr_x >= W or curr_y < 0 or curr_y >= H:
                break
            elif (curr_x, curr_y) in obstacles:
                curr_x -= inc_x
                curr_y -= inc_y
                inc_idx = (inc_idx + 1) % 4
            elif (curr_x, curr_y, inc_idx) in visited:
                loops += 1
                break

    print(loops)


if __name__ == '__main__':
    part1()
    part2()
