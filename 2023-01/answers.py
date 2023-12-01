"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    total = 0
    for line in lines:
        total += number_in(line)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    total = 0
    for line in lines:
        total += number_in_with_text(line)
    return total


def number_in(line):
    """Finds the number in the line.
    It is a two digit number. the tens value is the first number in the line
    The ones digit is the last number in the line"""

    digit1 = None
    digit2 = None
    for char in line:
        if char in "0123456789":
            if digit1 is None:
                digit1 = int(char)
            digit2 = int(char)
    return 10 * digit1 + digit2


def number_in_with_text(line):
    """Finds the number in the line.
    It is a two digit number. the tens value is the first number in the line
    The ones digit is the last number in the line.
    A number can either be a 0,1,2,3... or one, two, three, .."""

    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    index_digit1 = None
    digit1 = None
    index_digit2 = None
    digit2 = None
    for index, char in enumerate(line):
        if char in "0123456789":
            if digit1 is None:
                digit1 = int(char)
                index_digit1 = index
            digit2 = int(char)
            index_digit2 = index
    for digit, name in enumerate(digits):
        start = line.find(name)
        if -1 < start < index_digit1:
            index_digit1 = start
            digit1 = digit + 1
        end = line.rfind(name)
        if end > -1 and end > index_digit2:
            index_digit2 = end
            digit2 = digit + 1
    return 10 * digit1 + digit2


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
