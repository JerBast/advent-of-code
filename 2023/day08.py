from __future__ import annotations

from math import lcm
from aocd import get_data


class Node:
    def __init__(self, key: str, left: Node = None, right: Node = None):
        self.key = key
        self.left = left
        self.right = right


data = get_data(year=2023, day=8)
directions, entries = data.split('\n\n')
directions_len = len(directions)

# Construct nodes
nodes: dict[str, Node] = {}
for entry in entries.split('\n'):
    node, _ = entry.split(' = ')
    nodes[node] = Node(node)
for entry in entries.split('\n'):
    node, pointers = entry.split(' = ')
    left, right = pointers[1:-1].split(', ')
    nodes[node].left = nodes[left]
    nodes[node].right = nodes[right]


# Path finding
def find_path(current: Node, is_finished):
    idx = 0
    while not is_finished(current):
        direction = directions[idx % directions_len]
        if direction == 'L':
            current = current.left
        else:
            current = current.right
        idx += 1
    return idx


# Part 1
print(find_path(nodes['AAA'], lambda n: n.key == 'ZZZ'))

# Part 2
indices = [find_path(node, lambda n: n.key.endswith('Z')) for node in nodes.values() if node.key.endswith('A')]
print(lcm(*indices))
