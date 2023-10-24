# Data Model:
# ===========

def parse(lines):
    instructions = []
    for line in lines:
        if line.startswith("turn on "):
            command = "on"
            line = line.replace("turn on ","")
        elif line.startswith("turn off "):
            command = "off"
            line = line.replace("turn off ","")
        elif line.startswith("toggle "):
            command = "toggle"
            line = line.replace("toggle ","")
        else:
            print(f"Input Error unexpected command: {line}")
        start, end = line.split(" through ")
        start = [int(num) for num in start.split(",")]
        end = [int(num) for num in end.split(",")]
        instructions.append((command, start, end))
    return instructions


def initialize(rows, cols):
    grid = []
    for r in range(rows):
        row = [0] * cols
        grid.append(row)
    return grid


def update(grid, instruction):
    command, corner1, corner2 = instruction
    left = min(corner1[0], corner2[0])
    right = max(corner1[0], corner2[0])
    top = min(corner1[1], corner2[1])
    bottom = max(corner1[1], corner2[1])
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            if command == "on":
                grid[row][col] = 1
            if command == "off":
                grid[row][col] = 0
            if command == "toggle":
                grid[row][col] = (grid[row][col] + 1) % 2
    

def lights_on(grid):
    total = 0
    for row in grid:
        for light in row:
            if light == 1:
                total += 1
    return total


def part1(lines):
    instructions = parse(lines)
    grid = initialize(1000,1000)
    for instruction in instructions:
        update(grid, instruction)
    count = lights_on(grid)
    return count


def part2(lines):
    return len(lines)


if __name__ == '__main__':
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
