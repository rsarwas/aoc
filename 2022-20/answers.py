"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a random integer in range {-1e5 ,.., 1e5}; integers are NOT unique
# so we cannot search for the number that needs to move; we need to keep track of
# it's current location.  Therefore the following simple brute force solution will
# not work: find n, then swap it n times with the element after (or before for negative n)
# Puzzle specifies that list is "circular", so moving a number off one end of the
# list wraps back around to the other end as if the ends were connected.
# it isn't clear what should happen if the move is so large that it passes the
# original location. i.e. does it step wise swap with it's neighbor n times, so
# number may move multiple spaces for each loop around the list, or is it a
# enough to figure the final resting place (distance mod list length), and then
# move each intervening number once.  The puzzle input is 5000 numbers, with many
# numbers greater than +/-5000, so this situation will occur many times.

# Current solution works correctly with the test data
# but yields incorrect answer of 4326 (too low) for part1.

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"

DEBUGGING = True


def part1(lines):
    """Solve part 1 of the puzzle."""
    data = parse(lines)
    data = mix(data)
    result = gps_code(data, 0)
    return result


def part2(lines):
    """Solve part 2 of the puzzle."""
    return -1


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    data = [int(line) for line in lines]
    return data


def mix(data):
    """Mix up the data by shifting each number to a new location in the list.
    The value of the number is the distance to move it (left for negative numbers).
    The list is circular.  If a number ends up between the first and last,
    it goes at the end."""

    if DEBUGGING:
        print("Initial arrangement:")
        print(data)

    indexes = list(range(len(data)))  # starts the same as the original indexes
    new_data = list(data)  # will be updated at the end with the reorganized list
    size = len(data)
    for index, value in enumerate(data):
        index = indexes[index]  # current location of value
        left = index + value
        if value < 0:
            left -= 1
        left %= size

        if DEBUGGING:
            right = left + 1
            right %= size
            left_value, right_value = None, None
            for i, i_value in enumerate(indexes):
                if i_value == left:
                    left_value = data[i]
                if i_value == right:
                    right_value = data[i]
            print(f"\n{value} moves between {left_value} and {right_value}")

        # if left == index or left == index - 1:
        # Move the number to the same spot, so do nothing
        if left < index - 1:  # shift numbers to the right
            for i, i_value in enumerate(indexes):
                if left <= i_value <= index:
                    indexes[i] = i_value + 1
                if i_value == index:
                    indexes[i] = left + 1  # right
        elif index < left:  # shift numbers to the left
            for i, i_value in enumerate(indexes):
                if index < i_value <= left:
                    indexes[i] = i_value - 1
                if i_value == index:
                    indexes[i] = left

        if DEBUGGING:
            # Generate the data in the current order for printing
            for i, index in enumerate(indexes):
                new_data[index] = data[i]
            print(new_data)

    # Return the data in the current ordering
    for i, index in enumerate(indexes):
        new_data[index] = data[i]
    return new_data


def gps_code(data, value):
    """Get the sum of three values in the rearranged list.
    Values are at index of val + 1000, 2000, and 3000."""
    code = 0
    length = len(data)
    v_index = data.index(value)
    for i in [1000, 2000, 3000]:
        index = (v_index + i) % length
        code += data[index]
    return code


def test_uniqueness(lines):
    """Test if the integers in the input list are unique. For debugging"""
    data = parse(lines)
    print("Values are unique:", len(set(data)) == len(data))


def test_indexing():
    """Test the indexing algorithm. For debugging"""
    test_indexing2([1, 2, 3, 1, 7])
    # [1, 2, 3, 1, 7]
    # 1 moves between 2 and 3 => [2, 1, 3, 1, 7]
    # 2 moves between 1 and 7 => [1, 3, 1, 2, 7]
    # 3 moves between 1 and 2 => [1, 3, 2, 1, 7]
    # 1 moves between 7 and 1 => [1, 2, 3, 7, 1]
    # 7 moves between 2 and 3 => [1, 2, 7, 3, 1]
    test_indexing2([-7, -1, -3, -2, -1])
    # [-7, -1, -3, -2, -1]
    # -7 moves between -3 and -2 => [-1, -3, -7, -2, -1]
    # -1 moves between -1 and -7 => [-7, -3, -2, -1, -1]
    # -3 moves between -2 and -1 => [-7, -1, -2, -3, -1]
    # -2 moves between -7 and -1 => [-7, -2, -1, -3, -1]
    # -1 moves between -3 and -2 => [-7, -1, -3, -1, -2]


def test_indexing2(data):
    """Test the indexing algorithm. For debugging"""
    print(data)
    size = len(data)
    for index, value in enumerate(data):
        left = index + value
        if value < 0:
            left -= 1
        left %= size
        right = left + 1
        right %= size
        # print(index, left, right)

        # right will always be greater than left
        #   unless left is the last element then right is 0

        new_data = list(data)
        # if left == index or left == index - 1:
        # Move the number to the same spot, so do nothing
        if left < index - 1:  # shift numbers to the right
            for i in range(index, left, -1):
                new_data[i] = data[i - 1]
            new_data[right] = value
        elif index < left:  # shift numbers to the left
            for i in range(index + 1, left + 1):
                new_data[i - 1] = data[i]
            new_data[left] = value

        print(f"{value} moves between {data[left]} and {data[right]} => {new_data}")


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    # test_uniqueness(lines)
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
    # test_indexing()
