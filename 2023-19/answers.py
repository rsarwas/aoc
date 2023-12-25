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
START = "in"


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
    rules, _ = parse(lines)
    total = 0
    true, false = reverse_rules(rules)
    # print(true)
    # print(false)
    start = ACCEPT
    end = START
    # ranges is a dictionary of valid min,max values for each variable
    # each branch in the rule tree will adjust one of the values.
    ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}

    # Print ALL the paths from start to end (for testing number and length of paths)
    # for path in reverse_apply_rules_paths(start, end, true, false):
    #     print(path)
    list_of_valid_ranges = reverse_apply_rules(start, end, ranges, rules, true, false)
    # for r in list_of_valid_ranges:
    #     print(r)
    total = 0
    for r in list_of_valid_ranges:
        total += count_options(r)
    return total


def count_options(d):
    """d is a dictionary of min/max values. count the valid permutations"""
    total = 1
    for r_min, r_max in d.values():
        r = r_max - r_min + 1
        if r > 0:
            total *= r
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
    name = START
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


def reverse_rules(rules):
    """Return a new dictionary, where keys are swapped for values"""
    false = {}
    for rule_name, rule in rules.items():
        if rule.false_name not in false:
            false[rule.false_name] = []
        false[rule.false_name].append(rule_name)
    true = {}
    for rule_name, rule in rules.items():
        if rule.true_name not in true:
            true[rule.true_name] = []
        true[rule.true_name].append(rule_name)
    return true, false


# pylint: disable=too-many-arguments
def reverse_apply_rules(start, end, ranges, rules, true, false):
    """walk the list of rules in true/false backwards, from start to end
    There will be multiple ways to do this. each variant will have trimmed
    the ranges down to a limited set of values that if used as inputs at end
    will guarantee an outcome of start if applied in the correct order."""
    if start == end:
        return [ranges]
    new_ranges = []
    if start in true:
        for rule_name in true[start]:
            new_range = update_ranges(dict(ranges), rules[rule_name], "left")
            new_ranges += reverse_apply_rules(
                rule_name, end, new_range, rules, true, false
            )
    if start in false:
        for rule_name in false[start]:
            new_range = update_ranges(dict(ranges), rules[rule_name], "right")
            new_ranges += reverse_apply_rules(
                rule_name, end, new_range, rules, true, false
            )

    return new_ranges


def reverse_apply_rules_paths(start, end, true, false):
    """A recursive function to walk the list of rules in true/false backwards,
    from start to end. It returns a list of paths.  Used for testing and
    debug printing."""
    if start == end:
        return [end]
    results = []
    if start in true:
        for rule_name in true[start]:
            paths = reverse_apply_rules_paths(rule_name, end, true, false)
            results += [f"{start} <t- {path}" for path in paths]
    if start in false:
        for rule_name in false[start]:
            paths = reverse_apply_rules_paths(rule_name, end, true, false)
            results += [f"{start} <f- {path}" for path in paths]
    return results


def update_ranges(ranges, rule, branch):
    """Use the rule to reduce the input range too passing values"""
    v_min, v_max = ranges[rule.variable]
    if branch == "left":
        if rule.operation == "<":
            v_max = min(v_max, rule.value - 1)
        else:  # rule.operation == ">"
            v_min = max(v_min, rule.value + 1)
    else:  # branch == "right"
        if rule.operation == "<":
            v_min = max(v_min, rule.value)
        else:  # rule.operation == ">"
            v_max = min(v_max, rule.value)
    ranges[rule.variable] = (v_min, v_max)
    return ranges


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
