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
        count = count_buttons(code, 2)
        value = code_value(code)
        # print(value, "*", count)
        total += value * count
    return total


def part2(lines):
    """Solve part 2 of the problem.

    The brute force approach in part 1 proved WAY to slow.
    so a caching recursive solution was developed for the
    directional keys. This failed to deliver the correct answer"""
    codes = parse(lines)
    total = 0
    for code in codes:
        count = count_buttons(code, 25)
        value = code_value(code)
        # print(value, "*", count)
        total += value * count
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


def count_buttons(code, n):
    """Returns the minimum number of directional buttons, I must
    push to get a robot to enter the door code given.  There are
    n levels of robots in the middle pushing directional buttons
    for the next robot down the line.  the last robot pushes the
    door codes."""
    start = "A"
    count = 0
    for char in code:
        min_count = 1e15
        for move in number_keys[(start, char)]:
            c = count_moves(move, n)
            if c < min_count:
                min_count = c
        count += min_count
        start = char
    return count


"""
cache is used to store values in the recursive search.
It makes the recursion possible in limited time."""
cache = {}


def count_moves(moves, depth):
    """A recursive solution with caching, adapted from problem 2024-11
    moves is a sequence of moves to press a button. Each button press
    has zero to three directional moves (depending on the start location),
    then an A.  This solution uses a look up in the keys dictionary,
    which is the optimal path from one button to the other."""

    if depth < 0:
        raise ValueError
    if depth == 0:
        return len(moves)
    if (moves, depth) in cache:
        return cache[(moves, depth)]
    start = "A"
    count = 0
    for char in moves:
        move_options = keys[(start, char)]
        if isinstance(move_options, list):
            min_count = 1e15
            for move in move_options:
                c = count_moves(move, depth - 1)
                if c < min_count:
                    min_count = c
            count += min_count
        else:
            count += count_moves(move_options, depth - 1)
        start = char
    cache[(moves, depth)] = count
    return count


"""
number_keys is a lookup table of the directional buttons to press to make a
robot move from one numeric button to another on the following pad:
     7 8 9
     4 5 6
     1 2 3
     - 0 A
Even though one of the choices is usually better, it turns out through
testing, that this is true for less than 4 directional button pads,
it is not always true, in larger sequences, so we must check all options.
This may not always be necessary.  I don't think >^> will ever be shorter
than >>^ or ^>>, but we test them all anyway.
I am only providing the necessary look ups for my input codes:
     839A
     169A
     579A
     670A
     638A
"""
number_keys = {
    # 7 8 9
    # 4 5 6
    # 1 2 3
    # _ 0 A
    # 839A
    # 169A
    # 579A
    # 670A
    # 638A
    ("A", "8"): ["<^^^A", "^<^^A", "^^<^A", "^^^<A"],
    ("8", "3"): [">vvA", "v>vA", "vv>A"],
    ("3", "9"): ["^^A"],
    ("9", "A"): ["vvvA"],
    ("A", "1"): ["^<<A", "<^<A"],
    ("1", "6"): ["^>>A", ">^>A", ">>^A"],
    ("6", "9"): ["^A"],
    ("A", "5"): ["<^^A", "^<^A", "^^<A"],
    ("5", "7"): ["^<A", "<^A"],
    ("7", "9"): [">>A"],
    ("A", "6"): ["^^A"],
    ("6", "7"): ["<<^A", "<^<A", "^<<A"],
    ("7", "0"): [">vvvA", "v>vvA", "vv>vA"],
    ("0", "A"): [">A"],
    ("6", "3"): ["vA"],
    ("3", "8"): ["<^^A", "^<^A", "^^<A"],
    ("8", "A"): [">vvvA", "v>vvA", "vv>vA", "vvv>A"],
}

"""
keys is a lookup table of the directional buttons to press to make a
robot move from one direction button to another on the following pad
- ^ A
< v >
Even though one of the choices is usually better, it turns out through
testing, that it is not always true, so we must check all options.
This may not always be necessary.  I don't think >^> will ever be shorter
than >>^ or ^>>, but we test them all anyway.
"""
keys = {
    ("^", "^"): "A",
    ("^", "A"): ">A",
    ("^", ">"): [">vA", "v>A"],  # "v>A" better of two choices: ['>vA', 'v>A']
    ("^", "v"): "vA",
    ("^", "<"): "v<A",
    #
    ("A", "A"): "A",
    ("A", ">"): "vA",
    ("A", "v"): ["v<A", "<vA"],  # "<vA" better of two choices: ['v<A', '<vA']
    ("A", "<"): ["v<<A", "<v<A"],  # v<<A is better of ["v<<A", "<v<A"]
    ("A", "^"): "<A",
    #
    (">", ">"): "A",
    (">", "v"): "<A",
    (">", "<"): "<<A",
    (">", "^"): ["<^A", "^<A"],  # "<^A" better of two choices: ['<^A', '^<A']
    (">", "A"): "^A",
    #
    ("v", "v"): "A",
    ("v", "<"): "<A",
    ("v", "^"): "^A",
    ("v", "A"): ["^>A", ">^A"],  # "^>A" better of two choices: ['^>A', '>^A']
    ("v", ">"): ">A",
    #
    ("<", "<"): "A",
    ("<", "^"): ">^A",
    ("<", "A"): [">>^A", ">^>A"],  # >>^A is better option in [">>^A", ">^>A"]
    ("<", ">"): ">>A",
    ("<", "v"): ">A",
}


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
