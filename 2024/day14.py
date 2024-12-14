import re
import math

from aocd import get_data


DATA = get_data(year=2024, day=14).splitlines()

W = 0
H = 0
ROBOTS: list[tuple[int, int, int, int]] = []
for row in DATA:
    p_x, p_y, v_x, v_y = map(int, re.findall(r'-?\d+', row))
    ROBOTS.append((p_x, p_y, v_x, v_y))
    W = max(W, p_x + 1)
    H = max(H, p_y + 1)


def part1():
    robots = ROBOTS.copy()
    for _ in range(100):
        for idx, robot in enumerate(robots):
            p_x, p_y, v_x, v_y = robot
            p_x = (p_x + v_x + W) % W
            p_y = (p_y + v_y + H) % H
            robots[idx] = (p_x, p_y, v_x, v_y)

    qs = [0, 0, 0, 0]
    wm = (W - 1) // 2
    hm = (H - 1) // 2
    for robot in robots:
        p_x, p_y, _, _ = robot
        if p_x < wm and p_y < hm:
            qs[0] += 1
        elif p_x > wm and p_y < hm:
            qs[1] += 1
        elif p_x < wm and p_y > hm:
            qs[2] += 1
        elif p_x > wm and p_y > hm:
            qs[3] += 1
    print(math.prod(qs))


def max_cluster_size(robots: list[tuple[int, int, int, int]]) -> int:
    robots = set((x, y) for x, y, _, _ in robots)
    visited = set()

    max_cluster_size = 0
    for x, y in robots:
        if (x, y) in visited:
            continue

        cluster_size = 0
        queue = [(x, y)]
        while len(queue) > 0:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue

            cluster_size += 1
            visited.add((x, y))
            if (x + 1, y) in robots:
                queue.append((x + 1, y))
            if (x - 1, y) in robots:
                queue.append((x - 1, y))
            if (x, y + 1) in robots:
                queue.append((x, y + 1))
            if (x, y - 1) in robots:
                queue.append((x, y - 1))

        max_cluster_size = max(max_cluster_size, cluster_size)
    return max_cluster_size


def part2():
    elapsed = 0
    robots = ROBOTS.copy()
    min_aligned_robots = len(robots) // 3
    while max_cluster_size(robots) < min_aligned_robots:
        for idx, robot in enumerate(robots):
            p_x, p_y, v_x, v_y = robot
            p_x = (p_x + v_x + W) % W
            p_y = (p_y + v_y + H) % H
            robots[idx] = (p_x, p_y, v_x, v_y)
        elapsed += 1
    print(elapsed)


if __name__ == '__main__':
    part1()
    part2()
