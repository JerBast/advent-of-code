from aocd import get_data


DATA = get_data(year=2024, day=9)


def get_disk() -> list[tuple[int, int]]:
    return [(int(v), i // 2 if i % 2 == 0 else -1) for i, v in enumerate(DATA) if int(v) > 0]


def checksum(disk: list[tuple[int, int]]) -> int:
    c = 0
    i = 0
    for cnt, val in disk:
        if val != -1:
            c += val * (cnt * i + (cnt * (cnt - 1) // 2))
        i += cnt
    return c


def part1():
    disk = get_disk()

    i = 0
    j = len(disk) - 1
    while i < j:
        if disk[i][1] == -1:
            free = disk[i]
            file = disk[j]
            if free[0] == file[0]:
                # Replace empty space with file
                disk[i], disk[j] = file, free
            elif disk[i][0] > disk[j][0]:
                # Fill empty space with file and keep remainder
                disk[i] = (free[0] - file[0], -1)
                disk[j] = (file[0], -1)
                disk.insert(i, file)
            else:
                # Fill available space with file
                disk[i] = (free[0], file[1])
                disk[j] = (file[0] - free[0], file[1])

        while disk[j][1] == -1 and i < j:
            j -= 1
        while disk[i][1] != -1 and i < j:
            i += 1

    print(checksum(disk))


def part2():
    disk = get_disk()

    def find_file_idx(id): return next(
        i for i, v in enumerate(disk) if v[1] == id)

    def next_free_idx(begin, end, min_sz): return next(
        (begin + i for i, v in enumerate(disk[begin:end]) if v[1] == -1 and v[0] >= min_sz), None)

    file_idx = (len(DATA) - 1) // 2
    while file_idx >= 0:
        j = find_file_idx(file_idx)
        file = disk[j]

        i = next_free_idx(0, j, file[0])
        if i is not None:
            free = disk[i]
            if free[0] == file[0]:
                # Replace empty space with file
                disk[i], disk[j] = file, free
            else:
                # Fill empty space with file and keep remainder
                disk[i] = (free[0] - file[0], -1)
                disk[j] = (file[0], -1)
                disk.insert(i, file)
        file_idx -= 1

    print(checksum(disk))


if __name__ == '__main__':
    part1()
    part2()
