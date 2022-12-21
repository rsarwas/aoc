# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a random integer in range {-1e5 ,.., 1e5}; integers are NOT unique
# so we cannot search for the number that needs to move; we need to keep track of
# it's current location.
# Puzzle specifies that list is "circular", so moving a number off one end of the
# list wraps back around to the other end as if the ends were connected.
# it isn't clear what should happen if the move is so large that it passes the
# original location. i.e. does it step wise swap with it's neighbor n times, so
# number may move multiple spaces for each loop around the list, or is it a
# enough to figure the final resting place (distance mod list length), and then
# move each intervening number once.  The puzzle input is 5000 numbers, with many
# numbers greater than +/-5000, so this situation will occur many times.

def part1(lines):
    data = parse(lines)
    # data = mix(data)
    s = set(data)
    print(len(s) == len(data))
    result = gps_code(data)
    return result


def part2(lines):
     return -1


def parse(lines):
    data = [int(line) for line in lines]
    return data


def mix(data):
    oindexes = list(range(len(data)))
    nindexes = list(oindexes)
    # we keep a list of the 
    mixed = data[:]
    for e in data:
        if e > 0:
            # 0..i[e]-1 no change,
            # i[e]+1 = i[e] .. i[e]+e+1 = i[e]+3 (mod l)
            # i[e] = i[e]+e+1
            # i[e]+e+1.. end no change
            pass
        if e < 0:
            pass
        # else e == 0; do nothing
    return data

def gps_code(data):
    code = 0
    l = len(data)
    for i in [1000,2000,3000]:
        index = i % l
        code += data[index]
    return code


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
