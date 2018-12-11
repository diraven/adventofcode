"""
--- Part Two ---

The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

    Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which does not exist, and so the value of node C is 0.
    Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2 references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0, the value of node A is 33+33+0=66.

So, in this example, the value of the root node is 66.

What is the value of the root node?
"""
import timeit
from typing import List, Tuple


def parse_node(data: List[int]) -> Tuple[int, int]:
    """
    Returns (node_length, node_value).
    """
    child_nodes_count = data[0]
    metadata_entries_count = data[1]

    node_value = 0
    offset = 2

    if child_nodes_count > 0:
        node_values = []

        for i in range(child_nodes_count):
            node_length, sub_node_value = parse_node(data[offset:])
            offset += node_length

            node_values.append(sub_node_value)

        for i in range(metadata_entries_count):
            try:
                node_value += node_values[data[offset] - 1]
            except IndexError:
                pass
            offset += 1

    else:
        for i in range(metadata_entries_count):
            node_value += data[offset]
            offset += 1

    return offset, node_value


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        data = [int(x) for x in f.read().split()]
        print(parse_node(data)[1])


print(timeit.timeit(run, number=1))
