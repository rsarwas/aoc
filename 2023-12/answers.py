"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    match = 0
    partial_match = 0
    for spring_row in data:
        s1, g1 = spring_row
        # s1, g1 = fix_for_part2(spring_row)
        new = s1.replace("?", "#")
        g2 = count_contiguous_damaged(new)
        if len(g2) == len(g1):
            total += 1
        if g1 == g2:
            match += 1
        elif g1[0] == g2[0] or g1[-1] == g2[-1]:
            partial_match += 1
    print(f"match = {match}; partial_match = {partial_match}")
    # print(count_contiguous_damaged(new), spring_row[1])
    # new2 = spring_row[0].replace("?", ".")
    # print(count_contiguous_damaged(new2), spring_row[1])
    # perms = find_permutation_count(spring_row)
    # total += perms
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
        springs, groups = line.split(" ")
        groups = [int(item) for item in groups.split(",")]
        data.append((springs, groups))
    return data


def fix_for_part2(spring_row):
    s1, g1 = spring_row
    g2 = g1 * 5
    s2 = "?".join([s1] * 5)
    return (s2, g2)


def find_permutation_count(spring_row):
    """Return the number of valid permutations of sprint row data
    sprint_row is a (string, list) tuple, where string is a set of
    OPERATIONAL, DAMAGED AND UNKNOWN. list contains the size of each
    contiguous group of damaged springs."""
    springs, groups = spring_row
    count = 0
    for test_springs in perms(springs):
        test_groups = count_contiguous_damaged(test_springs)
        if test_groups == groups:
            count += 1
    return count


def perms(springs):
    l = 0
    for c in springs:
        if c == UNKNOWN:
            l += 1
    options = []
    for i in range(2**l):
        rep = new_str(i, l)
        o = []
        i = 0
        for c in springs:
            if c == UNKNOWN:
                o.append(rep[i])
                i += 1
            else:
                o.append(c)
        options.append("".join(o))
    return options


def count_contiguous_damaged(s):
    g = [ss for ss in s.split(".") if ss]
    return [len(i) for i in g]


def new_str(i, l):
    zero = "." * l
    if i == 0:
        return zero
    rem = ""
    while i > 0:
        if i % 2 == 1:
            rem = "#" + rem
        else:
            rem = "." + rem
        i = i // 2
    return (zero + rem)[-l:]  # (zero + rem)[:-l]


def testperms(l):
    for i in range(2**l):
        rep = new_str(i, l)
        print(f"{i}: {new_str(i, l)}")


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
    # print(perms("???.###"))
    # for l in [1, 2, 3]:
    #     print(f"-----{l}--------")
    #     testperms(l)
