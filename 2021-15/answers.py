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

def part1(lines):
    grid = parse(lines)
    # dijkstra function assumes integer vertex ids
    start = vertex_id(0, 0, grid)
    target = vertex_count(grid) - 1
    dist, _ = dijkstra(grid, start, target)
    return dist[target]

def part2(lines):
    return -1

def parse(lines):
    grid = []
    for line in lines:
        row = [int(c) for c in line.strip()]
        grid.append(row)
    return grid

# See https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode
def dijkstra(graph, source, target):
    n = vertex_count(graph)
    vertices = set(range(0,n))
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    
    while vertices:
        # find vertex in vertices with min dist[u]
        dist_u, u = float('inf'), None
        for v in vertices:
            if dist[v] < dist_u:
                dist_u, u = dist[v], v
        # print("min dist[u]", u, dist_u)
        vertices.remove(u)
        if u == target:
            # print("Found target", u, dist[u])
            return dist, prev
        for v, cost in neighbor_cost(graph, u):
            if v not in vertices:
                continue
            alt = dist_u + cost
            # print("  neighbors u, v, cost", u, v, alt)
            if alt < dist[v]:              
                dist[v] = alt
                prev[v] = u
    return dist, prev

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

def neighbor_cost(graph, v_id):
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
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
