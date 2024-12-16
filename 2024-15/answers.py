"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test3.txt"

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
    map = expand(map)
    # display(map, (10, 20))
    display(map, (7, 14))
    for move in moves:
        print("move", move)
        map = update_wide(map, move)
        display(map, (7, 14))
        # display(map, (10, 20))
    total = 0
    _, boxes, _ = map
    # display(map, (7, 14))
    for box in boxes:
        row, col = box
        total += 100 * row + col
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


def display(map, size):
    """A display of the map (for debugging part 2)"""
    rows, cols = size
    walls, boxes, robot = map
    grid = []
    for _ in range(rows):
        line = ["."] * cols
        grid.append(line)
    for row, col in walls:
        grid[row][col] = "#"
        grid[row][col + 1] = "#"
    for row, col in boxes:
        grid[row][col] = "["
        grid[row][col + 1] = "]"
    row, col = robot
    grid[row][col] = "@"
    for line in grid:
        print("".join(line))


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


def expand(map):
    """Make the map twice as wide.
    I adjust all the coordinates, but I do not adust the
    number of tiles in boxes and walls. Each box and wall tile
    explicitly includes (row, col) and implicitly includes (row, col + 1)"""
    walls, boxes, robot = map
    walls = set([(row, 2 * col) for row, col in walls])
    boxes = set([(row, 2 * col) for row, col in boxes])
    row, col = robot
    robot = (row, 2 * col)
    return (walls, boxes, robot)


def update_wide(map, move):
    """update the map with the robot move"""
    walls, boxes, robot = map
    new_position = adjacent_location(robot, move)
    wall_position = is_wide_hit(robot, move, walls)
    box_position = is_wide_hit(robot, move, boxes)
    if not wall_position and not box_position:
        # space is free, move the robot
        robot = new_position
        return (walls, boxes, robot)
    if wall_position:
        # can't move into a wall, just sit at the current location
        return (walls, boxes, robot)
    # new_position conflicts with a box, try moving the box:
    # print("before move wide_box, boxes = ", boxes)
    if move_widebox(box_position, move, walls, boxes):
        # boxes were moved, so move the robot
        # print("after wide_box MOVED, boxes = ", boxes)
        robot = new_position
        return (walls, boxes, robot)
    # else, the box cannot move, so the robot cannot move
    # print("after NO wide_box move, boxes = ", boxes)
    return (walls, boxes, robot)


def move_widebox(position, move, walls, boxes):
    """There is a wide box at position. If we can make the move, update the map, and
    return True, otherwise return False.
    In order to move the box, we may need to move other wideboxes, so this is called
    recursively.
    It can move if the new position is empty
    it can not move if the new position is a wall
    if the new position is a box, call this function recursively
    if the box is moved out of the way, return True, otherwise return False
    * if we are moving up or down, we may need to move two boxes,
    IF we need to move two boxes, only return true if we CAN move both boxes"""
    new_position = adjacent_location(position, move)
    wall_positions = is_widebox_hit(position, move, walls)
    box_positions = is_widebox_hit(position, move, boxes)
    # print("try and move box from", position, "to", new_position)
    if not wall_positions and not box_positions:
        # space is free, move the box
        # print("no obstructions, move", position)
        boxes.remove(position)
        boxes.add(new_position)
        # print("return true with boxes = ", boxes)
        return True
    if wall_positions:
        # space is occupied, return without moving the box
        return False
    # else, there is one or more boxes in the way: can I move them
    if len(box_positions) == 1:
        if move_widebox(box_positions[0], move, walls, boxes):
            # print("only one box and it move")
            boxes.remove(position)
            boxes.add(new_position)
            # print("move ", position)
            # print("return true with boxes = ", boxes)
            return True
    # There are two boxes, try to move them both.
    # save a copy of boxes, it needs to be restored if the first box moves, but
    # the second box cannot move
    print("trying to move two boxes")
    # print(boxes)
    saved_boxes = list(boxes)
    if not move_widebox(box_positions[0], move, walls, boxes):
        # print("first box did not move. done.")
        # print(boxes)
        return False
    print("first box moved")
    # print(boxes)
    # box1 moved, try moving box 2
    if move_widebox(box_positions[1], move, walls, boxes):
        # print("second boxes moved")
        # print(boxes)
        boxes.remove(position)
        boxes.add(new_position)
        # print("move me and return")
        # print(boxes)
        return True
    else:
        print("second box did not move.")
        print(boxes)
        # box 1 moved, but box2 did not, undo the box 1 move
        boxes.clear
        boxes.update(saved_boxes)
        # Unfortunately this creates a new local variable that does not change
        # the reference in the outer scope
        # boxes = set(saved_boxes)
        print("Undo first move")
        print(boxes)
    # print("returning with False, boxes = ", boxes)
    return False


def is_wide_hit(location, move, items):
    """Used to test if a robot at location (single tile) can make the move.
    It can make the move if there is no item in the new position.
    items is either a set of wall or box locations, we do not know which the caller is providing.
    An item occupies it's (row,col) as well (row, col + 1), so if we are moving up or down, we
    will need to check two locations.  For examples

      # = item, * = item's right side, . = opentile, T/F = robot location that returns True or False
      move ^  ...#*...   move v  FFFTTFFF   move >  T#*; move <:  #*T all others are false
              FFFTTFFF           ...#*...

    Nominally, the answer would be true or false, but if item is a box, the caller need to know the
    actual location of the box, so that they can try moving it out of the way.
    Return None if there is nothing in the way, return the item location if there is a hit
    """
    row, col = location
    if move == RIGHT:
        if (row, col + 1) in items:
            return (row, col + 1)
    if move == LEFT:
        if (row, col - 2) in items:
            return (row, col - 2)
    if move == UP:
        if (row - 1, col) in items:
            return (row - 1, col)
        if (row - 1, col - 1) in items:
            return (row - 1, col - 1)
    if move == DOWN:
        if (row + 1, col) in items:
            return (row + 1, col)
        if (row + 1, col - 1) in items:
            return (row + 1, col - 1)
    return None


def is_widebox_hit(location, move, items):
    """Used to test if a widebox at location (row,col) + (row,col+1) can make the move.
    It can make the move if there is no item in the new position.
    items is either a set of wall or box locations, we do not know which the caller is providing.
    An item occupies it's (row,col) as well (row, col + 1), so if we are moving up or down, we
    will need to check multiple locations, and we may conflict with 0, 1 or 2 items.  For example:

      # = item, * = item's right side, . = opentile, [] = box location
      move ^, the following have 0, 1 or 2 hits, similar for down
       0: ..  1: .#*   #*   #*.  2: #*#*
          []     []    []    []      []
      moving left or right is nearly the same as moving a robot in is_wide_hit

    Nominally, the answer would be true or false, or the number of hits, but if item is a box,
    the caller need to know the actual location of the box(es), so that they can try moving them
    out of the way.
    Return an empty list is nothing in the way, return the item location(s) if there is a hit
    """
    row, col = location
    if move == RIGHT:
        if (row, col + 2) in items:
            return [(row, col + 2)]
        return []
    if move == LEFT:
        if (row, col - 2) in items:
            return [(row, col - 2)]
        return []
    if move == UP:
        r = row - 1
    else:  # move == DOWN
        r = row + 1
    # less code, but harder to reason about
    # hits = []
    # for delta in [-1,0,1]:
    #     if (r,col+delta) in items:
    #         hits.append((r, col + delta))
    if (r, col - 1) in items and (r, col + 1) in items:
        print("move two boxes in  row", r)
        return [(r, col - 1), (r, col + 1)]
    if (r, col) not in items and (r, col + 1) in items:
        return [(r, col + 1)]
    if (r, col) in items:
        return [(r, col)]
    if (r, col) not in items and (r, col - 1) in items:
        return [(r, col - 1)]

    return []


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
