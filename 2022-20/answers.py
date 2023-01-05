"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a random integer in range {-1e5 ,.., 1e5}; integers are NOT unique
# so we cannot search for the number that needs to move; we need to keep track of
# it's current location. Solution is to put each integer in a doubly linked list.
# The linked list will be stored as tuples in a standard python list.

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

DEBUGGING = False


def part1(lines):
    """Solve part 1 of the puzzle."""
    ints = parse(lines)
    ddl = make_doubly_linked_list(ints)
    ddl = mix(ddl)
    result = gps_code(ddl, 0)
    return result


def part2(lines):
    """Solve part 2 of the puzzle."""
    return -1


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    data = [int(line) for line in lines]
    return data


def make_doubly_linked_list(ints):
    """Given a list of ints, return a doubly linked list with the ints.
    The data structure is a standard python list with each entry being
    a (prev, value, next) tuple, where prev and next are the indexes in
    the list of the previous and next items in the list. items do not
    in the standard list."""
    ddl = []
    size = len(ints)
    for i, value in enumerate(ints):
        prev = (i - 1) % size
        next_ = (i + 1) % size
        item = (prev, value, next_)
        ddl.append(item)
    return ddl


def mix(ddl):
    """Mix up the doubly linked list (ddl) by shifting each item to a new location
    in the list. The value of the item is the distance to move it (left for negative
    numbers). The list is circular.
    Unclear if the item should be removed from the list before finding the new location,
    or after.  This only applies to abs(value) > len(ddl), but that never happens in
    the test input, but happens about 50% of the time in the puzzle input. Removing the
    item from the list _BEFORE_ finding the new location returns the correct answer!"""
    if DEBUGGING:
        display(ddl)
    for ptr, item in enumerate(ddl):
        offset = item[1]
        # Removing the item from the list _BEFORE_ finding the new location
        # returns the correct answer!
        remove(ddl, ptr)
        before = get_previous_ptr(ddl, ptr, offset)
        add(ddl, ptr, before)
        if DEBUGGING:
            display(ddl)
    return ddl


def get_previous_ptr(ddl, ptr, offset):
    """Returns the left side (node before) the location that
    offset moves from the location of the node at ptr.
    offset can be positive or negative."""
    prev = ddl[ptr][0]
    next_ = ddl[ptr][2]
    while offset > 1:
        next_ = ddl[next_][2]
        offset -= 1
    if offset == 1:
        return next_
    while offset < 0:
        prev = ddl[prev][0]
        offset += 1
    return prev


def remove(ddl, ptr):
    """Remove the item at ptr from the doubly linked list."""
    prev = ddl[ptr][0]
    next_ = ddl[ptr][2]
    update_prev(ddl, next_, prev)
    update_next(ddl, prev, next_)


def add(ddl, ptr, after):
    """Add the doubly linked list node at ptr to the spate after the node at after.
    the node in ptr is assumed in the data structure (a standard python list), but
    not necessarily connected to the next/prev items in the list."""
    next_ = ddl[after][2]
    prev = after
    update_next(ddl, prev, ptr)
    update_prev(ddl, ptr, prev)
    update_next(ddl, ptr, next_)
    update_prev(ddl, next_, ptr)


def update_prev(ddl, ptr, prev):
    """Update the previous pointer of the item at ptr in ddl to prev."""
    ddl[ptr] = (prev, ddl[ptr][1], ddl[ptr][2])


def update_next(ddl, ptr, next_):
    """Update the next pointer of the item at ptr in ddl to next."""
    ddl[ptr] = (ddl[ptr][0], ddl[ptr][1], next_)


def gps_code(ddl, value):
    """Get the sum of three values in the doubly linked list.
    Values are at index of value + 1000, 2000, and 3000."""
    ptr = find_value(ddl, value)
    result = 0
    for _ in range(3):
        ptr = get_previous_ptr(ddl, ptr, 1000)
        if DEBUGGING:
            print(ddl[ptr][1])
        result += ddl[ptr][1]
    return result


def find_value(ddl, value):
    """Find the pointer to the node in ddl containing value."""
    for i, item in enumerate(ddl):
        if item[1] == value:
            return i
    return None


def display(ddl):
    """Prints the doubly linked list in the correct order.
    The node at index 0 is always printed first."""
    output = [ddl[0][1]]
    ptr = ddl[0][2]
    while ptr != 0:
        output.append(ddl[ptr][1])
        ptr = ddl[ptr][2]
    print(output)


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
