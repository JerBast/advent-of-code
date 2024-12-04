import re
import math

from aocd import get_data


DATA = get_data(year=2024, day=3)


def part1():
    matches = re.findall(r'mul\((\d{1,3},\d{1,3})\)', DATA)
    print(sum(math.prod(map(int, match.split(','))) for match in matches))


def part2():
    matches = [(m.group(1), m.start()) for m in re.finditer(r'mul\((\d{1,3},\d{1,3})\)', DATA)]
    ignored = [(m.group(1) == 'don\'t', m.start()) for m in re.finditer(r'(do|don\'t)\(\)', DATA)]

    ans = 0
    enabled = True
    match_idx = 0
    for disable, idx in ignored:
        while match_idx < len(matches) and matches[match_idx][1] < idx:
            if enabled:
                ans += math.prod(map(int, matches[match_idx][0].split(',')))
            match_idx += 1
        enabled = not disable
    
    while match_idx < len(matches) and enabled:
        ans += math.prod(map(int, matches[match_idx][0].split(',')))
        match_idx += 1
    
    print(ans)

if __name__ == '__main__':
    part1()
    part2()
