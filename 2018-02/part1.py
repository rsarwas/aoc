import collections
import sys

def has_n(counts, n):
    for c in counts:
        if c[1] == n: return True
        if c[1] < n: return False
    return False

doubles = 0
triples = 0
for line in sys.stdin:
    counts = collections.Counter(line).most_common()
    if has_n(counts, 2):
        doubles += 1
    if has_n(counts, 3):
        triples += 1

print("Part1: ", doubles * triples)

""" Test Case = 12
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""