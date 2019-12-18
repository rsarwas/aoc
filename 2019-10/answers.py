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
    dy = pt2[1] - pt1[1]
    if dx == 0 and dy == 0:
        return (0,0)
    if dx == 0:
        return (0,1) if dy > 0 else (0,-1)
    if dy == 0:
        return (1,0) if dx > 0 else (-1,0)
    gcd = math.gcd(dx,dy)
    return (dx//gcd, dy//gcd)

if __name__ == '__main__':
    astroids = get_astroids(sys.stdin.readlines())
    # count includes the astroid in question (i.e. I can see myself)
    # The problem examples/solution do not include this 
    astroid, count = get_most_visible(astroids) 
    print("Part 1: {0}".format(count-1))
