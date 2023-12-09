"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    sequences = parse(lines)
    total = 0
    for sequence in sequences:
        total += next_item(sequence)
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
        items = [int(a) for a in line.split(" ")]
        data.append(items)
    return data


def next_item(sequence):
    """A recursive algorithm to find the next item in a sequence of integers."""
    if all_zeros(sequence):
        return 0
    return sequence[-1] + next_item(difference(sequence))


def difference(sequence):
    """Return a sequence of differences between adjacent items in sequence."""
    answer = []
    for i, item in enumerate(sequence[:-1]):
        diff = sequence[i + 1] - item
        answer.append(diff)
    return answer


def all_zeros(sequence):
    """Return True if all the items in the sequence are zeros."""
    for item in sequence:
        if item != 0:
            return False
    return True


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
