import re

from aocd import get_data


DATA = get_data(year=2024, day=19).split('\n\n')
TOWELS = DATA[1].splitlines()
PATTERNS = [p for p in DATA[0].split(', ')]


def part1():
    pattern = re.compile(f"({'|'.join(PATTERNS)})+")
    print(sum(pattern.fullmatch(t) is not None for t in TOWELS))


def part2():
    ans = 0
    for t in TOWELS:
        mem = [0] * (len(t) + 1)
        for i in range(1, len(t) + 1):
            for p in PATTERNS:
                if t[:i].endswith(p):
                    mem[i] += 1 if i == len(p) else mem[i - len(p)]
        ans += mem[len(t)]
    print(ans)


if __name__ == '__main__':
    part1()
    part2()
