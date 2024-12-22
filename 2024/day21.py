from aocd import get_data


DATA = get_data(year=2024, day=21).splitlines()
N_LOCS = {
    'A': (2, 3),
    '0': (1, 3),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
}
D_LOCS = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1)
}
MEM = {}


def travel_n(c: str, t: str) -> str:
    cx, cy = N_LOCS[c]
    tx, ty = N_LOCS[t]
    r = '>' * max(0, tx - cx)
    d = 'v' * max(0, ty - cy)
    u = '^' * max(0, cy - ty)
    l = '<' * max(0, cx - tx)
    return (l + u if cy < 3 or tx > 0 else u + l) + (d + r if ty < 3 or cx > 0 else r + d)


def travel_d(c: str, t: str) -> str:
    cx, cy = D_LOCS[c]
    tx, ty = D_LOCS[t]
    r = '>' * max(0, tx - cx)
    d = 'v' * max(0, ty - cy)
    u = '^' * max(0, cy - ty)
    l = '<' * max(0, cx - tx)
    return (l + d if tx > 0 or cy > 0 else d + l) + (u + r if cx > 0 else r + u)


def path_d_rec(s: str, depth: int) -> int:
    if depth == 0:
        return len(s)
    length = 0
    c = 'A'
    for t in s:
        if (c, t, depth) in MEM:
            length += MEM[(c, t, depth)]
        else:
            sub_length = path_d_rec(travel_d(c, t) + 'A', depth - 1)
            MEM[(c, t, depth)] = sub_length
            length += sub_length
        c = t
    return length


def path_n(s: str) -> str:
    path = ''
    c = 'A'
    for t in s:
        path += travel_n(c, t) + 'A'
        c = t
    return path


def part1():
    ans = 0
    for c in DATA:
        ans += int(c[:-1]) * path_d_rec(path_n(c), 2)
    print(ans)


def part2():
    ans = 0
    for c in DATA:
        ans += int(c[:-1]) * path_d_rec(path_n(c), 25)
    print(ans)


if __name__ == '__main__':
    part1()
    part2()
