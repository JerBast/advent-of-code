import sys
import heapq

import numpy as np

from enum import Enum
from collections import defaultdict

from aocd import get_data


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def shortest_path(data: np.array):
    # Construct visited nodes and queue objects
    visited: set[tuple[int, int, Direction]] = set()
    queue: list[tuple[int, tuple[int, int, Direction]]] = []
    distances = defaultdict(lambda: sys.maxsize)

    # Insert the starting point with both directions included
    heapq.heappush(queue, (0, (0, 0, Direction.RIGHT)))
    heapq.heappush(queue, (0, (0, 0, Direction.DOWN)))

    # Run while queue is not empty
    while queue:
        # Extract item from queue
        u: tuple[int, tuple[int, int, Direction]] = heapq.heappop(queue)
        dist, value = u

        # Continue if value was already visited, if not, mark visited
        if value in visited: continue
        visited.add(value)

        # Extract values from tuple
        x, y, direction = value

        # Go over each neighbour in the appropriate direction(s)
        if direction == Direction.UP:
            cum_dist = dist
            for i in range(y - 1, max(y - 4, -1), -1):
                cum_dist += data[i, x]
                left = (x, i, Direction.LEFT)
                right = (x, i, Direction.RIGHT)

                if cum_dist < distances[left]:
                    distances[left] = cum_dist
                    heapq.heappush(queue, (cum_dist, left))
                if cum_dist < distances[right]:
                    distances[right] = cum_dist
                    heapq.heappush(queue, (cum_dist, right))
        elif direction == Direction.DOWN:
            cum_dist = dist
            for i in range(y + 1, min(y + 4, data.shape[0])):
                cum_dist += data[i, x]
                left = (x, i, Direction.LEFT)
                right = (x, i, Direction.RIGHT)
                
                if cum_dist < distances[left]:
                    distances[left] = cum_dist
                    heapq.heappush(queue, (cum_dist, left))
                if cum_dist < distances[right]:
                    distances[right] = cum_dist
                    heapq.heappush(queue, (cum_dist, right))
        elif direction == Direction.LEFT:
            cum_dist = dist

            for i in range(x - 1, max(x - 4, -1), -1):
                cum_dist += data[y, i]
                up = (i, y, Direction.UP)
                down = (i, y, Direction.DOWN)

                if cum_dist < distances[up]:
                    distances[up] = cum_dist
                    heapq.heappush(queue, (cum_dist, up))
                if cum_dist < distances[down]:
                    distances[down] = cum_dist
                    heapq.heappush(queue, (cum_dist, down))
        else:
            cum_dist = dist
            for i in range(x + 1, min(x + 4, data.shape[1])):
                cum_dist += data[y, i]
                up = (i, y, Direction.UP)
                down = (i, y, Direction.DOWN)
                
                if cum_dist < distances[up]:
                    distances[up] = cum_dist
                    heapq.heappush(queue, (cum_dist, up))
                if cum_dist < distances[down]:
                    distances[down] = cum_dist
                    heapq.heappush(queue, (cum_dist, down))

    # Return the shortest path towards the end
    y_mx, x_mx = data.shape
    return min(distances[(x_mx - 1, y_mx - 1, Direction.DOWN)], distances[(x_mx - 1, y_mx - 1, Direction.RIGHT)])


def shortest_path2(data: np.array):
    # Construct visited nodes and queue objects
    visited: set[tuple[int, int, Direction]] = set()
    queue: list[tuple[int, tuple[int, int, Direction]]] = []
    distances = defaultdict(lambda: sys.maxsize)

    # Insert the starting point with both directions included
    heapq.heappush(queue, (0, (0, 0, Direction.RIGHT)))
    heapq.heappush(queue, (0, (0, 0, Direction.DOWN)))

    # Run while queue is not empty
    while queue:
        # Extract item from queue
        u: tuple[int, tuple[int, int, Direction]] = heapq.heappop(queue)
        dist, value = u

        # Continue if value was already visited, if not, mark visited
        if value in visited: continue
        visited.add(value)

        # Extract values from tuple
        x, y, direction = value

        # Go over each neighbour in the appropriate direction(s)
        if direction == Direction.UP:
            cum_dist = dist
            for i in range(y - 1, max(y - 4, -1), -1):
                cum_dist += data[i, x]

            for i in range(y - 4, max(y - 11, -1), -1):
                cum_dist += data[i, x]
                left = (x, i, Direction.LEFT)
                right = (x, i, Direction.RIGHT)

                if cum_dist < distances[left]:
                    distances[left] = cum_dist
                    heapq.heappush(queue, (cum_dist, left))
                if cum_dist < distances[right]:
                    distances[right] = cum_dist
                    heapq.heappush(queue, (cum_dist, right))
        elif direction == Direction.DOWN:
            cum_dist = dist
            for i in range(y + 1, min(y + 4, data.shape[0])):
                cum_dist += data[i, x]

            for i in range(y + 4, min(y + 11, data.shape[0])):
                cum_dist += data[i, x]
                left = (x, i, Direction.LEFT)
                right = (x, i, Direction.RIGHT)
                
                if cum_dist < distances[left]:
                    distances[left] = cum_dist
                    heapq.heappush(queue, (cum_dist, left))
                if cum_dist < distances[right]:
                    distances[right] = cum_dist
                    heapq.heappush(queue, (cum_dist, right))
        elif direction == Direction.LEFT:
            cum_dist = dist
            for i in range(x - 1, max(x - 4, -1), -1):
                cum_dist += data[y, i]

            for i in range(x - 4, max(x - 11, -1), -1):
                cum_dist += data[y, i]
                up = (i, y, Direction.UP)
                down = (i, y, Direction.DOWN)

                if cum_dist < distances[up]:
                    distances[up] = cum_dist
                    heapq.heappush(queue, (cum_dist, up))
                if cum_dist < distances[down]:
                    distances[down] = cum_dist
                    heapq.heappush(queue, (cum_dist, down))
        else:
            cum_dist = dist
            for i in range(x + 1, min(x + 4, data.shape[1])):
                cum_dist += data[y, i]

            for i in range(x + 4, min(x + 11, data.shape[1])):
                cum_dist += data[y, i]
                up = (i, y, Direction.UP)
                down = (i, y, Direction.DOWN)
                
                if cum_dist < distances[up]:
                    distances[up] = cum_dist
                    heapq.heappush(queue, (cum_dist, up))
                if cum_dist < distances[down]:
                    distances[down] = cum_dist
                    heapq.heappush(queue, (cum_dist, down))

    # Return the shortest path towards the end
    y_mx, x_mx = data.shape
    # pprint(distances)
    return min(distances[(x_mx - 1, y_mx - 1, Direction.DOWN)], distances[(x_mx - 1, y_mx - 1, Direction.RIGHT)])


data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
data = get_data(year=2023, day=17)
data = np.array([list(map(int, row)) for row in data.split('\n')])

# Part 1
print(shortest_path(data))

# Part 2
print(shortest_path2(data))
