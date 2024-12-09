"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.

# Note: The rules cannot be used to develop a complete correct ordering of pages
# because they are not a total ordering.  For example these rules:

# 49|67
# 64|49
# 57|64
# 33|57
# 67|33

# require that 67 must be printed before page 67.
# Therefore the rules can only be used to verify the correctness of an update
# which will not include all the pages that will result in a logical inconsistency


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
    rules, updates = parse(lines)
    total = 0
    for update in updates:
        rules_met, rules_unmet = match_rules(update, rules)
        if rules_unmet:
            update = fix_update(update, rules_met + rules_unmet)
            middle = update[len(update) // 2]
            total += middle
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

    valid_updates = []
    for update in updates:
        if good_update(update, rules):
            valid_updates.append(update)
    return valid_updates


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


def match_rules(update, rules):
    """Return a list of rules followed and rules broken"""
    good = []
    bad = []
    for rule in rules:
        try:
            if update.index(rule[1]) < update.index(rule[0]):
                bad.append(rule)
            else:
                good.append(rule)
        except ValueError:
            # rule doesn't apply, so ignore it
            continue
    return good, bad


def fix_update(update, applicable_rules):
    """Return the pages in update in the correct order.
    Sort the rules that apply.  There will be one page that is never listed
    as the first page in the applicable rules (it goes last).  There is only
    one page that is only listed once as the first page in the applicable rules
    it goes next to last....  The list can also be built in reverse order
    """
    counts = []
    for page in update:
        count = 0
        for rule in applicable_rules:
            if page == rule[0]:
                count += 1
        counts.append((count, page))
    counts.sort()
    counts.reverse()
    # print("counts", counts)
    update = [page for (_, page) in counts]
    return update


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
