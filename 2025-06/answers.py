"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import re  # for regular expression to remove extra spaces
import math  # for prod (returns the product of list items)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    operand_count = len(data) - 1
    operators = data[operand_count]
    operands = transpose(data[:-1])
    total = 0
    for index, operator in enumerate(operators):
        if operator == "+":
            total += sum(operands[index])
        if operator == "*":
            total += math.prod(operands[index])
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        new_line = re.sub(" +", " ", line)
        items = new_line.split(" ")
        if items[0] not in "*+":
            items = [int(x) for x in items]
        data.append(items)
    return data


def transpose(rows):
    """convert a list of rows into a list of columns"""
    columns = []
    for i in range(len(rows[0])):
        column = []
        for row in rows:
            column.append(row[i])
        columns.append(column)
    return columns


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
