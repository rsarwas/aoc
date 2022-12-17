# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    valves, tunnels = parse(lines)
    print(valves)
    print(tunnels)
    result = solve(valves, tunnels)
    return result


def part2(lines):
    return -1


def parse(lines):
    valves = []

    tunnels = set()
    # Valve BL has flow rate=0; tunnels lead to valves AA, ZD
    for line in lines:
        line = line.strip().replace("Valve ", "").replace(" has flow rate=", ", ")
        line = line.strip().replace("; tunnels lead to valves ", ", ").replace("; tunnel leads to valve ", ", ")
        items = line.split(", ")
        valve = {"name": items[0], "rate": items[1], "open": False}
        valves.append(valve)
        end1 = items[0]
        for end2 in items[2:]:
            if end1 < end2:
                tunnel = (end1, end2)
            else:
                tunnel = (end2, end1)
            tunnels.add(tunnel)
    return valves, tunnels


def solve(data, d2):
    result = 0
    for item in data:
        result += len(item)
    return result

def perms(xs):
    if len(xs) == 1:
        return xs
    if len(xs) == 2:
        return [xs, [xs[1],xs[0]]]
    p = []
    for i in range(len(xs)):
        p += [[xs[i]] + l for l in perms(xs[:i]+ xs[i+1:])]
    return p

def iperms(n):
    if n == 1:
        return [[0]]
    c = []
    for x in iperms(n-1):
        for a in range(n):
            c.append(x + [a])
    return c



if __name__ == '__main__':
    #lines = open("test.txt").readlines()
    #print(f"Part 1: {part1(lines)}")
    #print(f"Part 2: {part2(lines)}")
    print(len(perms([1,2,3,4,5,6,7,8])))
