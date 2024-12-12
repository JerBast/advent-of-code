import numpy as np

from aocd import get_data


DATA = get_data(year=2024, day=12)
DATA = np.array([np.array(list(row)) for row in DATA.splitlines()])


def find_neighbours(matrix: np.ndarray, x: int, y: int) -> list[tuple[int, int]]:
    visited = set()
    queue = [(x, y)]

    while len(queue) > 0:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue

        visited.add((x, y))
        if x > 0 and matrix[y][x] == matrix[y][x - 1]:
            queue.append((x - 1, y))
        if y > 0 and matrix[y][x] == matrix[y - 1][x]:
            queue.append((x, y - 1))
        if x < matrix.shape[1] - 1 and matrix[y][x] == matrix[y][x + 1]:
            queue.append((x + 1, y))
        if y < matrix.shape[0] - 1 and matrix[y][x] == matrix[y + 1][x]:
            queue.append((x, y + 1))

    return list(visited)


def find_clusters(matrix: np.ndarray) -> list[list[tuple[int, int]]]:
    clusters = []
    visited = np.zeros(matrix.shape)
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if visited[y][x]:
                continue

            nbs = find_neighbours(matrix, x, y)
            for nb_x, nb_y in nbs:
                visited[nb_y][nb_x] = 1

            clusters.append(nbs)
    return clusters


def perimeter(cluster: list[int]) -> int:
    area = 0
    for x, y in cluster:
        area += 4 - (
            ((x - 1, y) in cluster) +
            ((x, y - 1) in cluster) +
            ((x + 1, y) in cluster) +
            ((x, y + 1) in cluster)
        )
    return area


def discount_perimeter(cluster: list[int]) -> int:
    area = 0
    for x, y in cluster:
        # Corners from appendices
        if (x - 1, y) not in cluster and (x, y + 1) not in cluster:
            area += 1
        if (x + 1, y) not in cluster and (x, y - 1) not in cluster:
            area += 1
        if (x - 1, y) not in cluster and (x, y - 1) not in cluster:
            area += 1
        if (x + 1, y) not in cluster and (x, y + 1) not in cluster:
            area += 1

        # Corners from groups of three
        if (x - 1, y) in cluster and (x, y + 1) in cluster and (x - 1, y + 1) not in cluster:
            area += 1
        if (x + 1, y) in cluster and (x, y - 1) in cluster and (x + 1, y - 1) not in cluster:
            area += 1
        if (x - 1, y) in cluster and (x, y - 1) in cluster and (x - 1, y - 1) not in cluster:
            area += 1
        if (x + 1, y) in cluster and (x, y + 1) in cluster and (x + 1, y + 1) not in cluster:
            area += 1
    return area


def part1():
    print(sum(len(cluster) * perimeter(cluster)
          for cluster in find_clusters(DATA)))


def part2():
    print(sum(len(cluster) * discount_perimeter(cluster)
          for cluster in find_clusters(DATA)))


if __name__ == '__main__':
    part1()
    part2()
