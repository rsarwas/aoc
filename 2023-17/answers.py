"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# data is a flattened matrix (a list) of weights, where i = row * ncols + col)


import os.path  # to get the directory name of the script (current puzzle year-day)
import heapq  # for a priority queue (min_heap)

INPUT = "test.txt"
N_ROWS = 0
N_COLS = 0
RIGHT = ">"
LEFT = "<"
UP = "^"
DOWN = "v"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    start = 0
    end = index(N_ROWS - 1, N_COLS - 1)
    distance = dijkstra_distances(data, find_neighbors, start, end)
    return distance


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    start = 0
    end = index(N_ROWS - 1, N_COLS - 1)
    distance = dijkstra_distances(data, find_neighbors2, start, end)
    return distance


# pylint: disable=global-statement
def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    global N_ROWS
    global N_COLS
    N_ROWS = len(lines)
    N_COLS = len(lines[0].strip())
    for line in lines:
        line = line.strip()
        data.extend([int(i) for i in line])
    return data


def index(row, col):
    """Return the index in a list of a flattened matrix, given the row and col."""
    return row * N_COLS + col


def row_col(i):
    """Given the index into a list, return the row/col of "un-flattened" matrix."""
    row = i // N_COLS
    col = i % N_COLS
    return (row, col)


def dijkstra_distances(graph, neighbors_fn, starting_vertex, target_vertex=None):
    """Returns the shortest distance in graph from starting_vertex to target_vertex,
    or all nodes if target_vertex is None.

    Assumes vertices are integers from 0 to n. The graph isn't really a graph
    it is the weight of each vertex.  The edges (reachable vertices) is determined
    by the function neighbors_fn(v, direction, run, graph)
    Adapted from 2021-15
    """
    distances = {}
    # we need to save consider the direction and distance at a vertex
    # if the distances into a vertex are the same for different paths, we
    # need to consider both (but not if the direction is the same), because
    # the available neighbors are different for different directions.

    distances[(starting_vertex, RIGHT)] = 0

    # heapq sorts the items from min to max
    # if heapq item is a tuple, make sure the first element is the primary sorting key
    # our heapq contains, (weight, vertex, direction and run) values, dir and run are direction
    # and run used to reach this vertex, which will determine which neighbors are reachable from
    # this position.
    pq = [(0, starting_vertex, RIGHT, 0)]
    while len(pq) > 0:
        current_distance, current_vertex, direction, run = heapq.heappop(pq)
        if current_vertex == target_vertex:
            # print(distances)
            return distances[(current_vertex, direction)]
        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # here we are ignoring any time the minimum vertex has already been processed
        if (current_vertex, direction) in distances:
            if current_distance > distances[(current_vertex, direction)]:
                continue

        for direction, run, neighbor, weight in neighbors_fn(
            current_vertex, direction, run, graph
        ):
            distance = current_distance + weight

            # Only consider this new path if it's better than _or equal_ to any path we've
            # already found. Equal is considered, because we probably got hear with a different
            # direction/run which provides a different set of neighbors to consider
            if (neighbor, direction) not in distances or distance < distances[
                (neighbor, direction)
            ]:
                distances[(neighbor, direction)] = distance
                # heapq does not support update, so just add a new node (with a better distance)
                heapq.heappush(pq, (distance, neighbor, direction, run))

    return distances


def find_neighbors(v, direction, run, graph):
    """Find the neighbors of a vertex and the distance/weight to get to it
    v is an index into graph, and the returned list is a list of reachable
    vertices with the weight to get there.

    direction is the previous direction of travel; neighbors are left and right
    (1, 2, or 3 spaces), and straight ahead if run is less than 3. so 1 or 2 spaces
    The returned list will be 6, 7 or 8 vertices long in the field.  This may be
    reduced if we are near an edge
    Return a list of (direction, run, neighbor, weight) tuples"""
    neighbors = []
    # Add options to the left
    total_weight = 0
    for new_run in [1, 2, 3]:
        new_dir = turn_left(direction)
        new_v = location(v, new_dir, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        neighbors.append((new_dir, new_run, new_v, total_weight))
    # Add options to the right
    total_weight = 0
    for new_run in [1, 2, 3]:
        new_dir = turn_right(direction)
        new_v = location(v, new_dir, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        neighbors.append((new_dir, new_run, new_v, total_weight))
    # Add options straight ahead
    # QUESTION: Is this necessary?
    #   It seems that the three options in this direction were already considered
    total_weight = 0
    runs = list(range(1, 4 - run))  # run 0 -> [1,2,3]; run 1 -> [1,2]; run 3 -> []
    for new_run in runs:
        new_v = location(v, direction, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        neighbors.append((direction, new_run + run, new_v, total_weight))
    return neighbors


def find_neighbors2(v, direction, run, graph):
    """Find the neighbors of a vertex and the distance/weight to get to it
    v is an index into graph, and the returned list is a list of reachable
    vertices with the weight to get there.

    direction is the previous direction of travel; neighbors are left and right
    (4 to 10 spaces) if run is 4 or better, and straight ahead if run is less than 10.

    Return a list of (direction, run, neighbor, weight) tuples"""
    neighbors = []
    # Add options to the left (run will always be 4 or more)

    total_weight = 0
    for new_run in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        new_dir = turn_left(direction)
        new_v = location(v, new_dir, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        if new_run >= 4:
            neighbors.append((new_dir, new_run, new_v, total_weight))
    # Add options to the right
    total_weight = 0
    for new_run in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        new_dir = turn_right(direction)
        new_v = location(v, new_dir, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        if new_run >= 4:
            neighbors.append((new_dir, new_run, new_v, total_weight))
    # Add options straight ahead
    # QUESTION: Is this necessary?
    #   It seems that the three options in this direction were already considered
    total_weight = 0
    runs = list(range(1, 11 - run))  # run 4 -> [1..6]; run 9 -> [1]; run 10 -> []
    if v == 0 and direction == RIGHT:
        runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for new_run in runs:
        new_v = location(v, direction, new_run)
        if new_v is None:
            break
        weight = graph[new_v]
        total_weight += weight
        if new_run + run >= 4:
            neighbors.append((direction, new_run + run, new_v, total_weight))
    return neighbors


# pylint: disable=too-many-return-statements
def location(vertex, direction, distance):
    """Return the new vertex after traveling distance spaces in direction from vertex.
    Return None if new_ vertex is off the grid."""
    row, col = row_col(vertex)
    if direction == RIGHT:
        col += distance
        if col >= N_COLS:
            return None
        return index(row, col)
    if direction == LEFT:
        col -= distance
        if col < 0:
            return None
        return index(row, col)
    if direction == UP:
        row -= distance
        if row < 0:
            return None
        return index(row, col)
    # DOWN
    row += distance
    if row >= N_ROWS:
        return None
    return index(row, col)


def turn_left(direction):
    """Return the new direction if we turn left when moving in direction"""
    if direction == RIGHT:
        return UP
    if direction == UP:
        return LEFT
    if direction == LEFT:
        return DOWN
    return RIGHT


def turn_right(direction):
    """Return the new direction if we turn right when moving in direction"""
    if direction == RIGHT:
        return DOWN
    if direction == DOWN:
        return LEFT
    if direction == LEFT:
        return UP
    return RIGHT


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
