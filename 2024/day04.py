import numpy as np

from aocd import get_data


DATA = get_data(year=2024, day=4).splitlines()


def part1():
    m = np.array([np.array([j for j in i]) for i in DATA])
    xmas = 0

    # Rows
    ps = [np.array([['X', 'M', 'A', 'S']]), np.array([['S', 'A', 'M', 'X']])]
    ws = np.lib.stride_tricks.sliding_window_view(m, ps[0].shape)
    xmas += sum(np.sum(np.count_nonzero(p == ws, axis=(2, 3)) == 4)
                for p in ps)

    # Cols
    ps = [np.array([['X'], ['M'], ['A'], ['S']]),
          np.array([['S'], ['A'], ['M'], ['X']])]
    ws = np.lib.stride_tricks.sliding_window_view(m, ps[0].shape)
    xmas += sum(np.sum(np.count_nonzero(p == ws, axis=(2, 3)) == 4)
                for p in ps)

    # Diagonals
    p = np.array([
        ['X', ' ', ' ', ' '],
        [' ', 'M', ' ', ' '],
        [' ', ' ', 'A', ' '],
        [' ', ' ', ' ', 'S']
    ])
    ps = [p, np.rot90(p), np.rot90(p, 2), np.rot90(p, 3)]
    ws = np.lib.stride_tricks.sliding_window_view(m, p.shape)
    xmas += sum(np.sum(np.count_nonzero(p == ws, axis=(2, 3)) == 4)
                for p in ps)

    print(xmas)


def part2():
    m = np.array([np.array([j for j in i]) for i in DATA])
    p = np.array([
        ['M', ' ', 'S'],
        [' ', 'A', ' '],
        ['M', ' ', 'S']
    ])
    ps = [p, np.rot90(p), np.rot90(p, 2), np.rot90(p, 3)]

    ws = np.lib.stride_tricks.sliding_window_view(m, p.shape)
    print(sum(np.sum(np.count_nonzero(p == ws, axis=(2, 3)) == 5) for p in ps))


if __name__ == '__main__':
    part1()
    part2()
