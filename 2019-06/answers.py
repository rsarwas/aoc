import sys

def build_graph(lines):
    centers = {}
    for line in lines:
        center, body = line.strip().split(')')
        centers[body] = center
    return centers

def total_orbits(centers):
    total = 0
    for body in centers:
        total += orbits(body, centers)
    return total

def orbits(body, centers):
    center = centers[body]
    if center == 'COM':
        return 1
    else:
        return 1 + orbits(center, centers)

if __name__ == '__main__':
    input = sys.stdin.readlines()
    centers = build_graph(input)
    total = total_orbits(centers)
    print("Part 1: {0}".format(total))
