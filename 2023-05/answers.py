"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
START = "seed"
END = "location"


def part1(lines):
    """Solve part 1 of the problem."""
    seeds, transforms = parse(lines)
    locations = [find_value(START, END, seed, transforms) for seed in seeds]
    return min(locations)


def part2(lines):
    """Solve part 2 of the problem."""
    total = -1
    return min(total, len(lines))


def parse(lines):
    """Parse the input lines into a list of seeds and transformations"""
    data = "".join(lines).strip()
    sections = data.split("\n\n")
    seeds = sections[0].strip().replace("seeds: ", "").split(" ")
    seeds = [int(seed) for seed in seeds]
    transforms = {}
    for section in sections[1:]:
        source, destination, ranges = parse_section(section)
        transforms[source] = (destination, ranges)
    return (seeds, transforms)


def parse_section(section):
    """Parse a transformation section of the input into the identifying names and the map"""
    lines = section.split("\n")
    source, destination = lines[0].strip().replace(" map:", "").split("-to-")
    maps = []
    for line in lines[1:]:
        dest, src, length = [int(item) for item in line.strip().split(" ")]
        maps.append((dest, src, length))
    return (source, destination, maps)


def find_value(start_name, end_name, seed, transforms):
    """Find the final transformed value (at end_name) of the seed"""
    end_value = seed
    while start_name != end_name:
        # print(f"{start_name} {end_value} ->")
        start_name, ranges = transforms[start_name]
        end_value = transform(end_value, ranges)
        # print(f"   {start_name} {end_value}")
    return end_value


def transform(end_value, ranges):
    """Transform a single value given its range map"""
    for dest, src, length in ranges:
        if src <= end_value <= src + length:
            new_end_value = dest + (end_value - src)
            return new_end_value
    return end_value


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
