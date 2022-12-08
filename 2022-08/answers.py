# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    map = parse(lines)
    trees = visible(map)
    # display(trees,len(map))
    return len(trees)


def part2(lines):
    data = parse(lines)
    # print(scenic_score(1,2,data))
    # print(scenic_score(3,2,data))
    best = 0
    for r in range(len(data)):
        for c in range(len(data[r])):
            score = scenic_score(r,c,data)
            if score > best:
                best = score
    return best


def parse(lines):
    map = []
    for line in lines:
        line = line.strip()
        row = [int(char) for char in line]
        map.append(row) 
    return map


def visible(data):
    result = set() # unique (r,c) tuples
    # check rows
    for r in range(len(data)):
        # looking left to right
        tallest = -1
        for c in range(len(data[r])):
            height = data[r][c]
            if height > tallest:
                result.add((r,c))
                tallest = height
                if height == 9:
                    break
        # looking right to left
        tallest = -1
        for c in range(len(data[r])-1,-1, -1):
            height = data[r][c]
            if height > tallest:
                result.add((r,c))
                tallest = height
                if height == 9:
                    break
    # check columns
    # looking top to bottom
    tallest = [-1] * len(data[0])
    for r in range(len(data)):
        for c in range(len(data[r])):
            height = data[r][c]
            if height > tallest[c]:
                result.add((r,c))
                tallest[c] = height
    # looking bottom to top
    tallest = [-1] * len(data[0])
    for r in range(len(data)-1,-1,-1):
        for c in range(len(data[r])):
            height = data[r][c]
            if height > tallest[c]:
                result.add((r,c))
                tallest[c] = height
    return result

def scenic_score(r,c,data):
    r_count = len(data)
    c_count = len(data[0])
    if r == 0 or c == 0 or c ==  c_count-1 or r == r_count-1:
        # on an edge so one of the distance will be zero, so score is zero
        return 0
    height = data[r][c]
    # look down; increase r to edge or tree of equal or greater height
    down = 0
    ri = r+1
    while ri < r_count:
        down += 1
        if data[ri][c] >= height:
            break
        ri += 1
    if down == 0:
        return 0
    # look down; decrease r to edge or tree of equal or greater height
    up = 0
    ri = r-1
    while ri >= 0:
        up += 1
        if data[ri][c] >= height:
            break
        ri -= 1
    if up == 0:
        return 0
    # look right; increase c to edge or tree of equal or greater height
    right = 0
    ci = c+1
    while ci < c_count:
        right += 1
        if data[r][ci] >= height:
            break
        ci += 1
    if right == 0:
        return 0
    # look left; decrease c to edge or tree of equal or greater height
    left = 0
    ci = c-1
    while ci >= 0:
        left += 1
        if data[r][ci] >= height:
            break
        ci -= 1
    if left == 0:
        return 0    
    # print(r, c, up, left, right, down)
    return up*down*left*right

def display(trees, size):
    grid = []
    for i in range(size):
        row = ['.']*size
        grid.append(row)
    for r,c in trees:
        grid[r][c] = '#'
    for row in grid:
        print("".join(row))


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
