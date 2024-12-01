from __future__ import annotations

from aocd import get_data
from shapely.geometry.polygon import Polygon


class Node:
    def __init__(self, pos: tuple[int, int], val: str):
        self.pos: tuple[int, int] = pos
        self.val: str = val
        self.nodes: set[Node] = set()


data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
data = get_data(year=2023, day=10)

node_grid: dict[tuple[int, int], Node] = {}
for y, row in enumerate(data.split("\n")):
    for x, val in enumerate(row):
        if val != ".":
            node_grid[(x, y)] = Node((x, y), val)


def add_if_present(node: Node, pos: tuple[int, int]):
    if pos not in node_grid:
        return
    
    target = node_grid[pos]
    s_x, s_y = node.pos
    x, y = pos
    if (
        (s_x + 1 == x and target.val in "-J7")
        or (s_x - 1 == x and target.val in "-LF")
        or (s_y + 1 == y and target.val in "|LJ")
        or (s_y - 1 == y and target.val in "|F7")
    ):
        node.nodes.add(target)


start_node = None
for (x, y), node in node_grid.items():
    if node.val == "|":
        add_if_present(node, (x, y + 1))
        add_if_present(node, (x, y - 1))
    elif node.val == "-":
        add_if_present(node, (x + 1, y))
        add_if_present(node, (x - 1, y))
    elif node.val == "L":
        add_if_present(node, (x, y - 1))
        add_if_present(node, (x + 1, y))
    elif node.val == "J":
        add_if_present(node, (x, y - 1))
        add_if_present(node, (x - 1, y))
    elif node.val == "7":
        add_if_present(node, (x, y + 1))
        add_if_present(node, (x - 1, y))
    elif node.val == "F":
        add_if_present(node, (x, y + 1))
        add_if_present(node, (x + 1, y))
    elif node.val == "S":
        add_if_present(node, (x, y + 1))
        add_if_present(node, (x, y - 1))
        add_if_present(node, (x + 1, y))
        add_if_present(node, (x - 1, y))
        start_node = node
    else:
        raise RuntimeError("Invalid value encountered in node grid")


# Part 1
visited: set[Node] = set()
ordered: list[Node] = []
current = start_node
while current is not None and current not in visited:
    ordered.append(current)
    visited.add(current)
    current = next((n for n in current.nodes if not n in visited), None)
print(len(visited) // 2)

# Part 2
polygon = Polygon(n.pos for n in ordered)
print(polygon.area - len(visited) // 2 + 1)
