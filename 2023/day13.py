import numpy as np

from aocd import get_data


def reflection_idx(data: np.array):
    for i in range(len(data)):
        if sum(c != d for l, m in zip(data[i-1::-1], data[i:]) for c, d in zip(l, m)) == 0: return i
        else: return 0


data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
data = get_data(year=2023, day=13)
# data = [np.array(list(map(list, block.split('\n')))) for block in data.split('\n\n')]
# print(sum(reflection_idx(block) * 100 + reflection_idx(block.T) for block in data))


# def reflection_idx(data: np.array):
#     for i in range(len(data)):
#         if sum(c != d for l, m in zip(data[i-1::-1], data[i:])
#                       for c, d in zip(l, m)) == 0: return i
#         else: return 0

# ps = list(map(str.split, data.split('\n\n')))

# def f(p):
#     for i in range(len(p)):
#         if sum(c != d for l,m in zip(p[i-1::-1], p[i:])
#                       for c,d in zip(l, m)) == s: return i
#     else: return 0

# for s in 0,1: print(sum(100 * f(p) + f([*zip(*p)]) for p in ps))


# P1: 35360
# P2: 36755

# from aocd import get_data


# def find_mirror(series: list[int]):
#     sz = len(series)
#     res = 0
#     for i in range(1, sz):
#         l = series[:i]
#         r = series[i:]
#         d = min(i, sz - i)
#         if l[i-d:] == r[:d][::-1]:
#             res = max(res, i) 
#     return res


# data = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#"""
# data = get_data(year=2023, day=13)
# data = data.split('\n\n')

# ans1 = 0
# ans2 = 0
# for chunk in data:
#     block = [list(row) for row in chunk.split('\n')]
#     rows = [''.join(row) for row in block]
#     cols = [''.join(row[i] for row in block) for i in range(len(block[0]))] 
    
#     mx1 = max(find_mirror(list(map(hash, rows))) * 100, find_mirror(list(map(hash, cols))))
#     ans1 += mx1

#     mx2 = 0
#     for y, row in enumerate(block):
#         for x, val in enumerate(row):
#             block[y][x] = '.' if val == '#' else '#'

#             rows = [''.join(row) for row in block]
#             cols = [''.join(row[i] for row in block) for i in range(len(block[0]))]

#             l, r = find_mirror(list(map(hash, rows))) * 100, find_mirror(list(map(hash, cols)))
#             if l == 0 or r == 0:
#                 mx2 = max(mx2, l, r)
#             # mx2 = max(mx2, find_mirror(list(map(hash, rows))) * 100, find_mirror(list(map(hash, cols))))

#             block[y][x] = val
    
#     ans2 += mx2

# print(ans1)
# print(ans2)

# # High: 59374
# # Low:  33954
# # Wrong: 46929
