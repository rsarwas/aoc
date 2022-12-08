# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    map = parse(lines)
    trees = visible(map)
    # display(trees,len(map))
    return len(trees)


def part2(lines):
    return -1


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
