"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    track, start, end = parse(lines)
    measure(track, start, end)
    # print(start, track[start])
    # print(end, track[end])
    cheats = find_cheats(track, 102)
    # for loc1, loc2 in cheats:
    #     print(loc1, loc2, track[loc2] - track[loc1] - 2)
    # print(track)
    total = len(cheats)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    track = {}
    start, end = None, None
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == ".":
                track[(row, col)] = -1
            if char == "S":
                start = (row, col)
                track[(row, col)] = 0
            if char == "E":
                end = (row, col)
                track[(row, col)] = -1
    return track, start, end


def measure(track, start, end):
    """Assigns each element in the track the distance from the start."""
    current = start
    distance = 0
    while current != end:
        current = find_next(track, current)
        if not current:
            print("Oh, No, we have no where to go!")
            break
        distance += 1
        track[current] = distance


def find_next(track, current):
    """Return the next (row,col) in the track from current,
    Assume there is only one path trough the maze.
    unvisited tracks will have a value of -1."""
    row, col = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next = (row + dr, col + dc)
        if next in track and track[next] == -1:
            return next
    return None


def find_cheats(track, savings):
    """Return a list of cheats that have at save at least savings.
    A cheat has point 1 and 2 on the track, and they differ in the row
    or column by exactly 2 space, and the distance (measure) is from
    1 to 2 is at least savings."""
    cheats = []
    ordered = ordered_track(track)
    for index, loc1 in enumerate(ordered[:-savings]):
        for loc2 in ordered[index + savings :]:
            row1, col1 = loc1
            row2, col2 = loc2
            if (row1 == row2 and abs(col2 - col1) == 2) or (
                col1 == col2 and abs(row2 - row1) == 2
            ):
                cheats.append((loc1, loc2))
    return cheats


def ordered_track(track):
    """Return an ordered list of the track locations"""
    ordered = [(val, key) for (key, val) in track.items()]
    ordered.sort()
    ordered = [loc for (dist, loc) in ordered]
    return ordered


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
