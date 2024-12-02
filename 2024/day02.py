from aocd import get_data


DATA = get_data(year=2024, day=2).splitlines()
REPORTS = [list(map(int, report.split())) for report in DATA]


def is_safe(report):
    return all(1 <= j - i <= 3 for i, j in zip(report, report[1:])) \
        or all(1 <= i - j <= 3 for i, j in zip(report, report[1:]))


def part1():
    print(sum(map(is_safe, REPORTS)))


def part2():
    print(sum(any(is_safe(report[:i] + report[i+1:])
          for i in range(len(report))) for report in REPORTS))


if __name__ == '__main__':
    part1()
    part2()
