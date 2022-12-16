# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
#
# part1 solution takes about 375 milliseconds. if we used a similar
# algorithm on each of the 4e6 rows to check, it would take about 
# 17 days to run - I need a faster solution.

def part1(lines):
    data = parse(lines)
    row = 2000000 # aka y value; test = 10; puzzle = 2000000
    result = no_beacon(data,row)
    return result


def part2(lines):
    data = parse(lines)
    # extents = (0, 0, 20, 20)
    extents = (0, 0, 1, 4000000)
    bx, by = missing_beacon(data, extents)
    result = bx * 4000000 + by
    return result


def parse(lines):
    data = []
    for line in lines:
        line = line.strip().replace("Sensor at x=","").replace(" y=","")
        line = line.replace(" closest beacon is at x=","")
        sensor,beacon = line.split(":")
        sx,sy = sensor.split(",")
        sx,sy = int(sx),int(sy)
        bx,by = beacon.split(",")
        bx,by = int(bx),int(by)
        reach = abs(sx-bx) + abs(sy-by)
        data.append((sx,sy,bx,by,reach))
    return data


def no_beacon(data, row):
    # find all the x coordinates along row that are reachable by each sensor
    reachable = set() # use a set so we do not count duplicates
    for item in data:
        sx, sy, reach = item[0], item[1], item[4]
        dist_to_row = abs(sy - row)
        if dist_to_row <= reach:
            span = reach - dist_to_row
            start, end = sx - span, sx + span
            for r in range(start, end+1):
                reachable.add(r)
    # find all the beacons on this row (we need to remove them from the count)
    for item in data:
        bx, by = item[2], item[3]
        if by == row:
            if bx in reachable:
                reachable.remove(bx)
    return len(reachable)


def missing_beacon(data, extents):
    # create a set of rows*col items, and remove
    # the ones that can be found, the one remaining
    # item in the set is the solution
    # this is very slow, and takes a lot of space. 4e12 (x,y) tuples in the set
    # takes over 3 minutes to check 1 row, so it is not a viable candidate
    min_x, min_y, max_x, max_y = extents
    potential = set()
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            potential.add((x,y))
    for item in data:
        sx, sy, bx, by, reach = item
        potential.discard((bx,by))
        y1 = min(min_y, sx - reach)
        y2 = max(max_y, sx + reach)
        for row in range(y1, y2+1):
            dist_to_row = abs(sy - row)
            span = reach - dist_to_row
            start, end = sx - span, sx + span
            for r in range(start, end+1):
                potential.discard((r,row))
    print(potential)
    if len(potential) > 1:
        print("PANIC: more than one beacon")
    return potential.pop()


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    # print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
