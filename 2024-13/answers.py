"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    n = 1
    for machine in data:
        solution = solve(machine)
        if is_valid(solution):
            total += cost(solution)
    return int(round(total, 5))


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = 0
    n = 1
    for machine in data:
        button_a, button_b, prize = machine
        prize = [10000000000000 + x for x in prize]
        machine = (button_a, button_b, prize)
        solution = solve(machine)
        if is_valid(solution):
            total += cost(solution)
    return int(round(total, 3))


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    i = 0
    while i + 3 <= len(lines):
        button_a = lines[i + 0].strip().replace("Button A: X+", "").split(", Y+")
        button_a = [int(x) for x in button_a]
        button_b = lines[i + 1].strip().replace("Button B: X+", "").split(", Y+")
        button_b = [int(x) for x in button_b]
        prize = lines[i + 2].strip().replace("Prize: X=", "").split(", Y=")
        prize = [int(x) for x in prize]
        machine = (button_a, button_b, prize)
        data.append(machine)
        i += 4
    return data


def solve(machine):
    """Solve a simple system of linear equations
    a1*x + b1*y = c1
    a2*x + b2*y == c2

    where x is the number of button pushes for A and y is for B.
    a1,b1,c1 are distances along the X axis  and a2,b2,c2 are along y."""
    button_a, button_b, prize = machine
    a1, a2 = button_a
    b1, b2 = button_b
    c1, c2 = prize
    y = (c1 - c2 * a1 / a2) / (b1 - b2 * a1 / a2)
    x = (c1 - b1 * y) / a1
    return (x, y)


def is_valid(solution):
    """Checks if the solution is valid. i.e. a positive number of integral button pushes"""
    a, b = solution
    # round the numbers to remove floating point epsilon
    a, b = round(a, 3), round(b, 3)
    return a > 0 and b > 0 and int(a) == a and int(b) == b


def cost(solution):
    """return the cost of the solution"""
    a, b = solution
    return a * 3 + b


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
