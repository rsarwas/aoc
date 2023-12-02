"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# Games are stored in an array; the game id is the index + 1
# A game is an array of groups. A group is an rgb tuples (#red, #green, #blue)
# representing the number of red, green and blue cubes in the group

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    total = 0
    rgb_limit = (12, 13, 14)  # (red, green, blue)
    games = parse(lines)
    for index, game in enumerate(games):
        game_id = index + 1
        if valid(game, rgb_limit):
            total += game_id
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    total = 0
    games = parse(lines)
    for game in games:
        total += power(game)
    return total


def parse(lines):
    """Convert a list of lines into a list of games
    See the data model above for the structure of a game"""
    games = []
    for line in lines:
        line = line.strip()
        line = line[line.find(":") + 2 :]  # remove "Game id: "
        groups = line.split("; ")
        game = []
        for group in groups:
            red, green, blue = 0, 0, 0
            cubes = group.split(", ")
            for cube in cubes:
                qty, color = cube.split(" ")
                if color == "red":
                    red = int(qty)
                elif color == "green":
                    green = int(qty)
                elif color == "blue":
                    blue = int(qty)
                else:
                    print(f"Ignoring Unexpected input: set = {set}")
            game.append((red, green, blue))
        games.append(game)
    return games


def valid(game, rgb):
    """Determine if a game is valid
    That is it has less than the maximum rgb value in each group"""
    max_red, max_green, max_blue = rgb
    for group in game:
        red, green, blue = group
        if red > max_red or green > max_green or blue > max_blue:
            return False
    return True


def power(game):
    """Find the power of a game:
    power is minimum # or red, min green, min blue"""
    min_red, min_green, min_blue = (0, 0, 0)
    for group in game:
        red, green, blue = group
        if red > min_red:
            min_red = red
        if green > min_green:
            min_green = green
        if blue > min_blue:
            min_blue = blue
    return min_red * min_green * min_blue


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
