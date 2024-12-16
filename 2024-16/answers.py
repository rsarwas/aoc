"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import heapq  # for a priority queue in dijkstra algorithm

INPUT = "input.txt"

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def part1(lines):
    """Solve part 1 of the problem."""
    maze, start, end = parse(lines)
    graph = build_graph(maze)
    start = (start[0], start[1], EAST)
    r, c = end
    ends = [(r, c, EAST), (r, c, WEST), (r, c, NORTH), (r, c, SOUTH)]
    distance = dijkstra_distances(graph, start, ends)
    return distance


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    maze = []
    start, end = None, None
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char in [".", "S", "E"]:
                maze.append((row, col))
            if char == "S":
                start = (row, col)
            if char == "E":
                end = (row, col)
    return maze, start, end


def build_graph(maze):
    """Create a graph - a dictionary of nodes and edges.  There are four nodes for
    each location in the maze (one for each direction).  the edges are
    in a dictionary that has the node for a key, and a list of nodes
    that are reachable from the key.  Each node in the list contains the
    cost (integer) to get to that node.
    Node = (row, col, direction), Edge[node] = [(node, cost), ...]
    There are at most 3 edges for each node (left, forward, and right).
    The cost of left and right is 1001, and the cost of forward is 1.
    """
    graph = {}
    for location in maze:
        row, col = location
        for direction in range(4):
            graph[(row, col, direction)] = find_neighbors(location, direction, maze)
    return graph


def find_neighbors(location, direction, maze):
    """return a list of reachable neighboring nodes and their cost
    The list may be empty"""
    neighbors = []
    row, col = location
    if direction == NORTH:
        if (row - 1, col) in maze:
            neighbors.append(((row - 1, col, NORTH), 1))
        if (row, col - 1) in maze:
            neighbors.append(((row, col - 1, WEST), 1001))
        if (row, col + 1) in maze:
            neighbors.append(((row, col + 1, EAST), 1001))
    if direction == SOUTH:
        if (row + 1, col) in maze:
            neighbors.append(((row + 1, col, SOUTH), 1))
        if (row, col - 1) in maze:
            neighbors.append(((row, col - 1, WEST), 1001))
        if (row, col + 1) in maze:
            neighbors.append(((row, col + 1, EAST), 1001))
    if direction == EAST:
        if (row, col + 1) in maze:
            neighbors.append(((row, col + 1, EAST), 1))
        if (row - 1, col) in maze:
            neighbors.append(((row - 1, col, NORTH), 1001))
        if (row + 1, col) in maze:
            neighbors.append(((row + 1, col, SOUTH), 1001))
    if direction == WEST:
        if (row, col - 1) in maze:
            neighbors.append(((row, col - 1, WEST), 1))
        if (row - 1, col) in maze:
            neighbors.append(((row - 1, col, NORTH), 1001))
        if (row + 1, col) in maze:
            neighbors.append(((row + 1, col, SOUTH), 1001))
    return neighbors


def left(direction):
    """Return a new direction, by rotating left (CCW) 90 degrees."""
    direction -= 1
    direction %= 4
    return direction


def right(direction):
    """Return a new direction, by rotating right (CW) 90 degrees."""
    direction += 1
    direction %= 4
    return direction


def dijkstra_distances(graph, starting_vertex, target_vertices=None, max_distance=None):
    """Returns the shortest distance in graph from starting_vertex to any of the target_vertices,
    or all nodes if target_vertex is None. If max_distance is not None, stop when
    the shortest distance to all remaining nodes is greater than max_distance; the
    distance reported for those nodes will be infinity.

    Vertexes can be any hashable (int, char, string, tuple, etc).
    The returned distances are in a dictionary (key = vertex, value = min cost
    from starting vertex)

    The input graph is a dict of iterables, the key is a node and the iterable contains the
    other nodes connected by an edge to the key node.  All edges have an associated cost.
    iterable looks like (node1, cost1), (node2, cost2), ...
    """
    distances = {vertex: float("infinity") for vertex in graph}
    distances[starting_vertex] = 0

    # heapq sorts the items from min to max
    # if heapq item is a tuple, make sure the first element is the primary sorting key
    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)
        # check if we are done
        if current_vertex in target_vertices:
            return distances[current_vertex]

        # Since pq is sorted, when we hit max_distance, all remaining distances will be greater
        if max_distance is not None and current_distance > max_distance:
            return distances

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # here we are ignoring any time the minimum vertex has already been processed
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, cost in graph[current_vertex]:
            distance = current_distance + cost

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # heapq does not support update, so just add a new node (with a better distance)
                heapq.heappush(pq, (distance, neighbor))
    return distances


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
