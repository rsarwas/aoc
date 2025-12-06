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
    data = parse2(lines)
    operand_count = len(data) - 1
    operators = data[operand_count]
    op_pointers = find_non_spaces(operators)
    # print(data)
    # print(op_pointers)
    starts = op_pointers
    ends = [x - 1 for x in op_pointers[1:]] + [len(data[0])]
    total = 0
    for start, end in zip(starts, ends):
        operands = []
        for row in data[:-1]:
            operands.append(row[start:end])
        total += compute(operands, operators[start])
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


def parse2(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.replace("\n", "")
        data.append(line)
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


def find_non_spaces(s):
    """Return a list of ints that are indexes to the non space chars in the input string"""
    pointers = []
    for i, char in enumerate(s):
        if char != " ":
            pointers.append(i)
    return pointers


def compute(operands, operator):
    """Return result of the operation"""
    # print(operands, operator)
    operands = funkify(operands)
    # print(operands)
    if operator == "+":
        return sum(operands)
    return math.prod(operands)


def funkify(operands):
    """Return a list of ints from the list of strings"""
    new_operands = []
    for i in range(len(operands[0])):
        n = ""
        for row in operands:
            n += row[i]
        n = int(n)
        new_operands.append(n)
    return new_operands


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
