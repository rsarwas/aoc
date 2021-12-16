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
    path = []
    start = (0,0)
    goal = (len(grid)-1, len(grid[0])-1)
    best = random_shortest_path(grid, start, goal)
    risk = min_path(grid, path, start, goal, 0, best)
    return risk

def part2(lines):
    return -1

def parse(lines):
    grid = []
    for line in lines:
        row = [int(c) for c in line.strip()]
        grid.append(row)
    return grid

def random_shortest_path(grid, start, goal):
    # go horizontal then vertical
    # assume start is smaller than goal
    # do not count start risk, do count goal risk
    sr,sc = start
    gr,gc = goal
    risk = sum(grid[sr][sc+1:gc]) #row
    for row in grid[sr+1:gr]: #column
        risk += row[gc]
    return risk

def min_path(grid, path, start, goal, risk, best):
    # print("path", path)
    # print("start", start, "goal", goal, "risk", risk, "best", best)
    if start == goal:
        return risk # we did not enter this square
    for (dr,dc) in [(0,-1),(-1,0),(1,0),(0,1)]:
        (r,c) = (start[0] + dr, start[1] + dc)
        if r < 0 or c < 0 or r > goal[0] or c > goal[1]:
            continue # do not go off the grid
        if (r,c) in path:
            continue # do not visit a call twice. this would cause a loop, that could not be minimal
        new_risk = risk + grid[r][c]
        if new_risk + 1 >= best:
            continue # skip paths that cannot beat our current best 
        new_path = path.copy() + [(r,c)]
        new_risk = min_path(grid, new_path, (r,c), goal, new_risk, best)
        if new_risk < best:
            best = new_risk
    return best
    
if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
