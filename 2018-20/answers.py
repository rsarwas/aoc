"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a single "\n" terminated string from the input file.
# _nodes_ are the rooms that can be reached. they are given as (row,col) tuples
# start at (0,0); A door to the North leads to (0,-1), S => (0,1), E => (1,0), W => (-1,0)
# the doors are the edges in a _graph_ of nodes
# graph[node] = a set of 1 to 4 nodes that are connected to node with a door


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    nodes, graph = build_graph(data)
    print(nodes, graph)
    total = len(data)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return lines[0].strip()[1:-1]


def build_graph(data):
    index = 0
    starts = [(0, 0)]
    nodes = set(starts)
    graph = {}
    process_route(starts, index, data, nodes, graph)
    return nodes, graph


def process_route(starts, index, data, nodes, graph):
    """
    route := leg*  // zero or more legs
    leg := "N" | "S" | "E" | "W" | branch2 | branch3
    branch2 := "(" route "|" route ")"
    branch3 := "(" route "|" route "|" route ")"
    """
    ends = []
    for start in starts:
        i = index
        current = start
        while i < len(data):
            char = data[i]
            new_room = door(current, char)
            nodes.add(new_room)
            if current not in graph:
                graph[current] = set()
            graph[current].add(new_room)
            current = new_room
            i += 1
        ends.append(current)
    index = i
    return index, ends


def dijkstra_distances(graph, starting_vertex, target_vertex=None):
    """Returns the shortest distance in graph from starting_vertex to target_vertex,
       or all nodes if target_vertex is None.

        Assumes vertices are integers from 0 to n. The distance to vertex v is
        at index v in the returned list

        The input graph is a list of lists of (vertex, cost) tuples. The index in
        the main list is the vertex id and the value is the vertex's neighbors
        for example: [ [(1,10),(2,20)], [(3,30)], [(3,40)] [] ]
          vertex 0 has neighbors 1 (cost 10) and 2 (cost 20)
          vertex 1 has only one neighbor 3 (cost 30)
          vertex 2 has only one neighbor 3 (cost 30)
          vertex 3 has no neighbors
              - 10 ->  1 - 30 ->
            /                    \
          0                       3
            \                    /
              - 20 -> 2 - 40 ->

    With small tweaks, this code can be tweaked to use dictionaries instead
    of lists. This allows any hashable item to be a vertex, but is slightly slower.
    """
    distances = [sys.maxsize] * len(graph)
    distances[starting_vertex] = 0

    # heapq sorts the items from min to max
    # if heapq item is a tuple, make sure the first element is the primary sorting key
    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)
        if current_vertex == target_vertex:
            return distances[current_vertex]
        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # here we are ignoring any time the minimum vertex has already been processed
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # heapq does not support update, so just add a new node (with a better distance)
                heapq.heappush(pq, (distance, neighbor))

    return distances


def door(room, door):
    """Return the room on the other side of the door.
    both room are (row,col) nodes. door is in {"N","S","E","W"}"""
    r, c = room
    if door == "N":
        return (r, c - 1)
    elif door == "S":
        return (r, c + 1)
    elif door == "E":
        return (r + 1, c)
    else:  # "W"
        return (r - 1, c)


def test_part1():
    lines = open("test.txt").readlines()
    print(f"test 0: expect 3; Got {part1(lines)}")
    lines = open("test1.txt").readlines()
    print(f"test 1: expect 10; Got {part1(lines)}")
    lines = open("test2.txt").readlines()
    print(f"test 2: expect 18; Got {part1(lines)}")
    lines = open("test3.txt").readlines()
    print(f"test 3: expect 23; Got {part1(lines)}")
    lines = open("test4.txt").readlines()
    print(f"test 4: expect 31; Got {part1(lines)}")


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
