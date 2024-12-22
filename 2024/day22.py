import numpy as np

from aocd import get_data
from collections import defaultdict


DATA = get_data(year=2024, day=22)
DATA = list(map(int, DATA.splitlines()))


def compute_next_secret(secret: int) -> int:
    new_secret = secret
    new_secret = (new_secret ^ (new_secret * 64)) % 16777216
    new_secret = (new_secret ^ (new_secret // 32)) % 16777216
    new_secret = (new_secret ^ (new_secret * 2048)) % 16777216
    return new_secret


def part1():
    ans = 0
    for secret in DATA:
        for _ in range(2000):
            secret = compute_next_secret(secret)
        ans += secret
    print(ans)


def part2():
    traders = []
    for secret in DATA:
        w = []
        info = defaultdict(lambda: 0)
        for _ in range(2000):
            new_secret = compute_next_secret(secret)
            w.append((new_secret % 10) - (secret % 10))
            if len(w) == 4:
                if tuple(w) not in info:
                    info[tuple(w)] = new_secret % 10
                w.pop(0)
            secret = new_secret
        traders.append(info)

    ws = map(tuple, np.unique(np.concatenate(
        [list(info.keys()) for info in traders]), axis=0))
    print(max(sum(info[w] for info in traders) for w in ws))


if __name__ == '__main__':
    part1()
    part2()
