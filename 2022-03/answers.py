# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    items = parse(lines)
    scores = [score(item) for item in items]
    return sum(scores)


def part2(lines):
    return -1

def parse(lines):
    items = []
    for line in lines:
        line = line.strip()
        line_mid = len(line)//2
        compartment1 = line[:line_mid]
        compartment2 = line[line_mid:]
        for item in compartment1:
            if item in compartment2:
                items.append(item)
                break
    return items


def score(item):
    """return 1..26 for a..z and 27..52 for A..Z"""
    val = ord(item)
    if val > 96: # a..
        return val - 96
    return val - 38


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
