"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
NS_PIPE = "|"  # a vertical pipe connecting north and south.
EW_PIPE = "-"  # a horizontal pipe connecting east and west.
NE_BEND = "L"  # a 90-degree bend connecting north and east.
NW_BEND = "J"  # a 90-degree bend connecting north and west.
SW_BEND = "7"  # a 90-degree bend connecting south and west.
SE_BEND = "F"  # a 90-degree bend connecting south and east.
GROUND = "."  # ground; there is no pipe in this tile.
START = "S"  # the starting position; there is an unknown but fully connected pipe here


def part1(lines):
    """Solve part 1 of the problem."""
    grid = [line.strip() for line in lines]
    loop = set()  # a set has a faster check for membership than a list
    start = find_start(grid)
    loop.add(start)
    next_pipe, _ = decode_start(start, grid)
    loop.add(next_pipe)
    prev_pipe = start
    while next_pipe != start:
        next_pipe, prev_pipe = find_adjacent(next_pipe, prev_pipe, grid)
        loop.add(next_pipe)
    # To traverse the loop, you would visit each location in loop once.
    # The furthest point will be halfway around in each direction, or half the loop size
    return len(loop) // 2


def part2(lines):
    """Solve part 2 of the problem."""
    grid = [line.strip() for line in lines]
    loop = set()  # a set has a faster check for membership than a list
    start = find_start(grid)
    loop.add(start)
    next_pipe, start_type = decode_start(start, grid)
    fix_grid(start, start_type, grid)
    loop.add(next_pipe)
    prev_pipe = start
    while next_pipe != start:
        next_pipe, prev_pipe = find_adjacent(next_pipe, prev_pipe, grid)
        loop.add(next_pipe)
    return count_interior_tiles(loop, grid)


def find_start(grid):
    """Return the row and column index into the grid, where START is located."""
    for row, line in enumerate(grid):
        for column, char in enumerate(line):
            if char == START:
                return (row, column)
    # should never happen
    return (-1, -1)


def decode_start(start, grid):
    """Find the two adjacent pipes that are connected to the START.
    This is trickier than the a normal find adjacent, because we to
    not know what type of pipe is in START"""
    max_row = len(grid)
    max_col = len(grid[0])
    s_row, s_col = start
    adjacent = []
    # try NORTH
    if s_row - 1 >= 0:
        loc = (s_row - 1, s_col)
        pipe = grid[loc[0]][loc[1]]
        if pipe in (NS_PIPE, SW_BEND, SE_BEND):
            adjacent.append(("N", loc))
    # try SOUTH
    if s_row + 1 < max_row:
        loc = (s_row + 1, s_col)
        pipe = grid[loc[0]][loc[1]]
        if pipe in (NS_PIPE, NW_BEND, NE_BEND):
            adjacent.append(("S", loc))
    # try West
    if s_col - 1 >= 0:
        loc = (s_row, s_col - 1)
        pipe = grid[loc[0]][loc[1]]
        if pipe in (EW_PIPE, NE_BEND, SE_BEND):
            adjacent.append(("W", loc))
    # try East
    if s_col + 1 < max_col:
        loc = (s_row, s_col + 1)
        pipe = grid[loc[0]][loc[1]]
        if pipe in (EW_PIPE, NW_BEND, SW_BEND):
            adjacent.append(("E", loc))
    if len(adjacent) != 2:
        # This should never happen
        print(f"Error: invalid start: start = {start}, adjacent = {adjacent}")
    start_type = determine_mystery_type(adjacent)
    print(start_type)
    return (adjacent[0][1], start_type)


def determine_mystery_type(adjacent):
    """Return the type of the pipe with connections in the adjacent tiles."""
    dir1, _ = adjacent[0]
    dir2, _ = adjacent[1]
    # WARNING: not all combinations are tested because they are not possible
    # due to the search order in decode_start.  if decode_start changes, this
    # code will need to be reviewed and probably changed.""
    if dir1 == "N":
        if dir2 == "W":
            return NW_BEND
        if dir2 == "E":
            return NE_BEND
        if dir2 == "S":
            return NS_PIPE
    if dir1 == "S":
        if dir2 == "W":
            return SW_BEND
        if dir2 == "E":
            return SE_BEND
    if dir1 == "W":
        if dir2 == "E":
            return EW_PIPE
    # This should never happen
    print(f"Error determning start type: dir1 = {dir1}, dir2 = {dir2}")
    return None


# pylint: disable=too-many-return-statements
def find_adjacent(this_pipe, prev_pipe, grid):
    """Find the next pipe after this_pipe, coming from prev_pipe.
    Return (next_pipe, this_pipe) to facilitate the next search"""
    # I don't worry about going off the grid, because that would be invalid input
    # I don't worry about finding a ground or a start - invalid loop
    t_row, t_col = this_pipe
    pipe = grid[t_row][t_col]
    if pipe == NS_PIPE:
        north = (t_row - 1, t_col)
        south = (t_row + 1, t_col)
        if prev_pipe == north:
            return (south, this_pipe)
        return (north, this_pipe)
    if pipe == EW_PIPE:
        west = (t_row, t_col - 1)
        east = (t_row, t_col + 1)
        if prev_pipe == west:
            return (east, this_pipe)
        return (west, this_pipe)
    if pipe == NE_BEND:
        north = (t_row - 1, t_col)
        east = (t_row, t_col + 1)
        if prev_pipe == north:
            return (east, this_pipe)
        return (north, this_pipe)
    if pipe == NW_BEND:
        north = (t_row - 1, t_col)
        west = (t_row, t_col - 1)
        if prev_pipe == north:
            return (west, this_pipe)
        return (north, this_pipe)
    if pipe == SE_BEND:
        south = (t_row + 1, t_col)
        east = (t_row, t_col + 1)
        if prev_pipe == south:
            return (east, this_pipe)
        return (south, this_pipe)
    if pipe == SW_BEND:
        south = (t_row + 1, t_col)
        west = (t_row, t_col - 1)
        if prev_pipe == south:
            return (west, this_pipe)
        return (south, this_pipe)
    # This should never happen
    print("Error", this_pipe, pipe)
    return (None, None)


# pylint: disable=too-many-branches
def count_interior_tiles(loop, grid):
    """An interior tile has an odd number of perpendicular pipes between it and the edge.
    An exterior tile has an even (or zero number of perpendicular pipes between it and the edge)
    Only count the pipes in the loop, ignore the ground and other pipes not in the main loop.
    If counting up/down, do not count NS_PIPE. IF counting left/right do not count EW_PIPE.
    A tile that is on the loop is not an interior tile.  If a tile is not on the loop it must
    have an even number of bends between it and the edge.  An S bend counts as 1, a U bend
    counts as 2.

    Algorithm: look at each row, from left to right
    skip all perimeter tiles (nothing on the edge can be interior)
    if the tile is on the main loop, update the vertical pipe count
    otherwise, if the vertical pipe count is odd it is interior
    to update the vertical pipe count:
    ignore EW_PIPE, +1 for NW PIPE
    keep track of the last unmatched bend (from south, from north, none)
    if none, then +1 to pipe count, and save as last unmatched pipe
    if from S (N) and we are going back S (N) +1 to pipe count and last unmatched is None
    if from S (N) and we aer continuing N (S), then +0 to pipe count and last unmatched is None
    """
    interior_count = 0
    for row, line in enumerate(grid[:-1]):
        if row == 0:
            continue
        vert_count = 0
        last_dir = None  # vertical direction of the last bend {None, 'N', 'S'}
        for col, tile in enumerate(line[:-1]):
            if (row, col) in loop:
                if tile in (NS_PIPE):
                    vert_count += 1
                elif tile in (NW_BEND, NE_BEND):
                    if last_dir is None:
                        vert_count += 1
                        last_dir = "N"
                    elif last_dir == "S":
                        last_dir = None
                    else:  # last_dir == "N" (U-Turn)
                        vert_count += 1
                        last_dir = None
                elif tile in (SW_BEND, SE_BEND):
                    if last_dir is None:
                        vert_count += 1
                        last_dir = "S"
                    elif last_dir == "N":
                        last_dir = None
                    else:  # last_dir == "S" (U-Turn)
                        vert_count += 1
                        last_dir = None
                else:
                    # EW_PIPE - ignore
                    pass
            else:
                if vert_count % 2 == 1:
                    # print("interior", row, col, vert_count, last_dir)
                    interior_count += 1
    return interior_count


def fix_grid(start, start_type, grid):
    """Replace the START with the correct pipe type.
    This is required for the counting of interior tiles"""
    pass


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
