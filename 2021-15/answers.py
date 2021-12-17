# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is filled with the digits 1-9.  It represents a grid
# of risk levels.  Travel through the grid from top left (r,c) = (0,0)
# to bottom right with the least risk; do not move diagonally.

# My first solution: part1_brute_force() and min_path()
# is a brute force recursion solution.
# As an optimization, I limit the depth of recursion by picking
# a random shortest path, and pass that as a best path found so far,
# and end the recursion if the current attempt cannot beat the current
# best path
# This solution is good enough to solve the sample, but is too slow to
# solve the real problem.

# The Part1 solution uses dijkstra's algorithm with a simple linear search
# for the minimum vertex.  This is O(V2), where V = 10_000 vertices.

# Part2 expands this to a 500x500 grid or 250_000 vertices.  The time to solve
# part 1 was ~ 3.39secs.  Therefore the time to solve the larger puzzle will
# be t = 3.39 / 10_000^2 * 250_000^2 = 35.5minutes, The cost of finding the
# neighbors and cost will be a little more complicated, but it could double
# or triple the expected run time. without some optimization.  If a optimize
# solution is implemented, the run time will be O((E + V)log2(V)), since there
# are 4 edges for every vertex, this will yield a run time of
# ~ 3.39 / 10_000^2 * (4+1)250_000*log2(250_000) = ~ 0.8 seconds (faster than
# the 100x100 grid with a linear search!)
#
# Therefore, I can ignore ways to simplify the graph or try to find tricks
# that might use the similarity of the 100x100 tiles that make up the larger
# grid (none of which seem promising anyway). Time to find a more efficient
# way to extract the minimum vertex (priority queue with a balance binary
# search tree?)

# To make neighbor lookup faster, and eliminate redundant computation,
# inside the dijkstra loops, (especially when it is more complicated
# in part 2), I create a list of edges which have a vertex_id for the
# index, the list items are lists of the (vertex_id,cost) tuples for
# all the neighbors of vertex_id

import sys # for sys.maxint

def part1(lines):
    grid = parse(lines)
    # dijkstra function assumes integer vertex ids
    start = vertex_id(0, 0, grid)
    target = vertex_count(grid) - 1
    edges = build_edges(grid)
    dist, _ = dijkstra(edges, start, target)
    return dist[target]

def part2(lines):
    grid = parse(lines)
    # dijkstra function assumes integer vertex ids
    start = 0 # (r,c) = (0,0)
    target = vertex_count2(grid) - 1
    edges = build_edges2(grid)
    dist, _ = dijkstra(edges, start, target)
    return dist[target]

def parse(lines):
    grid = []
    for line in lines:
        row = [int(c) for c in line.strip()]
        grid.append(row)
    return grid

def build_edges(grid):
    edges = []
    n_r, n_c = len(grid), len(grid[0])
    for v_id in range(vertex_count(grid)):
        v_r, v_c = row_column(v_id, grid)
        neighbors = []
        for (dr,dc) in [(0,-1),(-1,0),(1,0),(0,1)]:
            (r,c) = (v_r + dr, v_c + dc)
            if r < 0 or c < 0 or r >= n_r or c >= n_c:
                continue # do not go off the grid
            neighbors.append((vertex_id(r,c,grid), grid[r][c]))
        edges.append(neighbors)
    return edges

# See https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode
def dijkstra(edges, source, target):
    n = len(edges)
    vertices = set(range(0,n))
    dist = [sys.maxsize] * n
    # prev = [None] * n
    dist[source] = 0
    
    while vertices:
        # find vertex in vertices with min dist[u]
        dist_u, u = sys.maxsize, None
        for v in vertices:
            if dist[v] < dist_u:
                dist_u, u = dist[v], v
        # print("min dist[u]", u, dist_u)
        vertices.remove(u)
        if u == target:
            # print("Found target", u, dist[u])
            return dist, None #, prev
        for v, cost in edges[u]:
            if v not in vertices:
                continue
            alt = dist_u + cost
            # print("  neighbors u, v, cost", u, v, alt)
            if alt < dist[v]:              
                dist[v] = alt
                # prev[v] = u
    return dist, None #, prev

def vertex_count(graph):
    # vertices will be numbered 0 to n*m for an nxm grid
    # vertex 0 is at (0,0), 1 at (0,1), etc
    return len(graph) * len(graph[0])

def row_column(vertex_id, graph):
    n = len(graph[0]) # the length of a row
    return vertex_id // n, vertex_id % n

def vertex_id(r, c, graph):
    n = len(graph[0]) # the length of a row
    return r * n + c

# For part 2:
# The input is just one tile in a 5x5 tile area that forms the graph.
# The tiles will be numbered for 0 to 24 from left to right then top
# to bottom. A vertex_id (0..5*m*5*n], for an input of an nxm grid
# can be translated to a row and column in the input grid and a tile_id

def build_edges2(grid):
    edges = []
    tile_cost = [0,1,2,3,4,
                1,2,3,4,5,
                2,3,4,5,6,
                3,4,5,6,7,
                4,5,6,7,8]
    # the new costs are in (1..9) if the cost + inc > 9 then it wraps to 1
    tile_height, tile_width = len(grid), len(grid[0])
    num_tiles_wide, num_tiles_tall = 5,5
    graph_height = tile_height * num_tiles_tall
    graph_width = tile_width * num_tiles_wide
    for v_id in range(graph_height * graph_width):
        graph_row, graph_col = graph_row_column(v_id, graph_width)
        neighbors = []
        for (dr,dc) in [(-1,0),(0,1),(1,0),(0,-1)]:
            (gr,gc) = (graph_row + dr, graph_col + dc)
            if gr < 0 or gc < 0 or gr >= graph_height or gc >= graph_width:
                continue # do not go off the graph
            r,c = tile_row_column(gr, gc, tile_height, tile_width)
            n_id = vertex_id2(gr, gc, graph_width)
            tile_id = get_tile_id(gr, gc, tile_height, tile_width, num_tiles_wide)
            cost = grid[r][c] + tile_cost[tile_id]
            cost = 1 + ((cost - 1) % 9)
            neighbors.append((n_id, cost))
        edges.append(neighbors)
    return edges

def vertex_count2(grid):
    # vertices will be numbered 0 to 5*n*5*m for an nxm grid
    # vertex 0 is at (0,0), 1 at (0,1), etc
    # the total graph is 25 (5x5) tiles of grid
    return 5*len(grid) * 5*len(grid[0])

def graph_row_column(v_id, graph_width):
    graph_row = v_id // graph_width
    graph_col = v_id % graph_width
    return (graph_row, graph_col)

def get_tile_id(graph_row, graph_col, tile_rows, tile_cols, tile_count_c):
    tile_row = graph_row // tile_rows
    tile_col = graph_col // tile_cols
    t_id = tile_row * tile_count_c + tile_col
    return t_id 

def tile_row_column(graph_row, graph_col, tile_height, tile_width):
    # returns the row and column of the input tile that
    # underlies the graph row/column
    return graph_row % tile_height, graph_col % tile_width

def vertex_id2(row, col, width):
    return row * width + col

def neighbor_cost2(graph, v_id):
    # given an integer vertex_id, return the
    # neighbors as a list of (vertex_id,cost) tuples

    n_r, n_c = len(graph), len(graph[0])
    v_r, v_c = row_column(v_id, graph)
    neighbors = []
    for (dr,dc) in [(0,-1),(-1,0),(1,0),(0,1)]:
        (r,c) = (v_r + dr, v_c + dc)
        if r < 0 or c < 0 or r >= n_r or c >= n_c:
            continue # do not go off the grid
        neighbors.append((vertex_id(r,c,graph), graph[r][c]))
    return neighbors



# def part1(lines):
#     grid = parse(lines)
#     path = []
#     start = (0,0)
#     goal = (len(grid)-1, len(grid[0])-1)
#     best = random_shortest_path(grid, start, goal)
#     risk = min_path(grid, path, start, goal, 0, best)
#     return risk

# def random_shortest_path(grid, start, goal):
#     # go horizontal then vertical
#     # assume start is smaller than goal
#     # do not count start risk, do count goal risk
#     sr,sc = start
#     gr,gc = goal
#     risk = sum(grid[sr][sc+1:gc]) #row
#     for row in grid[sr+1:gr]: #column
#         risk += row[gc]
#     return risk

# def min_path(grid, path, start, goal, risk, best):
#     # print("path", path)
#     # print("start", start, "goal", goal, "risk", risk, "best", best)
#     if start == goal:
#         return risk # we did not enter this square
#     for (dr,dc) in [(0,-1),(-1,0),(1,0),(0,1)]:
#         (r,c) = (start[0] + dr, start[1] + dc)
#         if r < 0 or c < 0 or r > goal[0] or c > goal[1]:
#             continue # do not go off the grid
#         if (r,c) in path:
#             continue # do not visit a call twice. this would cause a loop, that could not be minimal
#         new_risk = risk + grid[r][c]
#         if new_risk + 1 >= best:
#             continue # skip paths that cannot beat our current best 
#         new_path = path.copy() + [(r,c)]
#         new_risk = min_path(grid, new_path, (r,c), goal, new_risk, best)
#         if new_risk < best:
#             best = new_risk
#     return best
    
if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    # print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
