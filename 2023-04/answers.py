"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# _wins_ is an int list of wins on each line
# _cards_ is a number of the scratch cards held for each line


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    total = 0
    wins = [count_wins(line) for line in lines]
    for win in wins:
        if win > 0:
            # double for each win: 1 => 1; 2 => 2, 3 => 4, 4 => 8
            total += 2 ** (win - 1)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    cards = [1] * len(lines)
    wins = [count_wins(line) for line in lines]
    for card_id, win in enumerate(wins):
        num_cards = cards[card_id]
        for _ in range(num_cards):
            for offset in range(1, win + 1):
                cards[card_id + offset] += 1
    return sum(cards)


def count_wins(line):
    "Count the wins on each line"
    line = line.strip()
    parts = line.split(": ")
    line = parts[1]
    parts = line.split(" | ")
    winning = [a for a in parts[0].split(" ") if a != ""]
    held = [a for a in parts[1].split(" ") if a != ""]
    count = 0
    for num in held:
        if num in winning:
            count += 1
    return count


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
