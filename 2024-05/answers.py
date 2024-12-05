"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    rules, updates = parse(lines)
    valid_updates = filter_valid(updates, rules)
    total = 0
    for update in valid_updates:
        middle = update[len(update) // 2]
        total += middle
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    rules = []
    updates = []
    parse_rules = True
    for line in lines:
        line = line.strip()
        if line == "":
            parse_rules = False
            continue
        if parse_rules:
            first, second = line.split("|")
            rules.append((int(first), int(second)))
        else:
            update = [int(x) for x in line.split(",")]
            updates.append(update)
    return rules, updates


def filter_valid(updates, rules):
    """Return a list of only the updates that meet all the rules.
    This is a simple brute force check"""

    def good_update(update, rules):
        """Search the rules if a rule is found which is violated return False,
        if all the rules are checked as valid, return True"""
        for rule in rules:
            try:
                if update.index(rule[1]) < update.index(rule[0]):
                    return False
                # else rule is valid, keep checking
            except ValueError:
                # rule doesn't apply, so ignore it
                continue
        return True

    valid_updates = []
    for update in updates:
        if good_update(update, rules):
            valid_updates.append(update)
    return valid_updates


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
