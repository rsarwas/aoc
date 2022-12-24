# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

WALL = "#"
OPEN = "."
UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"

def part1(lines):
    blizzards, start, finish, walls = parse(lines)
    print (blizzards, start, finish, walls)
    blizzards = update(blizzards, walls)
    print (blizzards)
    result = solve(blizzards)
    return result


def part2(lines):
    return -1


def parse(lines):
    data = []
    left_wall, top_wall, right_wall, bottom_wall = 1e10, 1e10, 0, 0
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == WALL:
                if row < top_wall: top_wall = row
                if row > bottom_wall: bottom_wall = row
                if col < left_wall: left_wall = col
                if col > right_wall: right_wall = col
            elif char == OPEN:
                if row == top_wall: start = (row, col)
                if row == bottom_wall: finish = (row, col)
            else:
                blizzard = (row, col, char)
                data.append(blizzard)
    return data, start, finish, (left_wall, top_wall, right_wall, bottom_wall)


def solve(data):
    result = 0
    for item in data:
        result += len(item)
    return result


def update(blizzards, walls):
    left, top, right, bottom = walls
    for i, blizzard in enumerate(blizzards):
        row, col, dir = blizzard
        if dir == UP:
            row -= 1
            if row == top: row = bottom - 1
        if dir == DOWN:
            row += 1
            if row == bottom: row = top + 1
        if dir == RIGHT:
            col += 1
            if col == right: col = left + 1
        if dir == LEFT:
            col -= 1
            if col == left: col = right - 1
        blizzards[i] = (row, col, dir)
    return blizzards


if __name__ == '__main__':
    lines = open("test.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
