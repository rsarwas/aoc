"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    # print(data)
    total = 0
    for machine in data:
        # print(machine)
        config = find_min_config(machine)
        # print(config)
        if len(config) > 4:
            print(len(config))
        total += len(config)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        line = line[1:-1]  # remove leading "[" and trailing "}"
        lights, rest = line.split("] ")
        lights = [x == "#" for x in lights]
        button_lists, joltage = rest.split(" {")
        button_lists = button_lists[1:-1].split(") (")
        buttons = [[int(y) for y in x.split(",")] for x in button_lists]
        joltage = [int(x) for x in joltage.split(",")]
        machine = (lights, buttons, joltage)
        data.append(machine)
    return data


def find_min_config(machine):
    """Return the shortest list of button pushes to configure the machine"""
    final_state, buttons, _ = machine
    initial_state = [False] * len(final_state)
    if initial_state == final_state:
        return []
    n = 1
    while True:
        for config in all_configs_of_length(n, buttons):
            # print("testing", config)
            if test_config(initial_state, final_state, config, buttons):
                return config
        n += 1
        if n == 11:
            print("oh no, need more than 10 button pushes")
            print(initial_state, final_state, buttons)
            return []


def all_configs_of_length(n, buttons):
    configs = []
    ids = range(len(buttons))
    for id in ids:
        configs.append([id])
    while n > 1:
        old_configs = list(configs)
        configs = []
        for config in old_configs:
            for id in ids:
                configs.append(config + [id])
        n -= 1
    return configs


def test_config(initial_state, final_state, config, buttons):
    """Return true if the list of button pushes in config
    will create the final_state from the initial state"""
    results = apply(config, initial_state, buttons)
    # print(initial_state, "*", config, "=", results, "?==?", final_state)
    return results == final_state


def apply(config, initial_state, buttons):
    """apply the config to the initial_state"""
    state = list(initial_state)
    for button_id in config:
        button = buttons[button_id]
        for light_id in button:
            state[light_id] = not state[light_id]
    return state


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
