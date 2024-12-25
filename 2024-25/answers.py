"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    keys, locks = split(data)
    keys = encode_keys(keys)
    locks = encode_locks(locks)
    # print(keys)
    # print(locks)
    total = 0
    for key in keys:
        for lock in locks:
            if fit(key, lock):
                total += 1
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    return "Merry Christmas!"


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    n = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        key_id = n // 7
        row = n % 7
        if row == 0:
            key = []
            data.append(key)
        key.append(line)
        n += 1
    return data


def split(data):
    """Split the data into keys and locks"""
    keys = []
    locks = []
    for item in data:
        if item[0] == "#####":
            locks.append(item)
        else:
            keys.append(item)
    return keys, locks


def encode_keys(items):
    """Encode the height of the teeth on the key"""
    keys = []
    for item in items:
        key = [0, 0, 0, 0, 0]
        for col in range(5):
            for row in range(7):
                if item[row][col] == "#":
                    key[col] = row
                    break
        keys.append(key)
    return keys


def encode_locks(items):
    """Encode the height of the teeth on the key"""
    locks = []
    for item in items:
        lock = [0, 0, 0, 0, 0]
        for col in range(5):
            for row in range(7):
                if item[row][col] == ".":
                    lock[col] = row
                    break
        locks.append(lock)
    return locks


def fit(key, lock):
    """Test if a key fits in a lock"""
    for index in range(5):
        if lock[index] > key[index]:
            return False
    return True


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
