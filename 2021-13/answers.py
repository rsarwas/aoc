# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# coords is a list of (x:int,y:int) tuples
# folds is a list of tuples (axis:char, amount:int), where axis = {'x', 'y'}
#

def part1(lines):
    coords,folds = parse(lines)
    # print(coords)
    # print(folds)
    max_x, max_y = get_bounds(coords)
    # print(max_x, max_y)
    grid = build(max_x, max_y, coords)
    # print_grid(grid)
    for fold in folds[:1]:
        grid = fold_grid(grid, fold)
        # print(fold)
        # print_grid(grid)
    count = count_dots(grid)
    return count

def part2(lines):
    coords,folds = parse(lines)
    max_x, max_y = get_bounds(coords)
    grid = build(max_x, max_y, coords)
    for fold in folds:
        grid = fold_grid(grid, fold)
    print_grid(grid)
    return "ARHZPCUH"

def parse(lines):
    coords = []
    folds = []
    doing_folds = False
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            doing_folds = True
            continue
        if doing_folds:
            line = line.replace("fold along ","")
            axis,amount = line.split("=")
            folds.append((axis,int(amount)))
        else:
            x,y = line.split(",")
            coords.append((int(x),int(y)))
    return coords, folds

def get_bounds(coords):
    max_x = max([x for x,_ in coords])
    max_y = max([y for _,y in coords])
    return max_x, max_y

def build(max_x, max_y, coords):
    # X is the length of a row, Y is the number of rows
    grid = []
    for _ in range(0,max_y+1):
        row = [False] * (max_x + 1)
        grid.append(row)
    for x,y in coords:
        grid[y][x] = True
    return grid

def fold_grid(grid, fold):
    # fold the grid up (for horizontal fold[0] == 'y') or left (for vertical fold[0] == 'y')
    # the amount (fold[1]) is the index of the row ('y'), or the column ('x') where the fold
    # happens. if the fold is 'y',7, the new grid will have rows 0..6, not row 7, row 8 -> row 6, etc
    if fold[0] == 'x':
        return fold_left(grid, fold[1])
    if fold[0] == 'y':
        return fold_up(grid, fold[1])
    return grid

def fold_up(grid, y_axis):
    new_grid = []
    for row in range(0,y_axis):
        new_grid.append(grid[row].copy())
    max_y = y_axis*2
    for row in range(y_axis+1, max_y+1):
        old_row = max_y - row
        for i,c in enumerate(grid[row]):
            new_grid[old_row][i] |= c
    return new_grid

def fold_left(grid, x_axis):
    new_grid = []
    for row in grid:
        new_grid.append(row[:x_axis])
    max_x = x_axis*2
    for r, row in enumerate(grid):
        for c_i in range(x_axis+1, max_x+1):
            old_c_i = max_x - c_i
            new_grid[r][old_c_i] |= row[c_i]
    return new_grid

def count_dots(grid):
    total = 0
    for row in grid:
        for c in row:
            if c:
                total += 1
    return total

def print_grid(grid):
    for row in grid:
        print(''.join(['#' if cell else '.' for cell in row]))

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
