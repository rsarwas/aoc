"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    value = 50
    for item in data:
        value += item
        value %= 100
        if value == 0:
            total += 1
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = 0
    value = 50
    for item in data:
        # print(value, item)
        old_value = value
        value += item
        if item < 0:
            # Moving left to smaller numbers, usually if if the nev value is negative, then we have crossed
            # zero at least once, however this is not true if we start at zero.
            if old_value == 0:
                # item -1 to -99 => 0 (item//-100)
                # item -100 to -199 => 1 (item//-100)
                total += value // -100
            else:
                # if value > 0 then add nothing to total
                if value <= 0:
                    # x = original value; item = move in ();  new value = old_value - move
                    # if item in 1..x-1, then x + item is positive and zero count is 0;  i.e count = 0 if value + item > 0
                    # x-(x..100+x-1) = 1;  -99..0; count = 1 == (value + item)//-100 + 1
                    # x-(100+x..200+x-1) = 2: -199..-100;; 2 == (value + item)//-100 + 1
                    # ...  count of zeros = 2 == (value + item)//-100 + 1
                    total += 1 + value // -100
        else:  # rotate CW (positive item)
            # value = old_value + item (move count to right(+));  zero_count
            # value < 99 => zero_count = 0
            # value in 100..199 => zero_count = 1
            # value in 200..299 => zero_count = 2
            # ...  zero_count = value//100
            total += value // 100
        value %= 100
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        direction = -1 if line[0] == "L" else 1
        magnitude = int(line[1:])
        data.append(direction * magnitude)
    return data


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
