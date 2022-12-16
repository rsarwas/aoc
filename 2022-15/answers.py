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
# part 2 option 4 - 139 days
#   same as option 3, but sort sensors with the largest reach first
#   improves to about 3 seconds per row (from 8 seconds)
# part2 option 5 - 13 seconds
#  variant on part1, for each row, get the start/stop x-coordinate for the coverage of
#  each sensor (if there is any) and look for a gap in thhe start/stop pairs

def part1(lines):
    data = parse(lines)
    row = 2000000 # aka y value; test = 10; puzzle = 2000000
    result = no_beacon(data,row)
    return result


def part2(lines):
    data = parse(lines)
    size = 4_000_000
    row = 0
    while row < size + 1:
        x = beacon(data, row, 0, size)
        if x != None:
            break
        row += 1
    result = x * 4000000 + row
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


def beacon(data, row, x_min, x_max):
    # returns the x location (within bounds) of a possible beacon in row, or None
    # consider the start and stop location that each sensor covers on the given row
    # look for a gap in the range [x_min,x_max]
    # takes less than a millisecond per row
    covers = []
    for item in data:
        sx, sy, bx, by, reach = item
        dist_to_row = abs(sy - row)
        if dist_to_row <= reach:
            span = reach - dist_to_row
            start, end = sx - span, sx + span
            covers.append((start,end))
        if by == row:
            covers.append((bx,bx))
    covers.sort()
    # print(covers)
    if covers[0][0] > x_min:
        return x_min
    end = covers[0][1]
    i = 1
    while end < x_max and i < len(covers):
        if covers[i][0] > end+1:
            return end+1
        if covers[i][1] > end:
            end = covers[i][1]
        i += 1
    if end < x_max:
        return end+1
    return None        


def missing_beacon(data, extents):
    # Check each location: O(n*m*sensors) 4e6,4e6,30
    #  takes about 8 seconds for each row, estimated time about 1 year
    # solves the problem (4e6 rows) in about 14 seconds
    data1 = [(e,a,b,c,d) for (a,b,c,d,e) in data]
    data1.sort()
    data1.reverse()
    min_x, min_y, max_x, max_y = extents
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if status_unknown(x, y, data1):
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
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
