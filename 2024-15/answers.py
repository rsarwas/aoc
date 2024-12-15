"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

ROBOT = "@"
BOX = "O"
WALL = "#"
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"


def part1(lines):
    """Solve part 1 of the problem."""
    map, moves = parse(lines)
    for move in moves:
        map = update(map, move)
    total = 0
    _, boxes, _ = map
    for box in boxes:
        row, col = box
        total += 100 * row + col
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    map, moves = parse(lines)
    total = len(map)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    walls = set()
    boxes = set()
    robot = None
    moves = ""
    parse_first_part = True
    for row, line in enumerate(lines):
        line = line.strip()
        if line == "":
            parse_first_part = False
            continue
        if parse_first_part:
            for col, char in enumerate(line):
                if char == WALL:
                    walls.add((row, col))
                if char == ROBOT:
                    robot = (row, col)
                if char == BOX:
                    boxes.add((row, col))
        else:
            moves += line
    map = (walls, boxes, robot)
    return map, moves


def update(map, move):
    """update the map with the move"""
    walls, boxes, robot = map
    new_position = adjacent_location(robot, move)
    if new_position not in boxes and new_position not in walls:
        # space is free, move the robot
        robot = new_position
        return (walls, boxes, robot)
    if new_position in walls:
        # can't move into a wall, just sit at the current location
        return (walls, boxes, robot)
    # new_position is a box, try moving the boxes:
    if move_box(walls, boxes, new_position, move):
        # boxes were able to move, so move the robot
        robot = new_position
        return (walls, boxes, robot)
    # else, the box cannot move, os the robot cannot move
    return (walls, boxes, robot)


def move_box(walls, boxes, position, move):
    """There is a box at position. Try to move the box in the direction of move
    by updating boxes.
    It can move if the new position is empty
    it can not move if the new position is a wall
    if the new position is a box, call this function recursively
    if the box is moved out of the way, return True, otherwise return False"""
    new_position = adjacent_location(position, move)
    # print("try and move box from", position, "to", new_position)
    if new_position not in boxes and new_position not in walls:
        # space is free, move the box
        boxes.remove(position)
        boxes.add(new_position)
        return True
    if new_position in walls:
        # space is occupied, return without moving the box
        return False
    # else, there is a box at new_position, try and move it
    if move_box(walls, boxes, new_position, move):
        boxes.remove(position)
        boxes.add(new_position)
        return True
    return False


def adjacent_location(robot, move):
    """find the tile the robot would like to move to"""
    row, col = robot
    if move == UP:
        return row - 1, col
    if move == DOWN:
        return row + 1, col
    if move == RIGHT:
        return row, col + 1
    if move == LEFT:
        return row, col - 1
    return (row, col)


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
