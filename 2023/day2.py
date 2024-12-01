from math import prod
from aocd import get_data


data = get_data(year=2023, day=2).splitlines()
games = {}

for idx, line in enumerate(data):
    sets = []
    for st in line.split(': ')[1].split(';'):
        cubes = {}
        for cube in st.split(', '):
            amount, type = cube.split()
            cubes[type] = int(amount)
        sets.append(cubes)
    games[idx + 1] = sets


def part1():
    limits = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    cnt = 0
    for id, game in games.items():
        possible = True
        for cubes in game:
            for k, v in cubes.items():
                if v > limits[k]:
                    possible = False
        if possible:
            cnt += id
    print(cnt)


def part2():
    cnt = 0
    for _, game in games.items():
        minima = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for cubes in game:
            for k, v in cubes.items():
                minima[k] = max(v, minima[k])
        cnt += prod(minima.values())
    print(cnt)


part1()
part2()
