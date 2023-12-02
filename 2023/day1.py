import re

from typing import List
from aocd import get_data

DATA: List[str] = get_data(year=2023, day=1).splitlines()
REPR: List[str] = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def from_repr(s: str):
    return s if s.isdigit() else str(REPR.index(s))

def solve(regex: str):
    pattern = re.compile(regex)

    tot = 0
    for line in DATA:
        digits = [from_repr(i) for i in pattern.findall(line)]
        tot += int(digits[0] + digits[-1])
    print(tot)


if __name__ == '__main__':
    solve('\d')
    solve(f'(?=(\d|{"|".join(REPR[1:])}))')
