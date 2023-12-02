import re

from aocd import get_data
from typing import List

DATA: List[str] = get_data(year=2023, day=1).splitlines()
REPR: List[str] = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def part1():
    pattern = re.compile('\d')

    tot = 0
    for line in DATA:
        digits = pattern.findall(line)
        tot += int(digits[0] + digits[-1])
    print(tot)


def part2():
    pattern = re.compile(f'(?=(\d|{"|".join(REPR[1:])}))')

    tot = 0
    for line in DATA:
        digits = [i if i.isdigit() else str(REPR.index(i)) for i in pattern.findall(line)]
        tot += int(digits[0] + digits[-1])
    print(tot)


if __name__ == '__main__':
    part1()
    part2()
