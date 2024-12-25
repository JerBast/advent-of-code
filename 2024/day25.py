import numpy as np

from aocd import get_data


DATA = get_data(year=2024, day=25)
DATA = [np.array([np.array(list(r)) for r in s.splitlines()])
        for s in DATA.split('\n\n')]
H = DATA[0].shape[0]

KEYS = [np.count_nonzero(s == '#', axis=0)
        for s in DATA if all(c == '#' for c in s[-1])]
LOCKS = [np.count_nonzero(s == '#', axis=0)
         for s in DATA if all(c == '#' for c in s[0])]


def part1():
    print(sum(np.all((H - k) >= l) for k in KEYS for l in LOCKS))


if __name__ == '__main__':
    part1()
