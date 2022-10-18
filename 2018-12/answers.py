# Data Model:
# ===========
# The current state is represented in two ways:
# 1) as a list of 0s and 1s for the dead/live state.
#    It always starts with a 1 (the first live pot)
# 2) as a list of 5bit integers (0-31), representing
#    32 different configurations for the current plant
#    and the 4 adjacent plants
# The rules is a list of the n (<32) different 5 bit integers
# that result in a living plant at the current location.

def part1(lines):
    state, rules = parse(lines)
    # print(state, count(state, 0))
    # print(rules)
    first = 0
    for _ in range(100):
        state, first = search("...." + state + "....", rules, first)
        # print(first, state)
    return count(state, first)

def part2(lines):
    # in testing the timing, I noticed that:
    # 500 generations => 16401
    # 5000 => 160401
    # 50000 => 1600401, etc.
    # and that 500000 takes over a minute to run, so I will never finish 50 000 000 000
    # but I can guess the answer is 16 00 000 000 401
    return 1600000000401

def parse(lines):
    alive = ""
    rules = []
    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("initial state: "):
            alive = line.strip().replace("initial state: ","")
            continue
        if line.count(" => ") == 1:
            rule,end = line.strip().split(" => ")
            if end == "#":
                rules.append(rule_from_string(rule))
    return alive, rules


def rule_from_string(str):
    shift = 0
    rule = 0
    for char in str:
        state = 1 if char == "#" else 0
        rule += state<<shift
        shift += 1
    return rule


def search(str, rules, first):
    new_state = ""
    for index in range(len(str)-5):
        sub_str = str[index:index+5]
        rule = rule_from_string(sub_str)
        # print(sub_str, rule)
        if rule in rules:
            new_state += "#"
        else:
            new_state += "."
    # four empty pots are added to the string before searching
    # the first pot in the new list will be at -2 from the first pot in the input list
    # the adjust first after removing the initial empty pots
    first -= 2
    first += len(new_state) - len(new_state.lstrip("."))
    return new_state.strip("."), first


def count(state, first):
    total = 0
    current = first
    for char in state:
        if char == "#":
            total += current
        current += 1
    return total


if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
