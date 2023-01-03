# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# data is a list of tuples (msg1, msg2); msg is a nested list of integers
# correct is a list of booleans, on for each msg pair; true if in right order


import ast  # for list eval


def part1(lines):
    data = parse(lines)
    correct = solve(data)
    # find index+1 for each correct message pair
    # problem statement has indexes starting with 1, python starts with 0
    correct_indexes = [i + 1 for i, d in enumerate(correct) if d is True]
    # print(correct_indexes)
    return sum(correct_indexes)


def part2(lines):
    # there is no need to sort all the packets, just find out how many packets are less than
    # "[[2]]"(+1 for the index of [[2]]" and how many are less than [[6]] (+2 for the indexes
    # of both dividers)
    data = parse(lines)
    divider1 = [[2]]
    divider2 = [[6]]
    less_than_d1 = 0
    less_than_d2 = 0
    for msg1, msg2 in data:
        if in_order(msg1, divider1):
            less_than_d1 += 1
        if in_order(msg2, divider1):
            less_than_d1 += 1
        if in_order(msg1, divider2):
            less_than_d2 += 1
        if in_order(msg2, divider2):
            less_than_d2 += 1
    index_d1 = less_than_d1 + 1
    index_d2 = less_than_d2 + 2
    # print(index_d1, index_d2)
    return index_d1 * index_d2


def parse(lines):
    data = []
    index = 0
    while index < len(lines):
        left = ast.literal_eval(lines[index].strip())
        right = ast.literal_eval(lines[index + 1].strip())
        # blank line @ index+2
        index += 3
        item = (left, right)
        data.append(item)
    return data


def solve(data):
    correct = []
    for (msg1, msg2) in data:
        correct.append(in_order(msg1, msg2))
    return correct


def in_order(l1, l2):
    """recursively checks if the ints/lists in the two list are in order
    returns true if l1 is "less than" l2; and false if l2 is "less than" l1
    will return None if the messages are the same (should only happen with sub lists"""
    for i in range(min(len(l1), len(l2))):
        left, right = l1[i], l2[i]
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                continue
            else:
                return left < right
        if not isinstance(left, list) and isinstance(right, list):
            left = [left]
        if isinstance(left, list) and not isinstance(right, list):
            right = [right]
        # left and right are both lists
        result = in_order(left, right)
        if result == None:
            continue
        else:
            return result
    # we have exausted the overlapping values without a determination
    # use the length to check
    if len(l1) == len(l2):
        return None
        # used to signal no determination; should not happen in msgs, but may happen in sub lists
        # if sublist match, then continue checking other values in the messages
    return len(l1) < len(l2)


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
