# Data Model:
# ===========

def parse(lines):
    connections = {}
    for line in lines:
        destination, input = parse_line(line)
        connections[destination] = input
    return connections


def parse_line(line):
    input, destination = line.strip().split(" -> ")
    if "AND" in input:
        left, right = input.split(" AND ")
        input = (left, "AND", right)
    elif "OR" in input:
        left, right = input.split(" OR ")
        input = (left, "OR", right)
    elif "LSHIFT" in input:
        left, right = input.split(" LSHIFT ")
        input = (left, "LSHIFT", right)
    elif "RSHIFT" in input:
        left, right = input.split(" RSHIFT ")
        input = (left, "RSHIFT", right)
    elif input.startswith("NOT"):
        input = (input.replace("NOT ",""), "NOT", None)
    else:
        input = (input, "CONSTANT", None)

    return destination, input


def trace(wire, connections):
    left, op, right = connections[wire]
    try:
        left = int(left)
    except ValueError:
        left = trace(left, connections)
    if right is not None:
        try:
            right = int(right)
        except ValueError:
            right = trace(right, connections)
    if op == "CONSTANT":
        return left
    elif op == "NOT":
        val = 65535^left
        connections[wire] = (val, "CONSTANT", None)
        return val
    elif op == "AND":
        val = left & right
        connections[wire] = (val, "CONSTANT", None)
        return val
    elif op == "OR":
        val = left | right
        connections[wire] = (val, "CONSTANT", None)
        return val
    elif op == "LSHIFT":
        val = left << right
        connections[wire] = (val, "CONSTANT", None)
        return val
    elif op == "RSHIFT":
        val = left >> right
        connections[wire] = (val, "CONSTANT", None)
        return val
    else:
        print(f"ERROR: unknown command {op}, returning zero")
        return 0

def part1(lines):
    connections = parse(lines)
    signal = trace("a", connections)
    return signal


def part2(lines):
    return len(lines)


if __name__ == '__main__':
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
