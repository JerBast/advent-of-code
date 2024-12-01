from aocd import get_data

from math import prod
from copy import deepcopy


data = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
data = get_data(year=2023, day=19)
filters_inp, points_inp = data.split("\n\n")


filters = {}
for filter_inp in filters_inp.split("\n"):
    key, value = filter_inp.split("{")
    filters[key] = value[:-1].split(",")


def part2(current: str, ranges: dict[str, tuple[int, int]]):
    # Too bad, unaccepted state
    if current == "R":
        return 0

    # Accepting state, multiply all possibilities
    if current == "A":
        return prod(stop - start + 1 for (start, stop) in ranges.values())

    # Keep track of result
    res = 0
    ranges_cpy = deepcopy(ranges)

    # Apply filters to current ranges
    for f in filters[current][:-1]:
        cond, target = f.split(":")
        if ">" in cond:
            label, val = cond.split(">")
            val = int(val)

            rsc = deepcopy(ranges_cpy)
            start, stop = rsc[label]
            rsc[label] = (max(start, val + 1), stop)
            res += part2(target, rsc)

            start, stop = ranges_cpy[label]
            ranges_cpy[label] = (start, min(stop, val))
        else:
            label, val = cond.split("<")
            val = int(val)

            rsc = deepcopy(ranges_cpy)
            start, stop = rsc[label]
            rsc[label] = (start, min(stop, val - 1))
            res += part2(target, rsc)

            start, stop = ranges_cpy[label]
            ranges_cpy[label] = (max(start, val), stop)

    return res + part2(filters[current][-1], ranges_cpy)


print(part2("in", {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}))
