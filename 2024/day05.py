from collections import defaultdict

from aocd import get_data


DATA = get_data(year=2024, day=5).split('\n\n')
UPDATES = [list(map(int, update.split(',')))
           for update in DATA[1].splitlines()]

ORDERING = defaultdict(set)
for order in DATA[0].splitlines():
    l, r = map(int, order.split('|'))
    ORDERING[l].add(r)


def is_update_valid(update: list[int]) -> bool:
    printed = set()
    for page in update:
        if not ORDERING[page].isdisjoint(printed):
            return False
        printed.add(page)
    return True


def solve_order(update: set[int]) -> list[int]:
    fixed = []
    while len(update) > 0:
        mx = -1
        mp = -1
        for page in update:
            v = len(ORDERING[page].intersection(update))
            if v > mx:
                mx = v
                mp = page

        fixed.append(mp)
        update.remove(mp)
    return fixed


def part1():
    print(sum(update[len(update) // 2]
          for update in UPDATES if is_update_valid(update)))


def part2():
    print(sum(solve_order(set(update))[len(update) // 2]
          for update in UPDATES if not is_update_valid(update)))


if __name__ == '__main__':
    part1()
    part2()
