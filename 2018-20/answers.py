# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

import re

def part1(lines):
    code = lines[0][1:-2] # remove ^ at beginning and $\n at end
    # Simplify the input by removing all dead ends i.e. (...|)
    # assumes the dead ends are shorter than the options and that
    #  removing the dead ends does not create new dead ends i.e. (...|(...|))
    #  both these assumptions are true for my specific input file
    code1 = re.sub("\((E|W|N|S)*\|\)", "", code)
    # consider all the branches and find the longest branch
    length = find_longest_branch(code1)
    return length

def part2(lines):
    return -1

def find_longest_branch(str):
    return len(str)

def parse(s):
    # find first and last parens: s -> x(y)z
    b = s.find("(")
    e = s.rfind(")")
    if b == -1 and e == -1:  # no parens
        return len(s)
    if b*e < 0:  # one paren is missing
        raise Exception  # or return -1
    x = s[:b]
    y = s[b+1:e]
    z = s[e+1:]
    len_y = parse(y)
    len_xs = [len(s) for s in x.split("|")]
    len_zs = [len(s) for s in z.split("|")]
    # There are four options for how x,y, and z should be combined
    #  (E | .. | E | (...) | E | .. | E) => [a,..,b,0] + y + [0,c,..,d] => [a, .., b,y,c, .., d] find max
    #  (E | .. | E | (...) E | .. | E) => [a,..,b,0] + y + [c,..,d] => [a, .., b, y+c, .., d]
    #  (E | .. | E (...) | E | .. | E) => [a,..,b] + y + [0,c,..,d] => [a, .., b+y, c, .., d]
    #  (E | .. | E (...) E | .. | E) => [a,..,b] + y + [c,..,d] => [a, .., b+y+c, .., d]

    if len_xs[-1] == 0 and len_zs[0] == 0:
        return max(len_xs[:-1] + [len_y] + len_zs[1:])
    elif len_xs[-1] == 0 and len_zs[0] != 0:
        return max(len_xs[:-1] + [len_y + len_zs[0]] + len_zs[1:])
    elif len_xs[-1] != 0 and len_zs[0] == 0:
        return max(len_xs[:-1] + [ len_xs[-1] + len_y] + len_zs[1:])
    # else len_xs[-1] != 0 and len_zs[0] != 0:
    return max(len_xs[:-1] + [len_xs[-1] + len_y + len_zs[0]] + len_zs[1:])


if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    lines = open("test3.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


    """
    Development Notes

    ENWWW (NEEE|SSE(EE|N))
5 (NEEE|SSE(EE|N))
5 NEEE | SSE (EE|N)
5 + (4 or 3 + (1 or 2) )

5 4 (EE|N)
5 4 2 = 11

ESSWWN(E|NNENN(EESSSSS|WWWSSSSE(SW|NNNE)))
6 (E|NNENN(EESSSSS|WWWSSSSE(SW|NNNE)))
6 E|NNENN (EESSSSS|WWWSSSSE(SW|NNNE))
6 5 (EESSSSS|WWWSSSSE(SW|NNNE))
6 5 EESSSSS|WWWSSSSE (SW|NNNE)
6 5 8 (SW|NNNE)
6 5 8 SW|NNNE
6 5 8 4 = 23


parse(s):
find first and last parens: s -> x(y)z
b = s.find("(")
e = s.rfind(")")
if b == -1 and e == -1:  # no parens
    return len(s)
if b*e < 0  # one paren is missing
    raise exception or return -1
x = s[:b]
y = s[b+1:e]
z = s[e+1:]
len_y = parse(y)
len_xs = [len(s) for s in x.split("|")]
len_zs = [len(s) for s in z.split("|")]
# There are four options for how x,y, and z should be combined
(E | .. | E | (...) | E | .. | E) => [a,..,b,0] + y + [0,c,..,d] => [a, .., b,y,c, .., d] find max
(E | .. | E | (...) E | .. | E) => [a,..,b,0] + y + [c,..,d] => [a, .., b, y+c, .., d]
(E | .. | E (...) | E | .. | E) => [a,..,b] + y + [0,c,..,d] => [a, .., b+y, c, .., d]
(E | .. | E (...) E | .. | E) => [a,..,b] + y + [c,..,d] => [a, .., b+y+c, .., d]

if len_xs[-1] == 0 and len_zs[0] == 0:
    return max(len_xs[:-1] + [len_y] + len_zs[1:])
elif len_xs[-1] == 0 and len_zs[0] != 0:
    return max(len_xs[:-1] + [len_y + len_zs[0]] + len_zs[1:])
elif len_xs[-1] != 0 and len_zs[0] == 0:
    return max(len_xs[:-1] + [ len_xs[-1] + len_y] + len_zs[1:])
else: # len_xs[-1] != 0 and len_zs[0] != 0:
    return max(len_xs[:-1] + [len_xs[-1] + len_y + len_zs[0]] + len_zs[1:])

    """