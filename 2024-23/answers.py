"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    # print(data)
    group3 = groups_of_three(data)
    # print(group3)
    computers = [c for c in data.keys() if c.startswith("t")]
    # print(computers)
    total = 0
    for c1, c2, c3 in group3:
        if c1 in computers or c2 in computers or c3 in computers:
            total += 1
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = {}
    for line in lines:
        computer1, computer2 = line.strip().split("-")
        if computer1 not in data:
            data[computer1] = []
        if computer2 not in data:
            data[computer2] = []
        data[computer1].append(computer2)
        data[computer2].append(computer1)
    return data


def groups_of_three(data):
    """Return a set of the 3-pules of interconnected keys in data"""
    groups = set()
    for computer1 in data:
        for index, computer2 in enumerate(data[computer1][:-1]):
            for computer3 in data[computer1][index + 1 :]:
                if computer3 in data[computer2]:
                    # add the three to a list/set, but make sure it is unique
                    computers = [computer1, computer2, computer3]
                    computers.sort()
                    groups.add((computers[0], computers[1], computers[2]))
    return groups


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
