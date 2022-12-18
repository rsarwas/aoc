# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    # data = [(1,1,1), (2,1,1)] # testg data; result should be 10
    result = solve(data)
    return result


def part2(lines):
    data = parse(lines)
    result = solve(data)
    # find all the single cell voids (solves the test case)
    voids = find_holes(data)
    # find all the multi cell voids
    # ???
    # lets check to see what this thing looks like
    display(data)
    # ack, it has a huge void in the center, with isolated blobs within the void
    # I'll need a whole new strategy
    interior_area = solve(voids)
    result -= interior_area
    return result


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        items = line.split(",")
        x,y,z = int(items[0]), int(items[1]), int(items[2])
        data.append((x,y,z))
    return data


def solve(data):
    result = 0
    for drop in data:
        result += exposed(drop, data)
    return result


def exposed(drop, drops):
    x,y,z = drop
    exposed = 6
    for other in drops:
        x1,y1,z1 = other
        if y1 == y and z1 == z and (x1 == x+1 or x1 == x-1):
            exposed -= 1
        elif x1 == x and z1 == z and (y1 == y+1 or y1 == y-1):
            exposed -= 1
        elif x1 == x and y1 == y and (z1 == z+1 or z1 == z-1):
            exposed -= 1
    return exposed


def find_holes(drops):
    x_min, y_min, z_min, x_max, y_max, z_max = extents(drops)
    drop_set = set(drops)
    voids = []
    for x in range(x_min+1, x_max):
        for y in range(y_min+1, y_max):
                for z in range(z_min+1, z_max):
                    if (x,y,z) in drop_set:
                        continue
                    if neighbors((x,y,z), drops) == 6:
                        voids.append((x,y,z))
    return voids


def extents(drops):
    x_max, y_max, z_max = (-1E6, -1E6, -1E6)
    x_min, y_min, z_min = (1E6, 1E6, 1E6)
    for drop in drops:
        x,y,z = drop
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
        if z < z_min:
            z_min = z
        if z > z_max:
            z_max = z
    return x_min, y_min, z_min, x_max, y_max, z_max


def neighbors(void, drops):
    x,y,z = void
    neighbors = 0
    for drop in drops:
        x1,y1,z1 = drop
        if y1 == y and z1 == z and (x1 == x+1 or x1 == x-1):
            neighbors += 1
        elif x1 == x and z1 == z and (y1 == y+1 or y1 == y-1):
            neighbors += 1
        elif x1 == x and y1 == y and (z1 == z+1 or z1 == z-1):
            neighbors += 1
    return neighbors


def display(drops):
    x_min, y_min, z_min, x_max, y_max, z_max = extents(drops)
    print(x_min, y_min, z_min, x_max, y_max, z_max)
    cube = []
    for z in range(z_max-z_min+1):
        level = []
        for y in range(y_max-y_min+1):
            row = ['.']*(x_max-x_min+1)
            level.append(row)
        cube.append(level)
    for drop in drops:
        x,y,z = drop
        cube[z-z_min][y-y_min][x-x_min] = '#'
    level_n = z_min
    for level in cube:
        print("z = ", level_n)
        for i,row in enumerate(level):
            print((i+y_min)%10, "".join(row))
        level_n += 1


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
