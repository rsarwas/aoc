# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    pairs = parse(lines)
    ps = proper_subsets(pairs)
    return len(ps)


def part2(lines):
    pairs = parse(lines)
    laps = overlaps(pairs)
    return len(laps)


def parse(lines):
    pairs = []
    for line in lines:
        line = line.strip()
        e1,e2 = line.split(",")
        e1 = [int(i) for i in e1.split("-")]
        e2 = [int(i) for i in e2.split("-")]
        pairs.append((e1, e2))
    return pairs


def proper_subsets(pairs):
    ps = []
    for pair in pairs:
        e1, e2 = pair
        if (e1[0] >= e2[0] and e1[1] <= e2[1]) or (e1[0] <= e2[0] and e2[1] <= e1[1]):
            ps.append(pair)
    return ps

def overlaps(pairs):
    laps = []
    for pair in pairs:
        e1, e2 = pair
        if (e1[0] >= e2[0] and e1[0] <= e2[1]) or \
         (e1[1] >= e2[0] and e1[1] <= e2[1]) or \
         (e2[0] >= e1[0] and e2[0] <= e1[1]) or \
         (e2[1] >= e1[0] and e2[1] <= e1[1]):
            laps.append(pair)
    return laps

if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
