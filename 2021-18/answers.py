# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a snail number
# a snail number is a pair ([x,y]) where x and y are either a regular number 0..9,
# or a snail number.  for example: [[1,2],3]

import ast  # to parse string representation of a list as a list


def part1(lines):
    snail_numbers = parse(lines)
    n1 = snail_numbers[0]
    for n2 in snail_numbers[1:]:
        n1 = add(n1, n2)
    # print(n1)
    m = magnitude(n1)
    return m


def part2(lines):
    snail_numbers = parse(lines)
    best = 0
    for n1 in snail_numbers:
        for n2 in snail_numbers:
            m = magnitude(add(n1, n2))
            if m > best:
                best = m
    return best


def parse(lines):
    return [ast.literal_eval(line) for line in lines]


def magnitude(n):
    left, right = n
    if not isinstance(left, int):  # a nested pair (not a regular number)
        left = magnitude(left)
    if not isinstance(right, int):
        right = magnitude(right)
    return 3 * left + 2 * right


def add(n1, n2):
    """Add two snail numbers and return the new reduced snail number"""
    # added = "[" + n1 + ", " + n2 + "]"
    added = [n1, n2]
    return reduce(added)


def reduce(n):
    """Reduce a snail number"""
    while True:
        n1 = explode(n)
        if n1 is None:
            n2 = split(n)
            if n2 is None:
                return n
            else:
                n = n2
        else:
            n = n1


def explode(n):
    """
    Explode a snail number

    If the number cannot explode return None, otherwise
    return the new number after applying the first available explosion.
    If any pair is nested inside depth pairs, the leftmost such pair explodes.

    To explode a pair, the pair's left value is added to the first regular number
    to the left of the exploding pair (if any), and the pair's right value is added
    to the first regular number to the right of the exploding pair (if any).
    Exploding pairs will always consist of two regular numbers. Then, the entire
    exploding pair is replaced with the regular number 0.
    [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]
    [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]
    [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3]
    [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]]
    """
    if isinstance(n, int):
        return None

    left, right = n
    exl = explode_to(left, 4)
    if exl is not None:
        _, mid, post = exl
        # ignore the pre, there is no regular number to the left of this
        return [mid, add_left(right, post)]
    # we didn't explode the left side, so try the right
    exr = explode_to(right, 4)
    if exr is not None:
        pre, mid, post = exr
        # ignore the post, there is no regular number to the right of this
        return [add_right(left, pre), mid]
    return None


def explode_to(n, depth):
    if depth < 1:
        return None
    if depth == 1:
        if isinstance(n, int):
            return None
        left, right = n
        if not isinstance(left, int) or not isinstance(right, int):
            print("Aak!, n exceeds expected", n, depth)
            return None
        return (left, 0, right)
    else:
        if isinstance(n, int):
            return None
        left, right = n
        exl = explode_to(left, depth - 1)
        if exl is not None:
            pre, mid, post = exl
            return (pre, [mid, add_left(right, post)], 0)
        # we didn't explode the left side, so try the right
        exr = explode_to(right, depth - 1)
        if exr is not None:
            pre, mid, post = exr
            return (0, [add_right(left, pre), mid], post)
    return None


def add_left(sn, rn):
    if isinstance(sn, int):
        return sn + rn
    left, right = sn
    return [add_left(left, rn), right]


def add_right(sn, rn):
    if isinstance(sn, int):
        return sn + rn
    left, right = sn
    return [left, add_right(right, rn)]


def split(n):
    """
    Split a snail number
    if the number cannot split return None, otherwise
    return the new number after applying only first available split.

    If any regular number is 10 or greater, the leftmost such regular number splits.

    To split a regular number, replace it with a pair; the left element of
    the pair should be the regular number divided by two and rounded down,
    while the right element of the pair should be the regular number divided
    by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6],
    12 becomes [6,6], and so on.
    """
    if isinstance(n, int):
        if n > 9:
            left = n // 2
            right = n - left
            return [left, right]
        return None

    left, right = n
    # check left side first
    new_left = split(left)
    if new_left is not None:
        return [new_left, right]
    # check right side (only if we did not split the left side)
    new_right = split(right)
    if new_right is not None:
        return [left, new_right]

    return None


if __name__ == "__main__":
    # Tests
    # print(add(4,5))
    # print(add(add(4,5), add(3, add(7,5))))
    # print(add(add(4,15), add(3, add(17,5))))
    # print(magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]))
    # print(magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]))
    # print(magnitude([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]))
    # print(ast.literal_eval("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]\n"))
    # print(explode([[[[[9,8],1],2],3],4])) # == [[[[0,9],2],3],4])
    # print(explode([7,[6,[5,[4,[3,2]]]]])) # == [7,[6,[5,[7,0]]]])
    # print(explode([[6,[5,[4,[3,2]]]],1])) # == [[6,[5,[7,0]]],3])
    # print(explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])) # == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    # print(explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])) # == [[3,[2,[8,0]]],[9,[5,[7,0]]]])

    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
