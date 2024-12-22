"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    initial_secrets = parse(lines)
    total = 0
    for secret in initial_secrets:
        # print(secret)
        for _ in range(2000):
            secret = next_secrets(secret)
        # print(secret)
        total += secret
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return [int(line) for line in lines]


def next_secrets(secret):
    """Apply the formula in the puzzle to create a new secret"""
    secret ^= 64 * secret
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= 2048 * secret
    secret %= 16777216
    return secret


def test():
    secret = 123
    for _ in range(10):
        secret = next_secrets(secret)
        print(secret)


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
