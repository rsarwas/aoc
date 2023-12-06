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
        total *= ways_to_win_simple(race)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    race = parse2(lines)
    total = ways_to_win_simple(race)
    return total


def parse(lines):
    """Convert input lines into lists of times and distances"""
    times = lines[0].replace("Time: ", "").strip().split(" ")
    times = [int(time) for time in times if time]
    distances = lines[1].replace("Distance: ", "").strip().split(" ")
    distances = [int(distance) for distance in distances if distance]
    return times, distances


def parse2(lines):
    """Convert input lines into one time and one distance"""
    time = int(lines[0].replace("Time: ", "").strip().replace(" ", ""))
    distance = int(lines[1].replace("Distance: ", "").strip().replace(" ", ""))
    return time, distance


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


def ways_to_win_simple(race):
    """Count the number of speeds that will win the race

    Fastest solution in terms of thinking and coding, but
    slowest execution.  In this case it is fast enough (< 5sec for both parts)"""
    time, distance = race
    wins = 0
    for speed in range(1, time):
        if (time - speed) * speed > distance:
            wins += 1
    return wins


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
