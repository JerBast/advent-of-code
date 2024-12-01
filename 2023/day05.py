import re

from aocd import get_data


data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split('\n\n')


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def overlaps(self, other) -> bool:
        assert type(other) == Range

        return (self.start <= other.start <= self.end) \
            or (self.start <= other.end <= self.end) \
            or (other.start <= self.start and self.end <= other.end)

    def __repr__(self) -> str:
        return f'[{self.start}, {self.end}]'


def extract_nums_to_array(s: str):
    return list(map(int, re.findall('\d+', s)))


def remove_overlap(ranges):
    if len(ranges) == 0:
        return []
    
    ranges = sorted(ranges, key=lambda r: r.start)
    new_ranges = [ranges[0]]

    for r in ranges[1:]:
        if new_ranges[-1].overlaps(r):
            new_ranges[-1] = new_ranges[-1].union(r)
        else:
            new_ranges.append(r)
    return new_ranges


data = get_data(year=2023, day=5).split('\n\n')
seeds = extract_nums_to_array(data[0])
seeds = [Range(s, s + e - 1) for s, e in zip(seeds[::2], seeds[1::2])]
seeds = remove_overlap(seeds)

maps = list(map(extract_nums_to_array, data[1:]))
maps = [sorted([(a, b, b + c - 1) for a, b, c in zip(m[::3], m[1::3], m[2::3])], key=lambda x:x[1]) for m in maps]

ranges = seeds
for m in maps:
    new_ranges = []

    for r in ranges:
        seps = []
        eval_r = Range(r.start, r.end)

        for (d_start, s_start, s_end) in m:
            diff = d_start - s_start

            # Check if start lies in map entry
            if s_start <= eval_r.start <= s_end:
                # Check if end lies in map entry
                if s_start <= eval_r.end <= s_end:
                    # Subsumed by range, full map
                    # seps.append(Range(eval_r.start, eval_r.end)) # TODO: Correct to destination
                    seps.append(Range(eval_r.start + diff, eval_r.end + diff))

                    # No more eval to do
                    eval_r = None
                    break
                else:
                    # Partially in range, there is a leftover
                    # seps.append(Range(eval_r.start, s_end))  # TODO: Correct to destination
                    seps.append(Range(eval_r.start + diff, s_end + diff))
                    eval_r = Range(s_end + 1, eval_r.end)
            # Check if end lies in map entry
            elif s_start <= eval_r.end <= s_end:
                # Start cannot lay here, we already checked
                assert eval_r.start < s_start
                
                # Partially in range
                # seps.append(Range(s_start, eval_r.end))                    # TODO: Correct to destination
                seps.append(Range(s_start + diff, eval_r.end + diff))
                eval_r = Range(eval_r.start, s_start - 1)

                # Ranges are sorted so we must break
                break

        # Part of range that could not be mapped should remain unmapped
        if not (eval_r is None):
            seps.append(eval_r)

        # Add all separations to the new ranges list
        new_ranges += seps

    # Remove all overlap between the ranges
    ranges = remove_overlap(new_ranges)

print(min(map(lambda r: r.start, ranges)))  
