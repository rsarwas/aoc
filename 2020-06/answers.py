from functools import reduce
import sys

data = sys.stdin.read()[:-1]  # remove the trailing newline
groups = [group.split("\n") for group in data.split("\n\n")]
char_sets = [[set(line) for line in group] for group in groups]
# char_sets is a list of groups; a group is a list of responses; a response is a set of yes answers (chars a-z)
yeses = [len(reduce(lambda a, b: a.union(b), sets, set())) for sets in char_sets]
allchars = set("abcdefghijklmnopqrstuvwxyz")
allyes = [
    len(reduce(lambda a, b: a.intersection(b), sets, allchars)) for sets in char_sets
]
print(f"Part 1: {reduce(lambda a,b: a+b, yeses)}")
print(f"Part 2: {reduce(lambda a,b: a+b, allyes)}")
