"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    map = parse(lines)
    starts, ends = find_terminals(map)
    total = 0
    for start in starts:
        total += counts_trails(start, ends, map)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    map = parse(lines)
    starts, ends = find_terminals(map)
    total = 0
    for start in starts:
        total += rate_trailhead(0, start, map)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        row = [int(c) for c in line]
        data.append(row)
    return data


def find_terminals(map):
    """Return a list of the coordinates in the map of all the
    trailheads (value == 0), and all the trailends (value == 9)"""
    starts = []
    ends = []
    for r, row in enumerate(map):
        for c, height in enumerate(row):
            if height == 0:
                starts.append((r, c))
            if height == 9:
                ends.append((r, c))
    return starts, ends


def counts_trails(start, ends, map):
    """Return the number of unique locations in ends that can be reached from start.
    A trail has to have adjacent locations that increase in height by 1 at each step"""
    count = 0
    for end in ends:
        if within_reach(start, end):
            if has_trail(0, start, end, map):
                count += 1
    return count


def within_reach(start, end):
    """Return True is end is within 9 spaces (taxicab distance) of start"""
    dr = abs(start[0] - end[0])
    dc = abs(start[1] - end[1])
    return dr + dc <= 9


def has_trail(start_height, start, end, map):
    """Return True if we can find a trail from start to end
    A trail has adjacent squares (up/down/left/right) that increase
    in height by 1 unit from start to end.
    This function will be called recursively, so we can find trails of
    any length, and we do not assume a starting height of 0"""
    if start_height == 9:
        return start == end
    else:
        r, c = start
        height = start_height + 1
        if r - 1 >= 0 and map[r - 1][c] == height:
            if has_trail(height, (r - 1, c), end, map):
                return True
        if r + 1 < len(map) and map[r + 1][c] == height:
            if has_trail(height, (r + 1, c), end, map):
                return True
        if c - 1 >= 0 and map[r][c - 1] == height:
            if has_trail(height, (r, c - 1), end, map):
                return True
        if c + 1 < len(map[r]) and map[r][c + 1] == height:
            if has_trail(height, (r, c + 1), end, map):
                return True
    return False


def rate_trailhead(start_height, start, map):
    """Return the number of distinct trails starting at start and ending at
    any trail end (height == 9).
    A trail has adjacent squares (up/down/left/right) that increase
    in height by 1 unit from start to end.
    This function will be called recursively, so we can find trails of
    any length, and we do not assume a starting height of 0"""
    count = 0
    if start_height == 9:
        count = 1
    else:
        count = 0
        r, c = start
        height = start_height + 1
        if r - 1 >= 0 and map[r - 1][c] == height:
            count += rate_trailhead(height, (r - 1, c), map)
        if r + 1 < len(map) and map[r + 1][c] == height:
            count += rate_trailhead(height, (r + 1, c), map)
        if c - 1 >= 0 and map[r][c - 1] == height:
            count += rate_trailhead(height, (r, c - 1), map)
        if c + 1 < len(map[r]) and map[r][c + 1] == height:
            count += rate_trailhead(height, (r, c + 1), map)
    return count


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
