import sys


def what_floor(input):
    floor = 0
    for ch in input:
        if ch in "()":
            floor += 1 if ch == "(" else -1
    return floor


def when_basement(input):
    floor = 0
    position = 0
    for ch in input:
        if ch in "()":
            position += 1
            floor += 1 if ch == "(" else -1
        if floor == -1:
            return position
    return -1


if __name__ == "__main__":
    input = sys.stdin.read()
    print("Part 1: {0}".format(what_floor(input)))
    print("Part 2: {0}".format(when_basement(input)))
