from aocd import get_data


DATA = get_data(year=2024, day=7).splitlines()
TARGETS = {}
for row in DATA:
    target, numbers = row.split(': ')
    TARGETS[int(target)] = list(map(int, numbers.split()))


def is_valid_p1(t: int, nrs: list[int]) -> bool:
    if t == 0 and len(nrs) == 0:
        return True
    if t < 0 or len(nrs) == 0:
        return False

    ans, nrs = nrs[-1], nrs[:-1]

    return is_valid_p1(t - ans, nrs) \
        or (t % ans == 0 and is_valid_p1(t // ans, nrs))


def is_valid_p2(t: int, nrs: list[int]) -> bool:
    if t == 0 and len(nrs) == 0:
        return True
    if t < 0 or len(nrs) == 0:
        return False

    ans, nrs = nrs[-1], nrs[:-1]
    t_s, ans_s = str(t), str(ans)

    return is_valid_p2(t - ans, nrs) \
        or (t % ans == 0 and is_valid_p2(t // ans, nrs)) \
        or (t_s.endswith(ans_s) and is_valid_p2(int(t_s.removesuffix(ans_s)), nrs))


def part1():
    print(sum(t for t, nrs in TARGETS.items() if is_valid_p1(t, nrs)))


def part2():
    print(sum(t for t, nrs in TARGETS.items() if is_valid_p2(t, nrs)))


if __name__ == '__main__':
    part1()
    part2()
