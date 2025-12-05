"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    fresh, available = parse(lines)
    total = 0
    # print(fresh, available)
    for item in available:
        for start, end in fresh:
            if item >= start and item <= end:
                total += 1
                break
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    fresh, _ = parse(lines)
    fresh.sort()
    merged_fresh = merge(fresh)
    while len(merged_fresh) < len(fresh):
        fresh = merged_fresh
        merged_fresh = merge(fresh)
    total = 0
    for start, end in merged_fresh:
        size = end - start + 1
        total += size
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    fresh = []
    available = []
    parse_fresh = True
    for line in lines:
        line = line.strip()
        if not line:
            parse_fresh = False
            continue
        if parse_fresh:
            a, b = line.split("-")
            fresh.append((int(a), int(b)))
        else:
            available.append(int(line))
    return fresh, available


def merge(ranges):
    """Merges overlapping ranges"""
    ranges.sort()
    new_ranges = []
    index = 0
    while index < len(ranges):
        this_start, this_end = ranges[index]
        next = index + 1
        if next < len(ranges):
            that_start, that_end = ranges[next]
        while next < len(ranges) and that_start <= this_end:
            if that_end > this_end:
                this_end = that_end
            next += 1
            if next < len(ranges):
                that_start, that_end = ranges[next]
        new_ranges.append((this_start, this_end))
        index = next
    return new_ranges


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
