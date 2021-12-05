# Data Model
# vents is list of pairs of (x,y) tuples [((x1,y1),(x2,y2)), ...] 
# map is a dict { (x,y): count} which has the number of vents over x,y
def part1(lines):
    vents = parse(lines)
    return solve(vents)

def part2(lines):
    vents = parse(lines)
    return solve(vents, diag=True)

def solve(vents, diag=False):
    map = {}
    for vent in vents:
        x1, y1 = vent[0]
        x2, y2 = vent[1]
        # print(x1,y1,x2,y2)
        # vertical lines
        if x1 == x2:
            x = x1
            dy = 1 if y2 > y1 else -1
            for y in range(y1, y2+dy, dy):
                # print("  v", x,y)
                if (x,y) in map:
                    map[(x,y)] += 1
                else:
                    map[(x,y)] = 1
        # horizontal lines
        elif y1 == y2:
            y = y1
            dx = 1 if x2 > x1 else -1
            for x in range(x1, x2+dx, dx):
                # print("  h", x,y)
                if (x,y) in map:
                    map[(x,y)] += 1
                else:
                    map[(x,y)] = 1
        else:
        # diagonal lines
            if diag:
                dx = 1 if x2 > x1 else -1
                dy = 1 if y2 > y1 else -1
                n = abs(x2-x1)
                # Set (x,y) before the start so they are correctly incremented in the first loop
                x = x1 - dx
                y = y1 - dy
                # just one loop!  do not loop over both x and y!!
                for _ in range(0,n+1):
                    x += dx
                    y += dy
                    # print("  d", x, y)
                    if (x,y) in map:
                        map[(x,y)] += 1
                    else:
                        map[(x,y)] = 1

    overlaps = 0
    for key,value in map.items():
        if value > 1:
            overlaps += 1
    return overlaps

def parse(lines):
    vents = []
    for line in lines:
        start, end = line.strip().split(" -> ")
        x1,y1 = start.split(",")
        x2,y2 = end.split(",")
        vents.append( ((int(x1), int(y1)), (int(x2), int(y2))) )
    return vents

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    lines = open("input.txt").readlines() # as a list of line strings
    # lines = open("test.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
