"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# rule has a name (key in rules dict), variable name, GT or LT, value,
# true rule name, false rule name
# rules A and R are accept and reject respectively and halt processing
# part is a a dictionary with four keys x,m,a,s
# the parts list in the input is almost JSON, add a comma to the end of each line;
# prefix with '[', wrap the keys in double quotes
# and suffix with ']' and replace all "=" with ":"


import os.path  # to get the directory name of the script (current puzzle year-day)
import json  # for parsing parts
from collections import namedtuple

INPUT = "input.txt"
ACCEPT = "A"
REJECT = "R"


Rule = namedtuple("Rule", "variable, operation, value, true_name, false_name")


def part1(lines):
    """Solve part 1 of the problem."""
    rules, parts = parse(lines)
    total = 0
    for part in parts:
        if apply_rules(rules, part) == ACCEPT:
            total += sum(part.values())
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    rules = []
    parts = []
    i = lines.index("\n")
    rules = parse_rules(lines[:i])
    parts = parse_parts(lines[i + 1 :])
    return rules, parts


def parse_rules(lines):
    "Return a dictionary of rules"
    rules = {}
    for line in lines:
        name, data = line.split("{")
        data = data[:-2]  # remove "}\n" from end
        while data:
            # the true branch and the false branch will be one of "A", "R", the name of a
            # well known rule, or a interior rule (that can be parsed and treated like any
            # other rule once it has a look-up name) each rule will only have one chained rule.
            # data is the string for a chained set of rules, given the name: int_name
            rule, int_name, data = parse_rule(data)
            rules[name] = rule
            name = int_name
    return rules


def parse_rule(data):
    """Parse a rule from a string definition.
    Return the name and data for an interior (chained) rule"""
    variable = data[0]
    operation = data[1]
    i = data.index(":")
    value = int(data[2:i])
    data = data[i + 1 :]
    i = data.index(",")
    left = data[:i]
    right = data[i + 1 :]
    if ":" in left:
        name = make_unique_name()
        rule = Rule(variable, operation, value, name, right)
        return rule, name, left
    if ":" in right:
        name = make_unique_name()
        rule = Rule(variable, operation, value, left, name)
        return rule, name, right
    rule = Rule(variable, operation, value, left, right)
    return rule, None, None


def make_unique_name():
    """return a unique string for an interior rule name"""
    # create the equivalent of a C static variable.
    if not hasattr(make_unique_name, "counter"):
        make_unique_name.counter = 0
    make_unique_name.counter += 1
    return f"my_rule{make_unique_name.counter}"


def parse_parts(lines):
    """Return a list of parts from the input lines"""
    # separate objects with a ";" temporarily
    blob = ";".join([line.strip() for line in lines])
    # reformat as an object encase keys in double quotes and separate key/value with ':'
    blob = blob.replace("=", '":')
    blob = blob.replace(",", ',"')
    blob = blob.replace("{", '{"')
    # make it a list of objects
    blob = "[" + blob + "]"
    blob = blob.replace(";", ",")
    parts = json.loads(blob)
    return parts


def apply_rules(rules, part):
    """Apply the set of sorting rules to the part, return the final ACCEPT or REJECT rule"""
    name = "in"
    while name not in [ACCEPT, REJECT]:
        name = apply_rule(rules[name], part)
    return name


def apply_rule(rule, part):
    """Return the name of the next rule to apply after applying rule to part"""
    part_value = part[rule.variable]
    if rule.operation == "<":
        if part_value < rule.value:
            return rule.true_name
        return rule.false_name
    # rule.operation == ">":
    if part_value > rule.value:
        return rule.true_name
    return rule.false_name


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
