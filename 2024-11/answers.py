"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    stones = parse(lines)
    # print(stones)
    blink_count = 25
    for _ in range(blink_count):
        stones = blink(stones)
        # print(stones)
    total = len(stones)
    return total


def part2(lines):
    """Solve part 2 of the problem.

    The brute force solution is not practical;
    it starts to slow way down after 25 blinks.

    I noticed that all of the single digits stones will morph into 4 or 8
    single digit stones within 3 to 5 blinks.
    1 -> 2024 -> 20, 24 -> 2, 0, 2, 4 (3 blinks)
    2 -> 4048 -> 40, 48 -> 4, 0, 4, 8
    3 ->                -> 6, 0, 7, 2
    4 -> 8096 -> 90, 96 -> 8, 0, 9, 6 (3 blinks)
    5 -> 10120 -> 20402880 -> 2040, 2880 -> 20, 40, 28, 80 -> 2, 0, 4, 0, 2, 8, 8, 0 (5 blinks)
    6                                                      -> 2, 4, 5, 7, 9 ,4, 5, 6 (5 blinks)
    7
    8
    9 -> 18216 -> 36869184 -> 3686, 9184 -> 36, 86, 91, 84 -> 3, 6, 8, 6, 9, 1, 8, 4 (5 blinks)
    0 -> 1 -> 2024 -> 20, 24 -> 2, 0, 2, 4  (4 blinks)

    All of the double digit numbers decompose in one blink to 2 single digit numbers
    All of the four digit numbers decompose in two blink to 4 single digit numbers
    All of the eight digit numbers decompose in three blink to 8 single digit numbers
    All of the sixteen digit ...

    Therefore if we can confirm that all the initial input numbers will eventually decompose to
    single digits, we can use some sort of exponential math to figure out the
    total count after a given number of blinks

    input: 3935565 31753 437818 7697 5 38 0 123

    lets look at the first number:
    3935565 -> 7965583560 -> 79655, 83560 -> 161221720, x -> 326312761280, y
      326312761280 -> 326312, 761280 -> 326, 312, 761, 280
    It isn't obvious that this input will decompose to single digits quickly

    lets look at 3 digit numbers
    100 to 494 * 2024 -> 202400 to 999856 (6 digit numbers which will decompose to two 3 digit numbers - loop)
    495 to 999 -> 1001880 to 2021976 (7 digit numbers; will grow to 10 digit numbers -> two 5 digit numbers)
    so three digit numbers will goto 3 digit numbers (44%) or 5 digit numbers (56%)

    5 digit numbers:
    10000 to 49407 * 2024 = 2024 0000 to 9999 9768 (8 digit numbers; woot woot)
    49408 to 99999 * 2024 = 1000 01792 to 2023 97976 (9 digit numbers) -> all 12 digit numbers -> four 3 digit numbers
    so five digit numbers will goto single digits (44%) or 3 digit numbers (56%)

    Therefore all numbers will eventually decompose to single digits, but some may take a while
    """
    stones = parse(lines)
    total = 0
    for stone in stones:
        total += count(stone, 75)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return [int(n) for n in lines[0].strip().split()]


def blink(stones):
    """change the stones according to the rules in the problem statement"""
    new_stones = []
    for stone in stones:
        new_stones += change(stone)
    return new_stones


def change(n):
    """Return a list of stones given the number engraved on a stone"""
    digits = str(n)
    if n == 0:
        return [1]
    if len(digits) % 2 == 0:
        mid = len(digits) // 2
        return [int(digits[:mid]), int(digits[mid:])]
    return [n * 2024]


cache = {}


def count(stone, depth):
    """A crazy recursive solution with caching"""
    # print(f"count({stone},{depth})")
    if depth < 0:
        print("error, depth < 0")
        raise ValueError
    if depth == 0:
        return 1
    if (stone, depth) in cache:
        return cache[(stone, depth)]
    if stone == 0:
        if depth <= 4:
            total = [1, 1, 2, 4][depth - 1]
            cache[(stone, depth)] = total
            return total
        else:
            total = 0
            for s in [2, 0, 2, 4]:
                total += count(s, depth - 4)
            cache[(stone, depth)] = total
            return total
    if stone > 0 and stone < 5 and depth <= 3:
        total = [1, 2, 4][depth - 1]
        cache[(stone, depth)] = total
        return total
    if stone in [5, 6, 7, 9] and depth <= 5:
        total = [1, 1, 2, 4, 8][depth - 1]
        cache[(stone, depth)] = total
        return total
    if stone == 8 and depth <= 5:
        total = [1, 1, 2, 4, 7][depth - 1]
        cache[(stone, depth)] = total
        return total
    total = 0
    if (stone > 0 and stone < 8) or stone == 9:
        if stone == 1:
            for s in [0, 4]:  # 2024
                total += count(s, depth - 3)
            total += 2 * count(2, depth - 3)
        if stone == 2:
            for s in [0, 8]:  # 4048
                total += count(s, depth - 3)
            total += 2 * count(4, depth - 3)
        if stone == 3:
            for s in [6, 0, 7, 2]:
                total += count(s, depth - 3)
        if stone == 4:
            for s in [8, 0, 9, 6]:
                total += count(s, depth - 3)
        if stone == 5:
            # for s in [2, 0, 4, 8, 2, 8, 8, 0]:
            total += 2 * count(0, depth - 5)
            total += 2 * count(2, depth - 5)
            total += 1 * count(4, depth - 5)
            total += 3 * count(8, depth - 5)
        if stone == 6:
            for s in [2, 7, 9, 6]:  # [2, 4, 5, 7, 9, 4, 5, 6]
                total += count(s, depth - 5)
            total += 2 * count(4, depth - 5)
            total += 2 * count(5, depth - 5)
        if stone == 7:
            for s in [8, 7, 0, 3]:  # [2, 8, 6, 7, 6, 0, 3, 2]
                total += count(s, depth - 5)
            total += 2 * count(2, depth - 5)
            total += 2 * count(6, depth - 5)
        if stone == 9:
            for s in [3, 9, 1, 4]:  # [3, 6, 8, 6, 9, 1, 8, 4]
                total += count(s, depth - 5)
            total += 2 * count(6, depth - 5)
            total += 2 * count(8, depth - 5)
        cache[(stone, depth)] = total
        return total
    if stone == 8:
        for s in [3, 6, 16192]:  # [3, 2, 7, 7, 2, 6, 16192]
            total += count(s, depth - 5)
        total += 2 * count(2, depth - 5)
        total += 2 * count(7, depth - 5)
        cache[(stone, depth)] = total
        return total
    # generic solver
    digits = str(stone)
    if len(digits) % 2 == 0:
        mid = len(digits) // 2
        s1, s2 = int(digits[:mid]), int(digits[mid:])
        total = count(s1, depth - 1) + count(s2, depth - 1)
        cache[(stone, depth)] = total
        return total
    else:
        s = stone * 2024
        total = count(s, depth - 1)
        cache[(stone, depth)] = total
        return total


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
