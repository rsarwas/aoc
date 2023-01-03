# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    items = parse(lines)
    scores = [score(item) for item in items]
    return sum(scores)


def part2(lines):
    items = parse2(lines)
    scores = [score(item) for item in items]
    return sum(scores)


def parse(lines):
    items = []
    for line in lines:
        line = line.strip()
        line_mid = len(line) // 2
        compartment1 = line[:line_mid]
        compartment2 = line[line_mid:]
        for item in compartment1:
            if item in compartment2:
                items.append(item)
                break
    return items


def parse2(lines):
    badges = []
    for i in range(0, len(lines), 3):
        line1 = lines[i]
        line2 = lines[i + 1]
        line3 = lines[i + 2]
        matches = []
        for item in line1:
            if item in line2:
                matches.append(item)
        for item in matches:
            if item in line3:
                badges.append(item)
                break
    return badges


def score(item):
    """return 1..26 for a..z and 27..52 for A..Z"""
    val = ord(item)
    if val > 96:  # a..
        return val - 96
    return val - 38


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
