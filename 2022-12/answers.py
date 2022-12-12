# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# grid is a matrix of elevations (0..25)
# locations are (row,col) tuples where row and col are valid indices in grid

def part1(lines):
    grid, start, end = parse(lines)
    # print(start, end, grid)
    dist = min_path(grid, start, end)
    return dist


def part2(lines):
    grid, start, end = parse(lines)
    min_dist = 1e10
    starts = locations_minimal_elevation(grid)
    for start in starts:    
        dist = min_path(grid, start, end)
        if dist < min_dist:
            min_dist = dist
    return min_dist


def parse(lines):
    grid = []
    start = None
    end = None
    for row, line in enumerate(lines):
        line = line.strip()
        heights = [ord(char) - ord("a") for char in list(line)]
        if "S" in line:
            col = line.index("S")
            start = (row, col)
            heights[col] = 0
        if "E" in line:
            col = line.index("E")
            end = (row, col)
            heights[col] = 25
        grid.append(heights)
    return grid, start, end


def min_path(grid, start, end):
    """Dijkstra Sortest Path Algorithm
    wieght between nodes is always one (1) and
    we can only move up,down, left right, one space, so distance is always one (1)
    for part one, AEG (accumulated elevation gain) doesn't matter, just
    looking for the shortest distance, that follows the rule can increase more than 1"""
    # path = []
    F = {start}
    S = set()
    d = {start: 0} 
    while F:
        f = pop_minimum(F,d)
        if f == end:
            return d[f]
        S.add(f)
        # path.append(f)
        for loc in valid_locations(grid,f):
            dist = d[f] + 1
            if loc not in S and loc not in F:
                d[loc] = dist
                F.add(loc)
            else:
                if dist < d[loc]:
                    d[loc] = dist
    return 1e10 #no path found


def pop_minimum(F,d):
    m = None
    dist = 1e10
    for f in F:
        if d[f] < dist:
            m = f
            dist = d[f]
    F.remove(m)
    return m


def valid_locations(grid,f):
    neighbors = []
    my_ht = grid[f[0]][f[1]]
    for delta in [(-1,0),(1,0),(0,-1),(0,1)]:
        r,c = f[0] + delta[0], f[1] + delta[1]
        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r]):
            ht = grid[r][c]
            if ht <= my_ht+1:
                neighbors.append((r,c))
    return neighbors


def locations_minimal_elevation(grid):
    locs = []
    for r,row in enumerate(grid):
        for c,ht in enumerate(row):
            if ht == 0:
                locs.append((r,c))
    return locs


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
