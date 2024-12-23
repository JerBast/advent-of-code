from aocd import get_data
from collections import defaultdict


DATA = get_data(year=2024, day=23).splitlines()
LINKS = defaultdict(set)

for link in DATA:
    l, r = link.split('-')
    LINKS[l].add(r)
    LINKS[r].add(l)


def part1():
    unique_sets = set()
    for a, avs in LINKS.items():
        if a[0] != 't':
            continue
        for b in avs:
            for c in LINKS[b]:
                if a in LINKS[c]:
                    unique_sets.add(tuple(sorted([a, b, c])))
    print(len(unique_sets))


def part2():
    def is_interconnected(group: set[str]) -> bool:
        return all(len(group) == len(LINKS[c].intersection(group)) + 1 for c in group)

    mx_group = set()
    for a, ls in LINKS.items():
        res = {a}
        for l in ls:
            if is_interconnected(res.union({l})):
                res.add(l)
        if len(res) > len(mx_group):
            mx_group = res
    print(*sorted(mx_group), sep=',')


if __name__ == '__main__':
    part1()
    part2()
