"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"

WALL = "#"
OPEN = "."
UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"


def part1(lines):
    """Solve part 1 of the problem."""
    blizzards, start, finish, walls = parse(lines)
    print(blizzards, start, finish, walls)
    blizzards = update(blizzards, walls)
    print(blizzards)
    result = solve(blizzards)
    return result


def part2(lines):
    """Solve part 2 of the problem."""
    return -1


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    data = []
    left_wall, top_wall, right_wall, bottom_wall = 1e10, 1e10, 0, 0
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == WALL:
                if row < top_wall:
                    top_wall = row
                if row > bottom_wall:
                    bottom_wall = row
                if col < left_wall:
                    left_wall = col
                if col > right_wall:
                    right_wall = col
            elif char == OPEN:
                if row == top_wall:
                    start = (row, col)
                if row == bottom_wall:
                    finish = (row, col)
            else:
                blizzard = (row, col, char)
                data.append(blizzard)
    return data, start, finish, (left_wall, top_wall, right_wall, bottom_wall)


def solve(data):
    """Convert the input data structure into the result."""
    result = 0
    for item in data:
        result += len(item)
    return result


def update(blizzards, walls):
    """Given a list of blizzards, Update the location of each blizzard."""
    left, top, right, bottom = walls
    for i, blizzard in enumerate(blizzards):
        row, col, direction = blizzard
        if direction == UP:
            row -= 1
            if row == top:
                row = bottom - 1
        if direction == DOWN:
            row += 1
            if row == bottom:
                row = top + 1
        if direction == RIGHT:
            col += 1
            if col == right:
                col = left + 1
        if direction == LEFT:
            col -= 1
            if col == left:
                col = right - 1
        blizzards[i] = (row, col, direction)
    return blizzards


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
