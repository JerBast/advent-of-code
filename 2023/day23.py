import sys
import heapq
from pprint import pprint

from collections import defaultdict

from aocd import get_data

sys.setrecursionlimit(2500)


data = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
# data = get_data(year=2023, day=23)
data = data.split("\n")

h, w = len(data), len(data[0])

s_x, s_y = data[0].index("."), 0
e_x, e_y = data[-1].index("."), h - 1


def inefficient(data: list[str], current: tuple[int, int], end: tuple[int, int], visited: set[tuple[int, int]]) -> int:
    if current == end: return 0
    if current in visited: return -sys.maxsize
    visited.add(current)

    x, y = current
    c = data[y][x]
    if c == '#': return -sys.maxsize

    if c == '>':
        return 1 + inefficient(data, (x + 1, y), end, visited)
    if c == '<':
        return 1 + inefficient(data, (x - 1, y), end, visited)
    if c == 'v':
        return 1 + inefficient(data, (x, y + 1), end, visited)
    if c == '^':
        return 1 + inefficient(data, (x, y - 1), end, visited)
    
    return 1 + max(inefficient(data, (x + 1, y), end, visited.copy()), inefficient(data, (x - 1, y), end, visited.copy()), inefficient(data, (x, y + 1), end, visited.copy()), inefficient(data, (x, y - 1), end, visited.copy()))


def inefficient2(data: list[str], current: tuple[int, int], end: tuple[int, int], visited: set[tuple[int, int]]) -> int:
    if current == end: return 0
    if current in visited: return -sys.maxsize
    visited.add(current)

    x, y = current
    c = data[y][x]
    if c == '#': return -sys.maxsize
    
    return 1 + max(inefficient2(data, (x + 1, y), end, visited.copy()), inefficient2(data, (x - 1, y), end, visited.copy()), inefficient2(data, (x, y + 1), end, visited.copy()), inefficient2(data, (x, y - 1), end, visited.copy()))


def longest_path(data: list[str], start: tuple[int, int], end: tuple[int, int]) -> int:
    # Construct visited nodes and queue objects
    visited: set[tuple[int, int]] = set()
    queue: list[tuple[int, tuple[int, int]]] = []
    distances = defaultdict(lambda: sys.maxsize)
    prev = {}

    # Insert the starting point
    heapq.heappush(queue, (0, start))

    # Run while queue is not empty
    while queue:
        # Extract point from queue (including cost)
        cost, point = heapq.heappop(queue)

        # Continue if already visited, if not, mark visited
        if point in visited: continue
        visited.add(point)

        # Go over all valid neighbours
        x, y = point

        t_x, t_y, t_p = x - 1, y, (x - 1, y)
        if t_x >= 0 and data[t_y][t_x] != '#' and data[y][x] in '<.' and data[t_y][t_x] not in '>':
            if cost - 1 < distances[t_p]:
                distances[t_p] = cost - 1
                if t_p not in visited:
                    prev[t_p] = point
                    heapq.heappush(queue, (cost - 1, t_p))
        
        t_x, t_y, t_p = x, y - 1, (x, y - 1)
        if t_y >= 0 and data[t_y][t_x] != '#' and data[y][x] in '^.' and data[t_y][t_x] not in 'v':
            if cost - 1 < distances[t_p]:
                distances[t_p] = cost - 1
                if t_p not in visited:
                    prev[t_p] = point
                    heapq.heappush(queue, (cost - 1, t_p))
        
        t_x, t_y, t_p = x + 1, y, (x + 1, y)
        if t_x < w and data[t_y][t_x] != '#' and data[y][x] in '>.' and data[t_y][t_x] not in '<':
            if cost - 1 < distances[t_p]:
                distances[t_p] = cost - 1
                if t_p not in visited:
                    prev[t_p] = point
                    heapq.heappush(queue, (cost - 1, t_p))
        
        t_x, t_y, t_p = x, y + 1, (x, y + 1)
        if t_y < h and data[t_y][t_x] != '#' and data[y][x] in 'v.' and data[t_y][t_x] not in '^':
            if cost - 1 < distances[t_p]:
                distances[t_p] = cost - 1
                if t_p not in visited:
                    prev[t_p] = point
                    heapq.heappush(queue, (cost - 1, t_p))

    # Return distance
    pprint(prev)
    curr = end
    dop = [list(row) for row in data]
    while curr != start:
        x, y = curr
        dop[y][x] = 'O'
        curr = prev[curr]
    print(*[''.join(r) for r in dop], sep='\n')
    return distances[end]


# print(longest_path(data, (s_x, s_y), (e_x, e_y)))
# print(inefficient(data, (s_x, s_y), (e_x, e_y), set()))
print(inefficient2(data, (s_x, s_y), (e_x, e_y), set()))

# class Direction(Enum):
#     UP = 0
#     DOWN = 1
#     LEFT = 2
#     RIGHT = 3

#     def __lt__(self, other):
#         if self.__class__ is other.__class__:
#             return self.value < other.value
#         return NotImplemented


# def shortest_path(data: np.array):
#     # Construct visited nodes and queue objects
#     visited: set[tuple[int, int, Direction]] = set()
#     queue: list[tuple[int, tuple[int, int, Direction]]] = []
#     distances = defaultdict(lambda: sys.maxsize)

#     # Insert the starting point with both directions included
#     heapq.heappush(queue, (0, (0, 0, Direction.RIGHT)))
#     heapq.heappush(queue, (0, (0, 0, Direction.DOWN)))

#     # Run while queue is not empty
#     while queue:
#         # Extract item from queue
#         u: tuple[int, tuple[int, int, Direction]] = heapq.heappop(queue)
#         dist, value = u

#         # Continue if value was already visited, if not, mark visited
#         if value in visited: continue
#         visited.add(value)

#         # Extract values from tuple
#         x, y, direction = value

#         # Go over each neighbour in the appropriate direction(s)
#         if direction == Direction.UP:
#             cum_dist = dist
#             for i in range(y - 1, max(y - 4, -1), -1):
#                 cum_dist += data[i, x]
#                 left = (x, i, Direction.LEFT)
#                 right = (x, i, Direction.RIGHT)

#                 if cum_dist < distances[left]:
#                     distances[left] = cum_dist
#                     heapq.heappush(queue, (cum_dist, left))
#                 if cum_dist < distances[right]:
#                     distances[right] = cum_dist
#                     heapq.heappush(queue, (cum_dist, right))
#         elif direction == Direction.DOWN:
#             cum_dist = dist
#             for i in range(y + 1, min(y + 4, data.shape[0])):
#                 cum_dist += data[i, x]
#                 left = (x, i, Direction.LEFT)
#                 right = (x, i, Direction.RIGHT)

#                 if cum_dist < distances[left]:
#                     distances[left] = cum_dist
#                     heapq.heappush(queue, (cum_dist, left))
#                 if cum_dist < distances[right]:
#                     distances[right] = cum_dist
#                     heapq.heappush(queue, (cum_dist, right))
#         elif direction == Direction.LEFT:
#             cum_dist = dist

#             for i in range(x - 1, max(x - 4, -1), -1):
#                 cum_dist += data[y, i]
#                 up = (i, y, Direction.UP)
#                 down = (i, y, Direction.DOWN)

#                 if cum_dist < distances[up]:
#                     distances[up] = cum_dist
#                     heapq.heappush(queue, (cum_dist, up))
#                 if cum_dist < distances[down]:
#                     distances[down] = cum_dist
#                     heapq.heappush(queue, (cum_dist, down))
#         else:
#             cum_dist = dist
#             for i in range(x + 1, min(x + 4, data.shape[1])):
#                 cum_dist += data[y, i]
#                 up = (i, y, Direction.UP)
#                 down = (i, y, Direction.DOWN)

#                 if cum_dist < distances[up]:
#                     distances[up] = cum_dist
#                     heapq.heappush(queue, (cum_dist, up))
#                 if cum_dist < distances[down]:
#                     distances[down] = cum_dist
#                     heapq.heappush(queue, (cum_dist, down))

#     # Return the shortest path towards the end
#     y_mx, x_mx = data.shape
#     return min(distances[(x_mx - 1, y_mx - 1, Direction.DOWN)], distances[(x_mx - 1, y_mx - 1, Direction.RIGHT)])

# -4810 (low)
