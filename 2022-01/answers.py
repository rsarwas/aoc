"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# Each line is an integer or empty (just a newline).
# There is no empty line at the end
# _totals_ is list of integers. Each one is the sum of a group of
# integers in the input. Groups are separated by an empty line.


def part1(lines):
    """Solve part 1 of the problem."""
    totals = totalize_calories(lines)
    return max(totals)


def part2(lines):
    """Solve part 2 of the problem."""
    totals = totalize_calories(lines)
    totals.sort()
    top_three = totals[-3:]
    return sum(top_three)


def totalize_calories(lines):
    """Read the calories in each line and provide a total for each group.
    The calories for each group are sequential and separated by a blank line.
    The calories for the (n+1)th group are after the nth blank line.
    Return a list of totals for each group."""
    totals = []
    group_total = 0
    for line in lines:
        line = line.strip()
        if line:
            # Add this amount to the current group's total.
            group_total += int(line)
        else:
            # We are done with totalizing a group. Save it and start a new group
            totals.append(group_total)
            group_total = 0
    # Add any remaining group total to the list.
    if group_total > 0:
        totals.append(group_total)
    return totals


def main(filename):
    """Solve both parts of the puzzle."""
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
        print(f"Solving Advent of Code with {filename}")
        print(f"Part 1: {part1(lines)}")
        print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
