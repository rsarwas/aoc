# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# chars is a matrix of characters from the input file (each line is the same length)
# maze is a dictionary data structure storing information in the chars
#   chars: chars
#   num_rows, num_columns = the number of rows and columns in chars
#   left_outer = the column index of the left outer wall
#   left_inner, right_inner, right_outer = similar to left_outer
#   top_outer = the row index of the top outer wall
#   top_inner, bottom_inner, bottom_outer
#   inner_portals = {'name': (row, col)}
#   outer_portals = {'name': (row, col)}
#     there are two special vertices in outer_portals named START and END which are not portals
#     all other vertices will have a match in inner_portals
#   intersections = {'name': (row,col)}; name is 'i1', 'i2', ... 'in'
#   vertex_at = {(row,col): name}
# graph is a dict of dicts of (key=vertex, value=cost). The key in
#   the main dict is the vertex id and the value is the vertex's neighbors
#   every vertex must be in the graph, even if it has no neighbors
#   for example {'AA': {'i1': 1}, 'ZZ': {}, 'i1': {'BCi': 3, 'i2': 24}, ....}
# graph is built from the maze and maze is built from the grid and grid is built from the lines

import heapq  # for a priority queue in dijkstra algorithm

START = "AA"
END = "ZZ"
WALL = "#"
OPEN = "."
VOID = " "
OUTER_VOID_SIZE = (
    2  # All samples and the real puzzle have a margin of 2 voids around the perimeter
)
# The size of the inner void varies and must be determined by inspection


def part1(lines):
    maze = parse(lines)
    # print(maze)
    graph = build_graph(maze)
    cost = dijkstra_distances(graph, START, END)
    return cost


def part2(lines):
    maze = parse(lines)
    graph = build_graph(maze)
    cost = dijkstra_distances(graph, START, END)
    return cost


def parse(lines):
    chars = [list(line[:-1]) for line in lines]
    maze = {}
    maze["chars"] = chars
    num_columns = len(chars[0])
    num_rows = len(chars)
    maze["num_columns"] = num_columns
    maze["num_rows"] = num_rows
    set_boundary(maze)
    set_named_vertices(maze)
    set_intersections(maze)
    maze["vertex_at"] = {}  # {(row,col): name}
    return maze


def set_boundary(maze):
    left_outer = 0
    right_outer = maze["num_columns"] - 1
    top_outer = 0
    bottom_outer = maze["num_rows"] - 1

    if OUTER_VOID_SIZE is not None:
        left_outer += OUTER_VOID_SIZE
        right_outer -= OUTER_VOID_SIZE
        top_outer += OUTER_VOID_SIZE
        bottom_outer -= OUTER_VOID_SIZE
    else:
        # find it by inspection similar to inner void below
        pass

    left_inner = None
    right_inner = None
    top_inner = None
    bottom_inner = None
    # find the location of the inner void:
    for r, line in enumerate(maze["chars"]):
        if r < top_outer or r >= bottom_outer:
            continue
        for c, char in enumerate(line):
            if c < left_outer or c >= right_outer:
                continue
            if char == VOID and left_inner is None:
                left_inner = c - 1
                top_inner = r - 1
                # all samples and the puzzle are symmetrical
                # if other input, is not, keep searching until we find the other corner
                right_inner = maze["num_columns"] - 1 - left_inner
                bottom_inner = maze["num_rows"] - 1 - top_inner
                break
        if bottom_inner is not None:
            break
    maze["left_outer"] = left_outer
    maze["left_inner"] = left_inner
    maze["right_inner"] = right_inner
    maze["right_outer"] = right_outer
    maze["top_outer"] = top_outer
    maze["top_inner"] = top_inner
    maze["bottom_inner"] = bottom_inner
    maze["bottom_outer"] = bottom_outer


def set_named_vertices(maze):
    maze["start"] = ()
    maze["end"] = ()
    maze["inner_portals"] = {}  # {'name': (row, col)}
    maze["outer_portals"] = {}


def set_intersections(maze):
    maze["intersections"] = {}  # {'name': (row,col)}; name is 'i1', 'i2', ... 'in'


def build_graph(maze):
    graph = {
        "AA": {"i1": 1},
        "ZZ": {},
        "i1": {"BCi": 3, "i2": 24},
        "i2": {"ZZ": 1, "i1": 24, "FGi": 5},
        "BCo": {"BCi": 1, "DEi": 6},
        "DEo": {"DEi": 1, "FGo": 4},
        "FGo": {"FGi": 1, "DEo": 4},
        "BCi": {"BCo": 1, "i1": 3},
        "DEi": {"DEo": 1, "BCo": 6},
        "FGi": {"FGo": 1, "i2": 5},
    }
    return graph


def dijkstra_distances(graph, starting_vertex, target_vertex=None):
    """Returns the shortest distance in graph from starting_vertex to target_vertex,
       or all nodes if target_vertex is None.

        Vertexes can be any hashable (int, char, string, tuple, etc). 
        The returned distances are in a dictionary (key = vertex, value = min cost
        from starting vertex)

        The input graph is a dict of dicts of (key=vertex, value=cost). The key in
        the main dict is the vertex id and the value is the vertex's neighbors
        every vertex must be in the graph, even if it has no neighbors
        for example: {0:{1:10,2:20}, 1:{3:30}, 2:{3:40} 3:{}}
          vertex 0 has neighbors 1 (cost 10) and 2 (cost 20)
          vertex 1 has only one neighbor 3 (cost 30)
          vertex 2 has only one neighbor 3 (cost 30)
          vertex 3 has no neighbors
              - 10 ->  1 - 30 ->
            /                    \
          0                       3
            \                    /
              - 20 -> 2 - 40 ->

    If vertex_ids are ints for 0 to n, this code can be tweaked to use lists instead
    of dicts. This is slightly faster, but less general.
    """
    distances = {vertex: float("infinity") for vertex in graph}
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

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # heapq does not support update, so just add a new node (with a better distance)
                heapq.heappush(pq, (distance, neighbor))

    return distances


if __name__ == "__main__":
    lines = open("test.txt").readlines()  # as a list of line strings
    # lines = open("test1.txt").readlines() # as a list of line strings
    # lines = open("test2.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
