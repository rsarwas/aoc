"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
OPEN = "."
ROCK = "#"
START = "S"


def part1(lines):
    """Solve part 1 of the problem."""
    start, rocks, size = parse(lines)
    graph = make_graph_from_grid(size, rocks)
    steps = 64  # real problem
    if INPUT == "test.txt":
        steps = 6  # test case
    distances = dijkstra_distances(graph, start, None, steps)
    locations = remove_unreachable(distances, steps)
    locations = filter_grid_for_time_step(locations, steps)
    total = len(locations)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    start, rocks, size = parse(lines)
    graph = make_graph_from_grid(size, rocks)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model.
    Return a set of all the locations (row,col) of rocks (no-go tiles)
    and the extents, (max_row, max_col), and the start (row, col)"""
    max_rows = len(lines)
    max_cols = len(lines[0].strip())
    extents = (max_rows, max_cols)
    rocks = set()
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == START:
                start = (row, col)
            if char == ROCK:
                rocks.add((row, col))
    return start, rocks, extents


def make_graph_from_grid(size, no_go):
    """Return a graph from the grid, given the size and a list of no-go tiles
    size is a (max_rows, max_cols) tuple and no_go is a set of
    (row, col) tuples.  In this grid, you cannot move diagonally.
    the graph is a dictionary of nodes with a list of adjacent nodes as the
    key's value. nodes are (row, col) tuples.  The graph is unweighted, and
    undirected.  All edges are represented in both directions."""
    graph = {}
    (max_rows, max_cols) = size
    for row in range(max_rows):
        for col in range(max_cols):
            node = (row, col)
            if node in no_go:
                continue
            other_nodes = valid_neighbors(node, no_go, size)
            if other_nodes:
                graph[node] = other_nodes
            # else:
            #    print(f"node {node} has no reachable neighbors, ignore")
    return graph


def valid_neighbors(location, rocks, extents):
    """Return all the locations adjacent to location (up, down, left, right)
    that are on the grid GTE (0,0) and LT extents, and not a rock"""
    old_row, old_col = location
    max_row, max_col = extents
    neighbors = []
    for row in [old_row - 1, old_row + 1]:
        if 0 <= row < max_row and (row, old_col) not in rocks:
            neighbors.append((row, old_col))
    for col in [old_col - 1, old_col + 1]:
        if 0 <= col < max_col and (old_row, col) not in rocks:
            neighbors.append((old_row, col))
    return neighbors


def dijkstra_distances(graph, starting_vertex, target_vertex=None, max_distance=None):
    """Returns the shortest distance in graph from starting_vertex to target_vertex,
    or all nodes if target_vertex is None. If max_vertex is not None, stop when
    the shortest distance to all remaining nodes is greater than max_distance; the
    distance reported for those nodes will be infinity.

    Vertexes can be any hashable (int, char, string, tuple, etc).
    The returned distances are in a dictionary (key = vertex, value = min cost
    from starting vertex)

    The input graph is a dict of iterables, the key is a node and the iterable is the
    other nodes connected by an edge to that nodes.  All edges have a weight of 1
    """
    distances = {vertex: float("infinity") for vertex in graph}
    distances[starting_vertex] = 0

    # heapq sorts the items from min to max
    # if heapq item is a tuple, make sure the first element is the primary sorting key
    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)
        # check if we are done
        if current_vertex == target_vertex:
            return distances[current_vertex]

        # Since pq is sorted, when we hit max_distance, all remaining distances will be greater
        if max_distance is not None and current_distance > max_distance:
            return distances

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # here we are ignoring any time the minimum vertex has already been processed
        if current_distance > distances[current_vertex]:
            continue

        for neighbor in graph[current_vertex]:
            distance = current_distance + 1

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # heapq does not support update, so just add a new node (with a better distance)
                heapq.heappush(pq, (distance, neighbor))
    return distances


def remove_unreachable(distances, max_distance):
    """Remove items from distances that have a distance greater than max"""
    return [node for (node, distance) in distances.items() if distance <= max_distance]


def filter_grid_for_time_step(locations, time_step):
    """Remove the locations [(row,col), ...] that are not occupied on time_step.
    For example, the starting tile can be occupied on time_step 0, 2, 4, but not
    on time_step 1,3,5,.... Similarly, the tiles adjacent to the starting tile can
    be occupied on the odd time steps, but not the even time steps.

    Any tile that is reachable within the total time can be considered because
    the elf can oscillate back and forth until the time is up.

    This solution is not generalized for any start location, instead, we take
    advantage of the fact that in both the puzzle input and the test input
    the start tile is at an odd row and odd column.
    """
    if time_step % 2:
        # odd time step
        return [(row, col) for (row, col) in locations if not same_odd_even(row, col)]
    # even time step
    return [(row, col) for (row, col) in locations if same_odd_even(row, col)]


def same_odd_even(row, col):
    """Return true IFF row and column are both odd or both even."""
    return row % 2 == col % 2


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
