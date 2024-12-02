from collections import Counter

from aocd import get_data


DATA = get_data(year=2024, day=1).splitlines()
L = []
R = []

for idx, row in enumerate(DATA):
    l, r = map(int, row.split())
    L.append(l)
    R.append(r)

L = sorted(L)
R = sorted(R)


def part1():
    print(sum(abs(l - r) for l, r in zip(L, R)))


def part2():
    r_cnt = Counter(R)
    print(sum(l * r for l in L if not (r := r_cnt.get(l)) is None))


if __name__ == '__main__':
    part1()
    part2()
