"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    total = 0
    parts = find_part_numbers(lines)
    symbols = find_symbols(lines)
    for part in parts:
        if symbol_adjacent(part, symbols):
            total += part[0]
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    total = 0
    parts = find_part_numbers(lines)
    gears = find_gears(lines)
    for gear in gears:
        numbers = find_adjacent_parts(gear, parts)
        if len(numbers) == 2:
            ratio = numbers[0] * numbers[1]
            total += ratio
    return total


def find_part_numbers(lines):
    """Return the numbers and the location (row, start, end) of all the parts in the input"""
    numbers = []
    for row, line in enumerate(lines):
        in_number = False
        for i, c in enumerate(line):
            if c in "0123456789":
                if not in_number:
                    start = i
                    in_number = True
            else:
                if in_number:
                    end = i
                    number = int(line[start:end])
                    numbers.append((number, row, start, end))
                    in_number = False
    return numbers


def find_symbols(lines):
    """Return the locations (row,col) of all the symbols"""
    symbols = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char not in ".0123456789\n":
                symbols.add((row, col))
    return symbols


def find_gears(lines):
    """Return the locations (row,col) of all the '*' symbols"""
    gears = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "*":
                gears.append((row, col))
    return gears


def symbol_adjacent(part, symbols):
    """Return True IFF part is adjacent to any symbol"""
    (_, row, start, end) = part
    for r in range(row - 1, row + 2):
        for c in range(start - 1, end + 1):
            if r < 0 or c < 0:
                # ignore off the gird (optional)
                continue
            if r == row and start <= c < end:
                # ignore spaces occupied by number (optional)
                continue
            if (r, c) in symbols:
                return True
    return False


def find_adjacent_parts(gear, parts):
    """Return a list of parts that are adjacent to the gear"""
    numbers = []
    r, c = gear
    for part in parts:
        number, row, start, end = part
        if r in (row - 1, row, row + 1) and (start - 1 <= c <= end):
            numbers.append(number)
    return numbers


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
