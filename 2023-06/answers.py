"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    times, distances = parse(lines)
    total = 1
    for race in zip(times, distances):
        total *= ways_to_win(race)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    total = -1
    return min(total, len(lines))


def parse(lines):
    """Convert input lines into lists of times and distances"""
    times = lines[0].replace("Time: ", "").strip().split(" ")
    times = [int(time) for time in times if time]
    distances = lines[1].replace("Distance: ", "").strip().split(" ")
    distances = [int(distance) for distance in distances if distance]
    return times, distances


def ways_to_win(race):
    """Count the number of speed that will win the race"""
    time, distance = race
    min_speed = (distance // time) + 1
    # hold_time == speed; we win if time - hold_time) * speed > distance
    while (time - min_speed) * min_speed <= distance:
        min_speed += 1
    max_speed = min_speed
    while max_speed < time and (time - max_speed) * max_speed > distance:
        max_speed += 1
    max_speed -= 1  # last speed was no good
    winning_speeds = 1 + max_speed - min_speed
    return winning_speeds


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
