# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    # print(data)
    x = 1
    cycles = [20, 60, 100, 140, 180, 220]
    xs = solve(data, x)
    signals = [cycle * xs[cycle - 1] for cycle in cycles]
    return sum(signals)


def part2(lines):
    data = parse(lines)
    xs = solve(data, 1)
    crt = ["."]*240
    for i,x in enumerate(xs):
        if i%40 >= x-1 and i%40 <= x+1:
            crt[i%240] = "#"
    for row in range(6):
        start = row*40
        print("".join(crt[start:start+40]))
    return "ZKGRKGRK"

def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        if line == "noop":
            data.append(None)
        else:
            _, val = line.split()
            data.append(int(val))
    return data


def solve(data, x):
    xs = [x]
    for item in data:
        if item:
            xs.append(x)
            x += item
            xs.append(x)
        else:
            xs.append(x) 
    return xs 


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
