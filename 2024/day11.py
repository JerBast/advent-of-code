from aocd import get_data


DATA = get_data(year=2024, day=11)
DATA = list(map(int, DATA.split()))
PREV = {}


def impl(stone: int, remaining_blinks: int) -> int:
    if (stone, remaining_blinks) in PREV:
        return PREV[(stone, remaining_blinks)]

    res = 0
    s = str(stone)
    if remaining_blinks == 0:
        res = 1
    elif stone == 0:
        res = impl(1, remaining_blinks - 1)
    elif len(s) % 2 == 0:
        res = impl(int(s[:len(s)//2]), remaining_blinks - 1) + \
            impl(int(s[len(s)//2:]), remaining_blinks - 1)
    else:
        res = impl(stone * 2024, remaining_blinks - 1)

    PREV[(stone, remaining_blinks)] = res
    return res


def part1():
    print(sum(impl(stone, 25) for stone in DATA))


def part2():
    print(sum(impl(stone, 75) for stone in DATA))


if __name__ == '__main__':
    part1()
    part2()
