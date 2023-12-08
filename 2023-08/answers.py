"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import math  # for the lowest common multiple (lcm) function

INPUT = "input.txt"
LEFT = "L"
RIGHT = "R"
START = "AAA"
END = "ZZZ"


class Node:
    """A simple tree node.
    It uses a class/static variable to store a dictionary of nodes by name
    to facilitate construction of the node tree"""

    nodes = {}

    name = ""
    left_name = None
    right_name = None
    left_node = None
    right_node = None

    def __init__(self, s):
        """Initialize a node instance.
        s is a string in the format 'AAA = (BBB, CCC)\n'."""

        self.name, children = s.strip().split(" = (")
        self.left_name, self.right_name = children.replace(")", "").split(", ")

        Node.nodes[self.name] = self
        if self.left_name in Node.nodes:
            self.left_node = Node.nodes[self.left_name]
        if self.right_name in Node.nodes:
            self.right_node = Node.nodes[self.right_name]

    def left(self):
        "Return the left node.child, looking it up if not already defined"
        if self.left_node is None:
            self.left_node = Node.nodes[self.left_name]
        return self.left_node

    def right(self):
        "Return the right node.child, looking it up if not already defined"
        if self.right_node is None:
            self.right_node = Node.nodes[self.right_name]
        return self.right_node

    def get(self, move):
        """Use a move instruction to get a child."""
        if move == RIGHT:
            return self.right()
        if move == LEFT:
            return self.left()
        print("Invalid request {s} not one of '{LEFT}', '{RIGHT}'")
        return None

    # pylint: disable=no-method-argument
    # static/class method, so no self
    def part2_starts():
        """Return a list of starting nodes for part2"""
        starts = []
        for node in Node.nodes.values():
            if node.name.endswith(START[-1]):
                starts.append(node)
        return starts


def part1(lines):
    """Solve part 1 of the problem."""
    path, start = parse(lines)
    current = start
    steps = 0
    while True:
        index = steps % len(path)
        move = path[index]
        current = current.get(move)
        steps += 1
        if current.name == END:
            break
    return steps


def part2(lines):
    """Solve part 2 of the problem.
    Brute force solution was too slow.  Inspecting the input, there are 6 starting nodes, and
    six ending nodes.  Inspecting the path through the nodes for when ending nodes are found,
    I discovered that the paths get stuck in infinite loops:
    AAA -> ZZZ at step 20569, 41138, 61707, ... repeating forever, never finding another ending node
    STA -> XGZ at step 18113, 36226, 54339, ... ditto
    GPA -> LLZ at step 21797, 43594, 65391, ... ditto
    Assume the others follow suit, and the answer is the lowest common multiple of the 6 loop sizes
    """
    path, _ = parse(lines)
    currents = Node.part2_starts()
    steps = 0
    loop_size = [0] * len(currents)
    while True:
        index = steps % len(path)
        move = path[index]
        # print(f"{steps}{move}: {" ".join([n.name for n in currents])}")
        for index, current in enumerate(currents):
            currents[index] = current.get(move)
            if current.name.endswith(END[-1]):
                loop_size[index] = steps
        # Move the increment until after to get the right numbers in loop_size
        steps += 1
        if all_done(loop_size):
            break
    print(loop_size)
    total_steps = math.lcm(*loop_size)
    return total_steps


def parse(lines):
    """Convert the lines of text into a useful data model."""
    path = lines[0].strip()
    start = None
    for line in lines[2:]:
        node = Node(line)
        if node.name == START:
            start = node
    return path, start


def all_done(steps):
    """All the step counts are greater than zero"""
    for step in steps:
        if step == 0:
            return False
    return True


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
