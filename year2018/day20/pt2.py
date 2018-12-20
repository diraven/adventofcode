"""
--- Part Two ---

Okay, so the facility is big.

How many rooms have a shortest path from your current location that pass through at least 1000 doors?
"""
from collections import namedtuple

import networkx as nx

Node = namedtuple('Node', ('x', 'y'))
Direction = Node

DIRECTIONS = {
    'N': Direction(0, 1),
    'E': Direction(1, 0),
    'S': Direction(0, -1),
    'W': Direction(-1, 0),
}


def step(node: Node, direction: Direction):
    return Node(node.x + direction.x, node.y + direction.y)


def build_graph(g: nx.Graph, start: Node, data: str, offset: int = 0):
    current_node = start

    while offset < len(data):
        char = data[offset]
        offset += 1
        if char in ('(', '^'):
            current_node, offset = build_graph(g, current_node, data, offset)
        elif char == "|":
            current_node = start
        elif char in (')', '$'):
            return current_node, offset
        else:
            new_node = step(current_node, DIRECTIONS[char])
            g.add_node(new_node)
            g.add_edge(current_node, new_node)
            current_node = new_node

    return current_node, offset


with open('./input.txt') as f:
    # Load data.
    data = f.read().strip()

    g = nx.Graph()
    start = Node(0, 0)
    g.add_node(start)

    build_graph(g, start, data)
    longer_then_1k_count = 0
    for i, node in enumerate(g.nodes):
        if len(nx.astar_path(g, start, node)) > 1000:
            longer_then_1k_count += 1
    print(longer_then_1k_count)
