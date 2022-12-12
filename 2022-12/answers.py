# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# grid is a matrix of elevations (0..25)
# locations are (row,col) tuples where row and col are valid indices in grid

def part1(lines):
    grid, start, end = parse(lines)
    dist = min_path_dist(grid, start, end)
    return dist


def part2(lines):
    grid, start, end = parse(lines)
    min_dist = 1e10
    starts = locations_minimal_elevation(grid)
    for start in starts:    
        dist = min_path_dist(grid, start, end)
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


def min_path_dist(grid, start, end):
    """Dijkstra Sortest Path Algorithm
    S is the settled set (nodes with an established minimum distance)
    F is the frontier set (nodes we know about, but are not settled)
    the grid contains all the nodes (the far-off set is the grid minus S and F)
    There is a path between a point on the grid and the 4 adjacent points (up, down,
    left right) if the elevation of the adjacent point is less than or equal to the
    elevation of the current point.  All paths have a weight of one (1).
    d is the distance (sum of the weights to get from start to the current node).
    We are done once we get a distance to the end node.  If we run out of adjacent
    nodes without finding the end node, then there is not path from start to end.
    Note 1: there may be several paths of equal distance.  I am not asked to pick a path.
    Note 2: AEG (accumulated elevation gain) doesn't matter, just
    looking for the shortest 2-D distance."""
    F = {start}
    S = set()
    d = {start: 0} 
    while F:
        f = pop_minimum(F,d)
        if f == end:
            return d[f]
        S.add(f)
        for loc in valid_locations(grid,f):
            dist = d[f] + 1
            if loc not in S and loc not in F:
                d[loc] = dist
                F.add(loc)
            else:
                if dist < d[loc]:
                    d[loc] = dist
    return 1e10  # No path found


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
