# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
#


def part1(n):
    scores = [3, 7]
    c1 = 0
    c2 = 1
    while True:
        recipe = scores[c1] + scores[c2]
        if recipe > 9:
            scores.append(1)
            scores.append(recipe - 10)
        else:
            scores.append(recipe)
        c1 = (c1 + scores[c1] + 1) % len(scores)
        c2 = (c2 + scores[c2] + 1) % len(scores)
        # print(scores, c1, c2)
        if len(scores) > n + 10:
            return "".join([str(i) for i in scores[n : n + 10]])
    return -1


def part2(s):
    match_scores = [int(c) for c in s]
    start = 0
    scores = [3, 7]
    c1 = 0
    c2 = 1
    while True:
        recipe = scores[c1] + scores[c2]
        if recipe > 9:
            scores.append(1)
            scores.append(recipe - 10)
        else:
            scores.append(recipe)
        c1 = (c1 + scores[c1] + 1) % len(scores)
        c2 = (c2 + scores[c2] + 1) % len(scores)
        # print(scores, c1, c2)
        start, done = match(scores, start, match_scores, 0)
        if done:
            return start
    return -1


def match(haystack, start, needle, n):
    """Look for the list needle in the list haystack
    return True and the index in haystack where needle starts
    return false, and the best place to start the next search if not found
    * start is the best place to start searching (previous searches have not
      found it before this index.
    * n is the length of needle that has been found so far.

    This is a recursive search that increments start when there is no match
    and increments n when the first part of needle has been found"""

    if n >= len(needle):
        return start, True
    if start + n >= len(haystack):
        return start, False
    if haystack[start + n] == needle[n]:
        return match(haystack, start, needle, n + 1)
    else:
        return match(haystack, start + 1, needle, 0)


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    # print(f"Test 1a: {part1(5)} 5 => 0124515891")
    # print(f"Test 1b: {part1(9)} 9 => 5158916779")
    # print(f"Test 1c: {part1(18)} 18 => 9251071085")
    # print(f"Test 1d: {part1(2018)} 2018 => 5941429882")
    print(f"Part 1: {part1(598701)}")
    # print(f"Test 2a: {part2('01245')} == 5")
    # print(f"Test 2b: {part2('51589')} == 9")
    # print(f"Test 2c: {part2('92510')} == 18")
    # print(f"Test 2d: {part2('59414')} == 2018")
    print(f"Part 2: {part2('598701')}")
