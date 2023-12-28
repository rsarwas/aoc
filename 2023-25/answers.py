"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import random  # to shuffle an array

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    n_nodes, edges = parse(lines)
    size1, size2 = find_min_cut3(n_nodes, edges)
    return size1 * size2


def parse(lines):
    """Convert the lines of text into a useful data model."""
    graph = {}
    for line in lines:
        line = line.strip()
        node, nodes = line.split(": ")
        nodes = nodes.split(" ")
        graph[node] = nodes
    return make_edges(graph)


def make_edges(graph):
    """Return the number of nodes (N), and a list of edges (u,v) where 0 <= u,v < N"""
    node_names = set()
    for node, nodes in graph.items():
        node_names.add(node)
        for other in nodes:
            node_names.add(other)
    n_nodes = len(node_names)
    node_id = {}
    for i, name in enumerate(node_names):
        node_id[name] = i
    edges = set()
    for node, nodes in graph.items():
        for other in nodes:
            # to only add the edge once, put the node_ids in order
            u = node_id[node]
            v = node_id[other]
            edge = (u, v)
            if v < u:
                edge = (v, u)
            edges.add(edge)
    return n_nodes, list(edges)


def find_min_cut3(n_nodes, edges):
    """Iterate over randomized list of edges until the min cut of edges is 3.
    Uses Karger's Algorithm, which only _hopes_ to find a min cut.
    However since the probability is high that a random edge is not one of
    the 3 min_cut edges, it should find the solution in only a few tries."""
    min_cut = n_nodes
    super_groups = None
    # iteration = 0
    while min_cut > 3:
        # iteration += 1
        # print(iteration)
        # each node goes in it's own super group
        super_groups = [set([i]) for i in range(n_nodes)]
        n_super_groups = n_nodes
        group = {}  # group[node] is the id of node's super group
        for i in range(n_nodes):
            group[i] = i
        random_edges = list(edges)
        random.shuffle(random_edges)
        while n_super_groups > 2:
            u, v = random_edges.pop()
            if group[u] == group[v]:
                # nodes are already in the same super group
                continue
            # merge group[v] into group[v]
            s_g_v = super_groups[group[v]]
            super_groups[group[u]] = super_groups[group[u]].union(s_g_v)
            super_groups[group[v]] = None
            n_super_groups -= 1
            for n in s_g_v:
                group[n] = group[u]
        remaining_edges = []
        for u, v in random_edges:
            if group[u] != group[v]:
                remaining_edges.append((u, v))
        min_cut = len(remaining_edges)
    size1, size2 = [len(group) for group in super_groups if group is not None]
    return size1, size2


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print("Part 2: There is no Part2!")


if __name__ == "__main__":
    main(INPUT)
