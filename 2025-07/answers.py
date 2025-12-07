"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    start = data[0].index("S")
    beams = set([start])
    total = 0
    for row in data[1:]:
        # bl = list(beams)
        # bl.sort()
        # print(bl)
        for index, char in enumerate(row):
            if char == "^" and index in beams:
                total += 1
                beams.remove(index)
                beams.add(index - 1)
                beams.add(index + 1)

    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    start = data[0].index("S")
    memory = {}
    total = count_timelines(data, 1, start, memory)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        data.append(line)
    return data


def count_timelines(data, row, column, memory):
    """Count the number of timelines with recursion"""
    # solution was too slow without memoization
    if (row, column) in memory:
        return memory[(row, column)]
    if row == len(data):
        memory[(row, column)] = 1
        return 1
    if data[row][column] == ".":
        count = count_timelines(data, row + 1, column, memory)
        memory[(row, column)] = count
        return count
    else:
        left = count_timelines(data, row, column - 1, memory)
        right = count_timelines(data, row, column + 1, memory)
        count = left + right
        memory[(row, column)] = count
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
