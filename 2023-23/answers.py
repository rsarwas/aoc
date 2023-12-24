"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
from collections import defaultdict  # for the longest path algorithm

INPUT = "input.txt"
WALL = "#"
DOWN = "v"
UP = "^"
RIGHT = ">"
LEFT = "<"


def part1(lines):
    """Solve part 1 of the problem."""
    maze = parse(lines)
    graph, weights = make_dag(maze)
    return longest_path(graph, weights)


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return [line.strip() for line in lines]


def make_dag(maze):
    """Return a Directed Acyclic Graph from the maze.
    nodes is a list of locations (row, col), the list index is the node_id,
    edges are (start_node_id, end_node_id, edge_length) tuples,
    graph is a dict of nodes as keys and the value is a list of nodes available from node
    weights is a dict where edge (u,v) is a key and the value is the weight of the edge
    """
    path = make_path(maze)
    start, end = find_ends(maze)
    junctions = make_junctions(start, end, path)
    nodes = make_nodes(junctions)
    # for i, n in enumerate(nodes):
    #     print(f"{i}: {n}")
    edges = make_edges(junctions, path)
    edges = simplify_edges(edges, nodes)
    # for edge in edges:
    #     print(edge)
    # a more standard python representation of a graph
    graph = edges_to_graph(edges)
    weights = edges_to_weights(edges)
    return graph, weights


def make_path(maze):
    """Return a dictionary of all the locations that are not walls.
    save the type of location, so we can check for incoming/outgoing branches."""
    path = {}
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char != WALL:
                path[(row, col)] = char
    return path


def find_ends(maze):
    """Return the location (row, col) of the start and end tiles,
    They are the only open tiles in the first and last row respectively"""
    start_row = 0
    start_col = None
    end_row = len(maze) - 1
    end_col = None
    for col, char in enumerate(maze[start_row]):
        if char != WALL:
            start_col = col
            break
    for col, char in enumerate(maze[end_row]):
        if char != WALL:
            end_col = col
            break
    return (start_row, start_col), (end_row, end_col)


def make_junctions(start, end, path):
    """Return a dictionary of junctions. A Junction is a location with an incoming list
    and an outgoing list of locations. Either list can be empty. the location is stored
    as the key; the value is an {'in':[], 'out':[]} dictionary."""
    junctions = {}
    for location in path:
        branches = find_neighbors(location, path)
        if location == start:
            junctions[start] = {"in": [], "out": branches}
            continue
        if location == end:
            junctions[end] = {"in": branches, "out": []}
            continue
        if len(branches) == 2:
            continue
        junctions[location] = {
            "in": [
                branch for branch in branches if is_incoming(location, branch, path)
            ],
            "out": [
                branch for branch in branches if not is_incoming(location, branch, path)
            ],
        }
    return junctions


def find_neighbors(this, path):
    """Return a list of adjacent locations that are on the path."""
    row, col = this
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return [n for n in neighbors if n in path]


def is_incoming(location, branch, path):
    """Return True IFF the path location at branch is coming into location"""
    char = path[branch]
    row1, col1 = location
    row2, col2 = branch
    # above
    if row2 < row1 and char == DOWN:
        return True
    # below
    if row1 < row2 and char == UP:
        return True
    # left
    if col2 < col1 and char == RIGHT:
        return True
    # right
    if col1 < col2 and char == LEFT:
        return True
    return False


def make_edges(junctions, path):
    """Return a list of edges between junctions in the path.
    an edge is (start_junction, end_junction, length)"""
    edges = []
    for junction in junctions:
        for out in junctions[junction]["out"]:
            segment = make_segment(junction, out, junctions, path)
            edges.append((segment[0], segment[-1], len(segment) - 1))
    return edges


def make_segment(junction, next_location, junctions, path):
    """Return the segment starting at junction, going through next,
    until the next junction in junctions.  Each segment is a list of all
    locations along the segment and will always start and stop on a junction
    """
    start = junction
    segment = [start]
    while next_location not in junctions:
        segment.append(next_location)
        start, next_location = find_next(start, next_location, path)
    segment.append(next_location)
    return segment


def find_next(previous, this, path):
    """There will always be 2 neighbors of this location, and one will be the previous location.
    Return the other location, as well as this for the next round"""
    row, col = this
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    for neighbor in neighbors:
        if neighbor in path and neighbor != previous:
            return this, neighbor
    print(f"Find_next failed with {previous}, {this}")
    return None


def make_nodes(junctions):
    """Return a list where index = node_id, data is location (row,col) of node"""
    nodes = list(junctions.keys())
    nodes.sort()
    return nodes


def simplify_edges(edges, nodes):
    """Replace the location (row, col) in edges with the node id in nodes"""
    new_edges = []
    for start, end, length in edges:
        start_id = nodes.index(start)
        end_id = nodes.index(end)
        new_edges.append((start_id, end_id, length))
    return new_edges


def edges_to_graph(edges):
    """Return a graph (a dict of nodes as keys and the value is a list of nodes available from node)
    given a list of edges (start_node_id, end_node_id, edge_length) tuples.
    weights is a dict where edge (u,v) is a key and the value is the weight of the edge
    """
    graph = {}
    for node1, node2, _ in edges:
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append(node2)
    return graph


def edges_to_weights(edges):
    """Return weights (a dict where edge (u,v) is a key and the value is the weight of the edge)
    given a list of edges (start_node_id, end_node_id, edge_length) tuples.
    """
    weights = {}
    for node1, node2, weight in edges:
        weights[(node1, node2)] = weight
    return weights


def longest_path(graph, weights):
    """Return the longest path in a Directed Acyclic Graph.
    graph is a dict of nodes as keys and the value is a list of nodes available from node
    weights is a dict where edge (u,v) is a key and the value is the weight of the edge
    """
    sorted_nodes = topological_sort(graph)
    dist = defaultdict(lambda: float("-inf"))
    dist[sorted_nodes[0]] = 0

    for node in sorted_nodes:
        for successor in graph[node]:
            dist[successor] = max(
                dist[successor], dist[node] + weights[(node, successor)]
            )

    return max(dist.values())


def topological_sort(graph):
    """Topologically order/sort the graph.
    For every directed edge (u,v) from u to v, u comes before v in the ordering.
    graph is a dict of nodes as keys and the value is a list of nodes available from node
    """
    visited = set()
    sorted_nodes = []

    def visit(node):
        """Mark node as visited"""
        if node not in visited:
            visited.add(node)
            for successor in graph[node]:
                visit(successor)
            sorted_nodes.append(node)

    for node in graph:
        visit(node)
    return sorted_nodes[::-1]


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
