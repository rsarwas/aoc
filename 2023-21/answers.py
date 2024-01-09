"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import heapq  # for a priority queue in dijkstra algorithm

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
    """Solve part 2 of the problem.

    This solution takes advantage of the following facts observed in the input data:
    1) There is an unobstructed row and column in the center and both edges of the grid,
    2) The grid is square,
    3) The start is in the exact center.
    This allows the elf to get to any adjacent grid in the minimum number of steps,
    and we can use symmetry and modulo math to do the counting.  This reduces
    the additional work in part 2 to primarily book keeping. To reduce the workload, the
    solution is not general to the number of time steps in the input, nor the the input
    grid.
    """
    _, rocks, size = parse(lines)
    graph = make_graph_from_grid(size, rocks)
    if size[0] != size[1]:
        return -1
    size = size[0]
    steps = 26501365
    n_grid = steps // size  # 202,300
    n_tile = steps % size  # 65
    total = count_tiles(graph, n_grid, n_tile)
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


def count_tiles(graph, n_grid, n_tile):
    """Count the potentially occupied tiles after steps.

    See the part2() for general assumptions about the input.

    Since the total number of steps is 26501365, and the grid is 131 x 131 with 65 rows above
    and below the start and 65 columns left and right of the start. The magic numbers are:
    n_tile = steps % size = 65 and n_grid = steps // size = 202,300.

    The elf will be in the adjacent grids in 66 steps and the diagonal grids in
    66*2 or 132 steps.  The total reachable grids is a diamond shape, 1 grid in the top row,
    3 in the 2nd row, etc. Since 26501365 / 131 = 202,300 rem 65, the elf will reach the far
    edge of the 202,300th grid beyond the start grid moving left, right, up, and down in the
    clear lanes.

    Since the total number of steps is odd, the elf cannot occupy the start tile, or any tile
    where the row and col match in odd/even-ness, and will occupy all other tiles in the
    central grid. This rule flips for the adjacent tiles (since the edge is odd, the edge
    of the adjacent tile is even).  The diagonal grids will have the same occupation as the
    starting grid.  Notice, that the rule for a tile (using the row/col number) is the same
    as for the grid (using the grid row/col number). Since there are an odd number of steps,
    the odd tiles in the start grid are selected, so we call the start grid odd, and adjacent
    grids even.

    At the perimeter, the only partial grids/quadrants are reachable.  Consider the following
    smaller example where n = 2 (instead of 202,300) in total steps = 131*n + 65

    |-------+-------+---+---+-------|-------|
    |       | X | X |P16|P01| X | X |       |
    |   X   |---+---|---+---|---+---|   X   |
    |       | X |P14|   |   |P02| X |       |
    |-------+-------+---+---+-------|-------|
    | X | X |P15|   |       |   |P03| X | X |
    |---+---|---+---|   :   |---+---|---+---|
    | X |P14|   |   |       |   |   |P02| X |
    |-------+-------+---+---+-------|-------|
    |P13|   |       |QUL|QUR|       |   |P04|
    |---+---|  ...  |---S---|  ...  |---+---|
    |P12|   |       |QLL|QLR|       |   |P05|
    |-------|---+---+-------+-------+-------|
    | X |P10|   |   |       |   |   |P06| X |
    |---+---|---+---|   :   |---+---|---+---|
    | X | X |P11|   |       |   |P07| X | X |
    |-------+-------+---+---+-------|-------|
    |       | X |P10|   |   |P06| X |       |
    |   X   |---+---|---+---|---+---|   X   |
    |       | X | X |P09|P08| X | X |       |
    |-------+-------+---+---+-------|-------|

    X means that a grid/quadrant is unreachable.  Pn means the quadrant is partially
    reachable, a shortest path search is needed (using a max distance of 65) to find
    out how many tiles are reachable from the corner closest to the center/start.
    There will be only one of Pn where n in (1,4,5,8,9,12,13,16) These will have the
    same on/off tiles as the starting tile (even), and the search starts from the center.
    There will be 202,300 of Pn where n in (2,6,10,14) these will have the opposite
    on/off tiles as the center tile (odd).  There will be 202,300 - 1 of Pn where n in
    (3,7,11,15) These will have the same on/off tiles as the start tile (even).

    In the grids that have partial quadrants, the other quadrants are completely filled
    or empty. For Pn where n in (1,4,5,8,9,12,13,16) There are 4 nearly full grids, we
    subtract the unreachable tiles (beyond 65 steps from the center of the grid) in the
    partial quadrants.  For Pn where n in (3,7,11,15), we do the same thing - remove the
    unreachable tiles (beyond 65 steps from the center) in the partial quadrant from a
    full grid. For Pn where n in (2,6,10,14), we count the reachable tiles from the
    corner of the partial quadrant closest to the center grid. IN these tiles, we can only
    go 64 steps, due to the cost of stepping into the diagonal tile. (this wasn't obvious
    at first, but a diagram helps prove it).

    There will be a lot of grids where all tiles are reachable (approximately
    4 * 202,300^2/2 or 81850580000) about half have on/off to match the start
    grid (odd) and the rest are opposite (even).  Looking at the examples like the
    diagram above where n = 2 (and then n = 3, 4, etc) on paper, there will be:
    n = 2: 4 even grids, 1 odd grid
    n = 3: 4 even, 9 odd
    n = 4: 16 even, 9 odd
    n = 5: 16 even, 25 odd
    n is even: n^2 even, (n-1)^2 odd
    n is odd: (n-1)^2 even, n^2 odd
    This and the pattern are easiest to see if the layout is rotated 45 degrees,
    or you look along the diagonals. since n is even, there are n^2 opposite, and
    (n-1)^2 the same.  This is close to the approximation of 2*n^2
    """
    # pylint: disable=too-many-locals
    if n_grid != 202300 or n_tile != 65:
        print("Unexpected input, cannot count tiles.")
        return -1
    total = 0

    # count wholes, formulas based on n_grid being even:
    # note some (10) open tiles are surrounded by rocks and can never be reached,
    # they are not included in the graph, so the size of the graph is the number
    # reachable nodes.

    count_odd_tiles = len(filter_grid_for_time_step(graph.keys(), 1))
    count_odd_grids = (n_grid - 1) * (n_grid - 1)
    # print(f"count_odd_grids: {count_odd_grids}; count_odd_tiles: {count_odd_tiles}")
    total += count_odd_grids * count_odd_tiles

    count_even_tiles = len(filter_grid_for_time_step(graph.keys(), 0))
    count_even_grids = n_grid * n_grid
    # print(f"count_even_grids: {count_even_grids}; count_even_tiles: {count_even_tiles}")
    total += count_even_grids * count_even_tiles

    # find distance to tiles from corners of each quadrant
    min_row, min_col = 0, 0
    center_row, center_col = n_tile, n_tile
    max_row, max_col = n_tile * 2, n_tile * 2
    distances_from_upper_left = dijkstra_distances(
        graph, (min_row, min_col), None, n_tile
    )
    distances_from_upper_right = dijkstra_distances(
        graph, (min_row, max_col), None, n_tile
    )
    distances_from_center = dijkstra_distances(
        graph, (center_row, center_col), None, n_tile
    )
    distances_from_lower_left = dijkstra_distances(
        graph, (max_row, min_col), None, n_tile
    )
    distances_from_lower_right = dijkstra_distances(
        graph, (max_row, max_col), None, n_tile
    )

    # Count grid with partials along center lines
    # These grids are all odd (match start grid)
    for bounds in [
        (min_row, min_col, center_row, max_col),  # 1 and 16 (remove some from upper)
        (min_row, center_col, max_row, max_col),  # 4 and 5 (remove some from right)
        (center_row, min_col, max_row, max_col),  # 8 and 9 (remove some from bottom)
        (min_row, min_col, max_row, center_col),  # 12 and 13 (remove some from left)
    ]:
        remove = unreachable_in_bounds(distances_from_center, n_tile, bounds)
        remove = filter_grid_for_time_step(remove, 1)
        # print(remove)
        tile_count = count_odd_tiles - len(remove)
        # print(tile_count)
        total += tile_count

    # Count grids with partials #2, #6, #10, #14
    # These grids are all even (opposite the start grid)
    for distances in [
        distances_from_lower_left,  # 2 (only part of LL is reachable)
        distances_from_upper_left,  # 6 (only part of UL is reachable)
        distances_from_upper_right,  # 10 (only part of UR is reachable)
        distances_from_lower_right,  # 14 (only part of LR is reachable)
    ]:
        locations = remove_unreachable(distances, n_tile - 1)
        locations = filter_grid_for_time_step(locations, 0)
        # print(locations)
        tile_count = len(locations)
        # print(tile_count)
        grid_count = n_grid
        total += grid_count * tile_count

    # Count grids with partial #3, 7, 11 and 15
    # These grids are all odd (same as start grid)
    # note distances_from_center has distance = infinity for all tiles more than
    # n_tile (65) steps from the center in all quadrants. Only remove the
    # unreachable ones from the correct quadrant.
    for bounds in [
        (min_row, center_col, center_row, max_col),  # 3 (remove some UR)
        (center_row, center_col, max_row, max_col),  # 7 (remove some LR)
        (center_row, min_col, max_row, center_col),  # 11 (remove some LL)
        (min_row, min_col, center_row, center_col),  # 15 (remove some UL)
    ]:
        remove = unreachable_in_bounds(distances_from_center, n_tile, bounds)
        remove = filter_grid_for_time_step(remove, 1)
        # print(remove)
        tile_count = count_odd_tiles - len(remove)
        # print(tile_count)
        grid_count = n_grid - 1
        total += grid_count * tile_count

    # testing to verify that there are no reentrant corners that are
    # harder to get to in the grids with partial quadrants.  i.e. all
    # the tiles in the other quadrants are reachable.
    # distances_from_lower_center = dijkstra_distances(
    #     graph, (max_row, center_col), None, 2 * n_tile
    # )
    # bounds = (center_row, min_col, max_row, max_col)
    # locations = unreachable_in_bounds(distances_from_lower_center, 2 * n_tile, bounds)
    # print(locations)

    # distances_from_upper_center = dijkstra_distances(
    #     graph, (min_row, center_col), None, 2 * n_tile
    # )
    # bounds = (min_row, min_col, center_row, max_col)
    # locations = unreachable_in_bounds(distances_from_upper_center, 2 * n_tile, bounds)
    # print(locations)

    # distances_from_center_left = dijkstra_distances(
    #     graph, (center_row, min_col), None, 2 * n_tile
    # )
    # bounds = (min_row, min_col, max_row, center_col)
    # locations = unreachable_in_bounds(distances_from_center_left, 2 * n_tile, bounds)
    # print(locations)

    # distances_from_center_right = dijkstra_distances(
    #     graph, (center_row, max_col), None, 2 * n_tile
    # )
    # bounds = (min_row, center_col, max_row, max_col)
    # locations = unreachable_in_bounds(distances_from_center_right, 2 * n_tile, bounds)
    # print(locations)

    return total


def unreachable_in_bounds(distances, distance, bounds):
    """Return the locations that are in the bounds and greater than distance
    Distances are a dictionary {node:distance, ...}, where node is (row,col).
    Bounds is (min_row, min_col, max_row, max_col)"""

    def in_bounds(node, bounds):
        (min_row, min_col, max_row, max_col) = bounds
        (row, col) = node
        return min_row <= row <= max_row and min_col <= col <= max_col

    unreachable = [node for (node, d) in distances.items() if d > distance]
    return [node for node in unreachable if in_bounds(node, bounds)]


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
