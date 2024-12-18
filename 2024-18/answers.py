"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import heapq  # for a priority queue in dijkstra algorithm
import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    start = (0, 0)
    end = (size(), size())
    graph = build_graph(data[: bytes()], size())
    distance = dijkstra_distances(graph, start, end)
    return distance


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    # input data is x,y output data is list of (row, col) tuples
    data = []
    for line in lines:
        line = line.strip()
        coords = [int(n) for n in line.split(",")]
        # make the coord pair a (row,col) tuple which is hashable
        data.append((coords[1], coords[0]))
    return data


def size():
    """Return the size of the grid"""
    if INPUT == "input.txt":
        return 70
    return 6


def bytes():
    """Return how much memory will fall"""
    if INPUT == "input.txt":
        return 1024
    return 12


def build_graph(coords, size):
    """Build the graph of the grid after coords have been corrupted"""
    coords = set(coords)
    graph = {}
    for row in range(size + 1):
        for col in range(size + 1):
            if (row, col) not in coords:
                graph[(row, col)] = reachable_neighbors((row, col), coords, size)
    return graph


def reachable_neighbors(start, coords, size):
    """Return a list of the horizontal and vertical (not diagonal)
    neighbors of start that are non the grid, and not corrupted.
    coords in in (x,y) aka (col,row) format"""
    neighbors = []
    row, col = start
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if nr >= 0 and nr <= size and nc >= 0 and nc <= size and (nr, nc) not in coords:
            neighbors.append((nr, nc))
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
