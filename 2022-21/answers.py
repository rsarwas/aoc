"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the puzzle."""
    data = parse(lines)
    result = solve(data, "root", 1, None)
    return int(result)


def part2(lines):
    """Solve part 2 of the puzzle."""
    data = parse(lines)
    lower, upper = -1e15, 1e15
    # To confirm upper and lower bounds, manually use explore(data).  Will speed up interpolation.
    if INPUT == "input.txt":
        lower, upper = 3e12, 4e12
    if INPUT == "test.txt":
        # in the test data, the left side grows with larger inputs, so reverse upper and lower
        lower, upper = 400, 300
    return interpolate(data, lower, upper)


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    data = {}
    for line in lines:
        line = line.strip()
        name, job = line.split(": ")
        try:
            name1, operation, name2 = job.split(" ")
            job = (operation, name1, name2)
        except ValueError:
            operation = "yell"
            val = int(job)
            job = (operation, val)
        data[name] = job
    return data


def solve(data, monkey, version, value):
    """Solve the puzzle."""
    # pylint: disable=too-many-return-statements

    if monkey == "humn" and version == 2:
        return value
    job = data[monkey]
    if job[0] == "yell":
        return job[1]

    operation, monkey1, monkey2 = job
    if operation == "*":
        return solve(data, monkey1, version, value) * solve(
            data, monkey2, version, value
        )
    if operation == "/":
        return solve(data, monkey1, version, value) / solve(
            data, monkey2, version, value
        )
    if operation == "+":
        return solve(data, monkey1, version, value) + solve(
            data, monkey2, version, value
        )
    if operation == "-":
        return solve(data, monkey1, version, value) - solve(
            data, monkey2, version, value
        )
    print("PANIC. unexpected job")
    return -1


def explore(data):
    """Manually look for the bounds of the solution."""
    _, monkey1, monkey2 = data["root"]
    # for val in [100, 200, 300, 400]:  # test puzzle
    for val in [1e12, 2e12, 3e12, 4e12, 5e12]:
        left = solve(data, monkey1, 2, val)
        right = solve(data, monkey2, 2, val)
        if left == right:
            print("the winner is", val)
        else:
            verdict = "too small" if left < right else "too big"
            print("val", val, "is", verdict, "left", left, "right", right)


def interpolate(data, lower, upper):
    """Interpolate to a solution given the upper and lower bounds."""
    _, monkey1, monkey2 = data["root"]
    val = (lower + upper) // 2
    left = solve(data, monkey1, 2, val)
    right = solve(data, monkey2, 2, val)
    safety = 0
    while left != right and safety < 50:
        # print(upper, lower, left - right)
        if left < right:
            upper = val
        else:
            lower = val
        val = (lower + upper) // 2
        left = solve(data, monkey1, 2, val)
        right = solve(data, monkey2, 2, val)
        safety += 1
    return int(val)


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
