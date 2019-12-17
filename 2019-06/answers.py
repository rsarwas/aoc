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

def get_transfers(here, there, end, centers):
    here_list = orbits_for(here, end, centers)
    #print("here", here_list)
    there_list = orbits_for(there, end, centers)
    #print("there",there_list)
    for index, body in enumerate(here_list):
        if body in there_list:
            return index + there_list.index(body)

def orbits_for(start, end, centers):
    bodies = []
    center = centers[start]
    while center != end:
        bodies.append(center)
        center = centers[center]
    return bodies

if __name__ == '__main__':
    input = sys.stdin.readlines()
    centers = build_graph(input)
    total = total_orbits(centers)
    print("Part 1: {0}".format(total))
    number_orbital_transfers = get_transfers('YOU','SAN','COM',centers)
    print("Part 2: {0}".format(number_orbital_transfers))

