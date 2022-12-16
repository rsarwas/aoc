# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
#
# part1 solution takes about 375 milliseconds. if we used a similar
# algorithm on each of the 4e6 rows to check, it would take about 
# 17 days to run - I need a faster solution.
# part2 option 1 - 17 days
#   using modified part1 algorithm
# part 2 option 2 - infinite amount of time; exceed available memory 
#   create set of all potential location. for each sensor remove all reachable
#   answer is the remaining locations
# part 2 option 3 - 1 year
#   for each (x,y) location, check each sensor, stop sensor check if reachable
#   done if the location is not reachable by any sensor.


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
    # Check each location: O(n*m*sensors) 4e6,4e6,30
    #  takes about 8 seconds for each row, estimated time about 1 year
    min_x, min_y, max_x, max_y = extents
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if status_unknown(x, y, data):
                return (x,y)
    return None


def status_unknown(x, y, data):
    for item in data:
        sx, sy, bx, by, reach = item
        if x == bx and y == by:
            return False
        if abs(sx - x) + abs(sy - y) <= reach:
            return False
    return True


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    # print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
