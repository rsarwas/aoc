import sys

lines = []
for line in sys.stdin:
    lines.append(line)


def common_string(s1, s2):
    s = ""
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            s += s1[i]
    return s


winner = ""
for i in range(len(lines) - 1):
    for j in range(i + 1, len(lines)):
        common = common_string(lines[i], lines[j])
        if len(common) > len(winner):
            winner = common
print(winner)

""" Test Case = fgij
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""
