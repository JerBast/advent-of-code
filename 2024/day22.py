from aocd import get_data


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
    sequences = {}
    for idx, secret in enumerate(DATA):
        w = []
        for _ in range(2000):
            new_secret = compute_next_secret(secret)
            w.append((new_secret % 10) - (secret % 10))
            if len(w) == 4:
                tw = tuple(w)
                if tw not in sequences:
                    sequences[tw] = [None] * len(DATA)
                if sequences[tw][idx] is None:
                    sequences[tuple(w)][idx] = new_secret % 10
                w.pop(0)
            secret = new_secret
    print(max(sum(e for e in v if e is not None) for v in sequences.values()))


if __name__ == '__main__':
    part1()
    part2()
