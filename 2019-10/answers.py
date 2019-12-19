import math
import sys

def get_astroids(lines):
    data = []
    for row,line in enumerate(lines):
        for col,char in enumerate(line):
            if char == '#':
                data.append((col,row))
    return data

def get_most_visible(astroids):
    winner = (None,0)
    for astroid in astroids:
        slopes = {}
        for other in astroids:
            slope = simple_slope(astroid,other)
            if slope not in slopes:
                slopes[slope] = 0
            slopes[slope] += 1
        if len(slopes) > winner[1]:
            winner = (astroid, len(slopes))
    return winner

def simple_slope(pt1, pt2):
    dx = pt2[0] - pt1[0]
    dy = -(pt2[1] - pt1[1]) # y axis is inverted
    if dx == 0 and dy == 0:
        return (0,0)
    if dx == 0:
        return (0,1) if dy > 0 else (0,-1)
    if dy == 0:
        return (1,0) if dx > 0 else (-1,0)
    gcd = math.gcd(dx,dy)
    return (dx//gcd, dy//gcd)

def get_nth_vaporized(astroid, n, astroids):
    slopes = {}
    for other in astroids:
        if astroid == other:
            continue
        slope = simple_slope(astroid,other)
        if slope not in slopes:
            slopes[slope] = 0
        slopes[slope] += 1

    """
    # used to verify that I will find the nth astroid in the first revolution.
    counts = {}
    for slope in slopes:
        count = slopes[slope]
        if count not in counts:
            counts[count] = 0
        counts[count] += 1
    print(counts)
    """

    slope = sort_slopes([s for s in slopes])[n-1]
    location = astroid
    found = False
    while not found :
        # Note: Y axis is inverted
        location = (location[0] + slope[0], location[1] - slope[1])
        if location in astroids:
            print(location)
            found = True
    return location


def sort_slopes(slope_list):
    # order the astroids on thier slope (starting with 0,1 and rotating clockwise)
    def value(slope):
        # returns a number from 0 to 2pi with 0 = north, and increasing clockwise
        # atan2(x,y) => 0..pi for angle = (0,1)..(1,1)..(1,0)..(1,-1)..(0,-1)
        # atan2(x,y) => -pi..0 for slope = (0,-1)..(-1,-1)..(-1,0)..(-1,1)..(0,1)
        step1 = math.atan2(slope[0], slope[1])
        step2 = step1 if step1 >= 0 else step1 + (2*math.pi)
        return step2
    
    work = [(value(s), s) for s in slope_list]
    work.sort()
    return [s[1] for s in work]

if __name__ == '__main__':
    astroids = get_astroids(sys.stdin.readlines())
    # count includes the astroid in question (i.e. I can see myself)
    # The problem examples/solution do not include this 
    astroid, count = get_most_visible(astroids) 
    print("Part 1: {0}".format(count-1))
    astroid200 = get_nth_vaporized(astroid, 200, astroids)
    part2 = astroid200[0]*100 + astroid200[1]
    print("Part 2: {0}".format(part2))
