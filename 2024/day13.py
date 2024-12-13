import re

from aocd import get_data


DATA = get_data(year=2024, day=13).split('\n\n')

A: list[tuple[int, int]] = []
B: list[tuple[int, int]] = []
P: list[tuple[int, int]] = []
for group in DATA:
    g = group.splitlines()
    A.append(tuple(map(int, re.findall(r'(\d+)', g[0]))))
    B.append(tuple(map(int, re.findall(r'(\d+)', g[1]))))
    P.append(tuple(map(int, re.findall(r'(\d+)', g[2]))))


def impl(a: tuple[int, int], b: tuple[int, int], p: tuple[int, int], p_conv: int = 0) -> int:
    ax, ay = a
    bx, by = b
    px, py = p
    px += p_conv
    py += p_conv

    bc = (ax * py - px * ay) / (ax * by - bx * ay)
    ac = (px - bc * bx) / ax
    return int(bc + 3 * ac) if bc.is_integer() and ac.is_integer() else 0


def part1():
    print(sum(impl(a, b, p) for a, b, p in zip(A, B, P)))


def part2():
    print(sum(impl(a, b, p, 10000000000000) for a, b, p in zip(A, B, P)))


if __name__ == '__main__':
    part1()
    part2()
