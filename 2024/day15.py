import numpy as np

from aocd import get_data


MAP, DIRECTIONS = get_data(year=2024, day=15).split('\n\n')
DIRECTIONS = ''.join(DIRECTIONS.splitlines())
MAP = np.array([np.array(list(row)) for row in MAP.splitlines()])


def can_move(map: np.array, x: int, y: int, direction: chr) -> bool:
    dx = 1 if direction == '>' else (-1 if direction == '<' else 0)
    dy = 1 if direction == 'v' else (-1 if direction == '^' else 0)
    match map[y, x]:
        case '.':
            return True
        case '#':
            return False
        case '@':
            return can_move(map, x + dx, y + dy, direction)
        case 'O':
            return can_move(map, x + dx, y + dy, direction)
        case '[':
            c_m = can_move(map, x + dx, y + dy, direction)
            if direction in '^v':
                c_m &= can_move(map, x + 1, y + dy, direction)
            return c_m
        case ']':
            c_m = can_move(map, x + dx, y + dy, direction)
            if direction in '^v':
                c_m &= can_move(map, x - 1, y + dy, direction)
            return c_m
    return False


def move(map: np.array, x: int, y: int, direction: chr) -> tuple[int, int]:
    dx = 1 if direction == '>' else (-1 if direction == '<' else 0)
    dy = 1 if direction == 'v' else (-1 if direction == '^' else 0)
    match map[y, x]:
        case '@':
            move(map, x + dx, y + dy, direction)
            map[y + dy, x + dx] = '@'
            map[y, x] = '.'
        case 'O':
            move(map, x + dx, y + dy, direction)
            map[y + dy, x + dx] = 'O'
            map[y, x] = '.'
        case '[':
            if direction in '^v':
                move(map, x + 1, y + dy, direction)
                map[y + dy, x + 1] = ']'
                map[y, x + 1] = '.'
            move(map, x + dx, y + dy, direction)
            map[y + dy, x + dx] = '['
            map[y, x] = '.'
        case ']':
            if direction in '^v':
                move(map, x - 1, y + dy, direction)
                map[y + dy, x - 1] = '['
                map[y, x - 1] = '.'
            move(map, x + dx, y + dy, direction)
            map[y + dy, x + dx] = ']'
            map[y, x] = '.'
    return x + dx, y + dy


def score(map: np.array) -> int:
    return sum(100 * y + x for y, row in enumerate(map) for x, tile in enumerate(row) if tile in '[O')


def part1():
    map = MAP.copy()

    r_y, r_x = np.argwhere(map == '@')[0]
    for direction in DIRECTIONS:
        if can_move(map, r_x, r_y, direction):
            r_x, r_y = move(map, r_x, r_y, direction)

    print(score(map))


def part2():
    map = MAP.copy()
    map.resize((map.shape[0], map.shape[1] * 2))
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile in '.#':
                map[y][x*2:x*2+2] = tile
            elif tile == 'O':
                map[y][x*2] = '['
                map[y][x*2+1] = ']'
            elif tile == '@':
                map[y][x*2] = '@'
                map[y][x*2+1] = '.'

    r_y, r_x = np.argwhere(map == '@')[0]
    for direction in DIRECTIONS:
        if can_move(map, r_x, r_y, direction):
            r_x, r_y = move(map, r_x, r_y, direction)

    print(score(map))


if __name__ == '__main__':
    part1()
    part2()
