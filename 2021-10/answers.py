# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

def part1(lines):
    illegals = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    total = 0
    for line in lines:
        illegal = syntax_check(line.strip())
        if illegal is not None:
            total += illegals[illegal]
    return total

def part2(lines):
    scores = []
    for line in lines:
        ending = complete(line.strip())
        if ending is None:
            continue
        scores.append(score(ending))
    scores.sort()
    mid = len(scores) // 2
    return scores[mid]

CLOSERS = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}

OPENERS = set(['(','[','{','<'])

def syntax_check(line):
    stack = []
    for c in line:
        if c in OPENERS:
            stack.append(c)
        else:
            last = stack.pop()
            if CLOSERS[last] != c:
                 return c
    return None

def complete(line):
    stack = []
    for c in line:
        if c in OPENERS:
            stack.append(c)
        else:
            last = stack.pop()
            if CLOSERS[last] != c:
                 return None
    finishers = []
    while len(stack) > 0:
        last = stack.pop()
        finishers.append(CLOSERS[last])
    return finishers

POINTS = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
}

def score(ending):
    total = 0
    for c in ending:
        total *= 5
        total += POINTS[c]
    return total

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
