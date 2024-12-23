"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    codes = parse(lines)
    total = 0
    for code in codes:
        buttons = find_buttons(code, 2)
        value = code_value(code)
        # print(value, "*", len(buttons))
        total += value * len(buttons)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    # This solution is too slow
    codes = parse(lines)
    total = 0
    for code in codes:
        buttons = find_buttons(code, 25)
        value = code_value(code)
        print(value, "*", len(buttons))
        total += value * len(buttons)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        data.append(line)
    return data


def code_value(code):
    """Return the numerical part of the code as an integer"""
    return int(code[:3])


def find_buttons(code, n):
    """Return the shortest path of robot commands to enter the code.
    * One directional keypad that you are using.
    * Two directional keypads that robots are using.
    * One numeric keypad (on a door) that a robot is using."""
    # print(code)
    # moves = numeric_robot(code)
    # print("original numeric moves", "".join(moves), len(moves))
    # from experimenting with the variable parts, these are the optimal choices
    best_moves = {
        "839A": "<^^^Avv>A^^AvvvA",
        "169A": "^<<A>>^A^AvvvA",
        "579A": "<^^A<^A>>AvvvA",
        "670A": "^^A<<^A>vvvA>A",
        "638A": "^^AvA<^^Avvv>A",
    }
    moves = best_moves[code]
    # print("modified numeric Moves", moves, len(moves))
    for i in range(n):
        moves = directional_robot(moves)
        # print("Directional Moves {i+1}", "".join(moves), len(moves))
    return moves


def numeric_robot(code):
    """Return the shortest sequence of moves, "<>^vA" to enter the code
    on the numeric keypad (starting at A)
    7 8 9
    4 5 6
    1 2 3
    _ 0 A
    Note that all direct paths are equal length. Horizontal then vertical is the same
    as vertical then horizontal is the same as alternating (stair-stepping). There is
    no trick to finding the shortest path. Just make sure to avoid the blank button
    in the lower left. So if you are at 1, 4 or 7 and going to 0 or A be sure to go
    right then down. If you are going the other way go up then left."""
    keys = {
        # button: (row, col)
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        # " ": (3, 0),
        "0": (3, 1),
        "A": (3, 2),
    }
    start = (3, 2)  # button A
    blank = (3, 0)
    loc2 = None
    moves = []
    for char in code:
        if loc2 is None:
            loc2 = start
        loc1 = loc2
        loc2 = keys[char]
        moves += min_moves3(loc1, loc2, blank)
        moves.append("A")
    return moves


def directional_robot(buttons):
    """Return the shortest sequence of moves, "<>^vA" to press the buttons
    on the directional keypad (starting at A)
       ^  A
    <  v  >

    if we start at A and end at A which is better?
    down then left (6) vs left then down (6)
    down then right (4) vs right then down (4)
    up then left (6) vs left then up (6)
    up then right (4) vs right then up (4)
    Turns out all options are all the same for the first directional robot.

    What about the second?
    which is better <A^A (8) or ^A<A (8)
    """
    keys = {
        # button: (row, col)
        # " ": (0, 0),
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }
    start = (0, 2)  # button A
    blank = (0, 0)
    loc2 = None
    moves = []
    for char in buttons:
        if loc2 is None:
            loc2 = start
        loc1 = loc2
        loc2 = keys[char]
        moves += min_moves3(loc1, loc2, blank)
        moves.append("A")
    return moves


def min_moves(loc1, loc2, blank):
    """Return a minimum list of moves to get from loc1 to loc2
    We must avoid going over the blank spot in the lower left"""
    row1, col1 = loc1
    row2, col2 = loc2
    moves = []
    if blank == (0, 0):  # upper left
        if col1 == 0 and col2 > 0 and row1 > 0 and row2 == 0:
            moves += move_horizontal(col1, col2)
            moves += move_vertical(row1, row2)
        else:
            moves += move_vertical(row1, row2)
            moves += move_horizontal(col1, col2)
    else:  # blank at lower left
        if col1 == 0 and row2 == blank[0] and row1 < row2 and col2 > col1:
            moves += move_horizontal(col1, col2)
            moves += move_vertical(row1, row2)
        else:
            moves += move_vertical(row1, row2)
            moves += move_horizontal(col1, col2)
    return moves


def min_moves2(loc1, loc2, blank):
    """Return a minimum list of moves to get from loc1 to loc2
    We must avoid going over the blank spot in the lower left"""
    row1, col1 = loc1
    row2, col2 = loc2
    moves = []
    if row2 == blank[0] and col1 == blank[1]:
        moves += move_horizontal(col1, col2)
        moves += move_vertical(row1, row2)
    else:
        moves += move_vertical(row1, row2)
        moves += move_horizontal(col1, col2)
    return moves


def min_moves3(loc1, loc2, blank):
    """Return a minimum list of moves to get from loc1 to loc2
    We must avoid going over the blank spot in the lower left"""
    row1, col1 = loc1
    row2, col2 = loc2
    moves = []
    if row1 == blank[0] and col2 == blank[1]:
        moves += move_vertical(row1, row2)
        moves += move_horizontal(col1, col2)
    else:
        moves += move_horizontal(col1, col2)
        moves += move_vertical(row1, row2)
    return moves


def move_horizontal(col1, col2):
    if col1 < col2:
        return [">"] * (col2 - col1)
    elif col1 > col2:
        return ["<"] * (col1 - col2)
    else:
        # col1 == col2 do nothing
        return []


def move_vertical(row1, row2):
    if row1 < row2:
        return ["v"] * (row2 - row1)
    elif row1 > row2:
        return ["^"] * (row1 - row2)
    else:
        # row1 == row2 do nothing
        return []


def test():
    """Test various permutations.
    All horizontal then all vertical or visa versa is always better than
    a stair step approach. Often it is a tie, between the two options,
    but not always.  sometimes it is best for horizontal first, but not always.
    Since each sequence ends in an A, the sequences between 'A's are independent"""
    # 389A -> <^^^Avv>A^^AvvvA
    # moves = [
    #     "<^^^Avv>A^^AvvvA",
    #     "^<^^Avv>A^^AvvvA",
    #     "^^<^Avv>A^^AvvvA",
    #     "^^^<Avv>A^^AvvvA",
    #     "<^^^Av>vA^^AvvvA",
    #     "^<^^Av>vA^^AvvvA",
    #     "^^<^Av>vA^^AvvvA",
    #     "^^^<Av>vA^^AvvvA",
    #     "<^^^A>vvA^^AvvvA", # Winner
    #     "^<^^A>vvA^^AvvvA",
    #     "^^<^A>vvA^^AvvvA",
    #     "^^^<A>vvA^^AvvvA",
    # ]
    # moves = ["<^^^A", "^<^^A", "^^<^A", "^^^<A", "vv>A", "v>vA", ">vvA"]
    # winner: <^^^A and  vv>A
    # moves = ["^<<A", "<^<A", "^>>A", ">^>A", ">>^A"]
    # winners ^<<A and tie "^>>A" or ">>^A"
    # moves = ["^^<", "^<^", "<^^", "<^", "^<"] # tie except ^<^ is loser
    # moves = ["^<<", "<^<", "<<^", ">vvv", "v>vv", "vv>v"]  # tie and >vvv
    moves = ["^^<", "^<^", "<^^", ">vvv", "v>vv", "vv>v", "vvv>"]  # tie and vvv>
    moves1 = [
        "<^^^Avv>A^^AvvvA",
        "^<<A>>^A^AvvvA",
        "<^^A<^A>>AvvvA",
        "^^A<<^A>vvvA>A",
        "^^AvA<^^Avvv>A",
    ]
    for moves_1 in moves:
        print(moves_1, len(moves_1))
        moves_2 = directional_robot(moves_1)
        print("".join(moves_2), len(moves_2))
        moves_3 = directional_robot(moves_2)
        print("".join(moves_3), len(moves_3))


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
    # test()
