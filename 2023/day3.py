import re

from math import prod
from aocd import get_data


DATA = get_data(year=2023, day=3).splitlines()
# DATA = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..""".splitlines()

HEIGHT = len(DATA)
assert HEIGHT > 0
WIDTH = len(DATA[0])


def is_symbol(c: str):
    return not (c.isalnum() or c == '.')


def is_part(y, x_start, x_end):
    y_min = max(0, y-1)
    y_max = min(y+1, HEIGHT-1)
    x_min = max(0, x_start-1)
    x_max = min(x_end, WIDTH-1)

    for row in DATA[y_min:y_max + 1]:
        if any(map(is_symbol, row[x_min:x_max + 1])):
            return True
    return False


def part1():
    pattern = re.compile('\d+')

    tot_parts = 0
    for y, row in enumerate(DATA):
        for number_match in pattern.finditer(row):
            if is_part(y, number_match.start(), number_match.end()):
                tot_parts += int(number_match.group(0))

    print(tot_parts)


def part2():
    pattern = re.compile('\d+')

    gear_ratios = 0
    for y, row in enumerate(DATA):
        for x, c in enumerate(row):
            if c != '*': continue
            
            gears = []
            for level_idx, level in enumerate(DATA[max(0, y-1):min(y+2, HEIGHT)]):
                actual_level = max(0, y-1) + level_idx
                for number_match in pattern.finditer(level):
                    start = number_match.start()
                    end = number_match.end()
                    if (start - 1 <= x <= end) and (actual_level - 1 <= y <= actual_level + 1):
                        gears.append(int(number_match.group(0)))
            if len(gears) == 2:
                gear_ratios += prod(gears)


    print(gear_ratios)


if __name__ == '__main__':
    part1()
    part2()
