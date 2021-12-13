# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a coordinate pair row,col that are stored in a list
# as integer tuples.  The list index is the "name" of the coordinate
# grid is matrix (list of lists) of integers -1 means no closest coordinate
# 0..n means that that is the closest coordinate pair

def part1(lines):
    coords = parse(lines)
    grid = build_grid(coords)
    fill_grid(grid, coords)
    # print(grid)
    area = largest_area(grid)
    return area

def part2(lines):
    coords = parse(lines)
    area = safe_area(coords)
    return area

def parse(lines):
    coords = []
    for line in lines:
        x,y = line.strip().split(", ")
        coords.append((int(x),int(y)))
    return coords

def build_grid(coords):
    min_x, min_y, max_x, max_y = get_bounds(coords)
    #print(min_x, min_y, max_x, max_y)
    x_size = max_x - min_x + 1
    y_size = max_y - min_y + 1
    grid = []
    for y in range (0, y_size):
        grid.append([-1] * x_size)
    for i in range(0,len(coords)):
        x,y = coords[i]
        grid[y-min_y][x-min_x] = i
    return grid

def fill_grid(grid, coords):
    min_x, min_y, max_x, max_y = get_bounds(coords)
    for gy, row in enumerate(grid):
        for gx, cell in enumerate(row):
            if cell > -1:
                continue
            closest = -1
            min_dist = max_x + max_y
            for i, coord in enumerate(coords):
                x,y = coord
                x = x - min_x
                y = y - min_y
                dist = abs(x-gx) + abs(y-gy)
                if dist < min_dist:
                    min_dist = dist
                    closest = i
                elif dist == min_dist:
                    closest = -1
            if closest > -1:
                grid[gy][gx] = closest

def fill_grid2(grid, coords):
    min_x, min_y, max_x, max_y = get_bounds(coords)
    for gy, row in enumerate(grid):
        for gx, cell in enumerate(row):
            if cell > -1:
                continue
            closest = -1
            min_dist = max_x + max_y
            for i, coord in enumerate(coords):
                x,y = coord
                x = x - min_x
                y = y - min_y
                dist = abs(x-gx) + abs(y-gy)
                if dist < min_dist:
                    min_dist = dist
                    closest = i
                elif dist == min_dist:
                    closest = -1
            if closest > -1:
                grid[gy][gx] = closest

def largest_area(grid):
    infinite = set() # a set of the indexes on the edges (they have infinite area and are ignored)
    areas = {} # a count by index of the non-infinite areas
    max_x = len(grid[0])
    max_y = len(grid)
    for y in range(0,max_y):
        for x in range(0,max_x):
            area = grid[y][x]
            if area == -1:
                continue
            if x == 0 or x == max_x -1:
                infinite.add(area)
                if area in areas: del areas[area]
            if y == 0 or y == max_y -1:
                infinite.add(area)
                if area in areas: del areas[area]
            if area in infinite:
                continue
            if area in areas:
                areas[area] += 1
            else:
                areas[area] = 1
    # print(areas)
    max_size = 0
    for size in areas.values():
        if size > max_size:
            max_size = size
    return max_size

def safe_area(coords):
    # I do not need a grid, I just look at all cells
    # in the bounds, and add it to the total if
    # it meets the distance criteria
    total = 0
    min_x, min_y, max_x, max_y = get_bounds(coords)
    for x in range(min_x,max_x+1):
        for y in range(min_y,max_y+1):
            dist = 0
            for cx,cy in coords:
                dist += abs(cx-x) + abs(cy-y)
                if dist >= MAX_DIST: break
            if dist < MAX_DIST:
                total += 1
    return total

def get_bounds(coords):
    min_x = min([x for x,_ in coords])
    min_y = min([y for _,y in coords])
    max_x = max([x for x,_ in coords])
    max_y = max([y for _,y in coords])
    return min_x, min_y, max_x, max_y

MAX_DIST = 10_000  # 32 for testing, 10_000 for input

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
