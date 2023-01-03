# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line is a random integer in range {-1e5 ,.., 1e5}; integers are NOT unique
# so we cannot search for the number that needs to move; we need to keep track of
# it's current location.  Therefore the following simple brute force solution will
# not work: find n, then swap it n times with the element after (or before for negative n)
# Puzzle specifies that list is "circular", so moving a number off one end of the
# list wraps back around to the other end as if the ends were connected.
# it isn't clear what should happen if the move is so large that it passes the
# original location. i.e. does it step wise swap with it's neighbor n times, so
# number may move multiple spaces for each loop around the list, or is it a
# enough to figure the final resting place (distance mod list length), and then
# move each intervening number once.  The puzzle input is 5000 numbers, with many
# numbers greater than +/-5000, so this situation will occur many times.

def test_uniqueness(lines):
    data = parse(lines)
    print("Values are unique:", len(set(data)) == len(data))


def part1(lines):
    data = parse(lines)
    print("Initial arrangement:")
    print(data)
    data = mix(data)
    # uniqueness test
    # print("Values are unique:", len(set(data)) == len(data))
    result = gps_code(data, 0)
    return result


def part2(lines):
     return -1


def parse(lines):
    data = [int(line) for line in lines]
    return data


def mix(data):
    # just keep track of the indexes of the numbers in data
    # original indexes 0..len(data)
    indexes = list(range(len(data))) # starts the same as the original indexes
    new_data = list(data) # will be updated at the end with the reorganized list
    for i, e in enumerate(data):
        # in example, the interveening numbers move up or down tword the hole left
        # by the moving number.  regardless of pos or neg or wrap around
        # if the end is between the first and last element, it goes on the end, and
        # elements move down the list, example: if -1 is at index 1 (second item), it will
        # move down 1 to be between first item and last item, so it will go to the end.
        if e == 0:
            print("\n0 does not move:")
            print(new_data)
            continue
        index = indexes[i]
        # in python % n returns a number between 0 and n-1 even if the number is
        # negative, so this works in both directions.
        end = (index + e) % len(data)

        if end == 0:
            end = len(data) - 1
        start = index + 1
        delta = 1
        if end < index:
            delta = -1
        else:
            if e < 0: end -= 1
        iset = set(range(start, end + 1, delta))

        # debugging printout
        if delta == -1:
            print(f"\n{e} moves between {data[indexes[end+1]]} and {data[indexes[end]]}")
        else:
            print(f"\n{e} moves between {data[indexes[end]]} and {data[indexes[end + 1]]}")
        print("i, e, index, shift from start to end by delta")
        print(i, e, "at", index, "shift from", start, "to", end+1, "by", delta)
        print("indexes", indexes)
        print(iset)


        for ii,iii in enumerate(indexes):
            if iii in iset:
                indexes[ii] -= delta
        indexes[i] = end


        # for debugging, print the reorganized list
        print("indexes", indexes)
        for i,ii in enumerate(indexes):
            new_data[ii] = data[i]
        print(new_data)

    for i,ii in enumerate(indexes):
        new_data[ii] = data[i]
    return new_data

def test_indexing(data):
    # data = [1, 2, -1, -3, 0, 1, 4]
    #data = [1, 2, -1, -3, -7, 1, 4]
    print(data)
    for index in range(len(data)):
        e = data[index]
        left = (index + e) % len(data)
        if e < 0:
            left -=1
        right = left + 1
        right %= len(data)

        new_data = list(data)
        for i in range(index + 1, left+1):
            new_data[i-1] = data[i]
        new_data[left] = e

        print(f"{e} moves between {data[left]} and {data[right]} => {new_data}")


def gps_code(data, val):
    code = 0
    l = len(data)
    loc = data.index(val)
    for i in [1000,2000,3000]:
        index = (loc + i) % l
        code += data[index]
    return code


if __name__ == '__main__':
    # lines = open("test.txt").readlines()
    # test_uniqueness(lines)
    test_indexing([1, 2, 3, 1, 7])
    # [1, 2, 3, 1, 7]
    # 1 moves between 2 and 3 => [2, 1, 3, 1, 7]
    # 2 moves between 1 and 7 => [1, 3, 1, 2, 7]
    # 3 moves between 1 and 2 => [3, 2, 3, 1, 7]  # WRONG (description right); expecting [1, 3, 2, 1, 7]
    # 1 moves between 7 and 1 => [1, 2, 3, 7, 1]
    # 7 moves between 2 and 3 => [1, 7, 3, 1, 7]  # WRONG (description right); expecting [1, 2, 7, 3, 1]
    test_indexing([-7, -1, -3, -2, -1])
    # [-7, -1, -3, -2, -1]
    # -7 moves between -3 and -2 => [-1, -3, -7, -2, -1]
    # -1 moves between -1 and -7 => [-7, -1, -3, -2, -1]  # WRONG (description right); expecting [-7,-3, -2, -1, -1]
    # -3 moves between -2 and -1 => [-7, -1, -2, -3, -1]
    # -2 moves between -7 and -1 => [-2, -1, -3, -2, -1]  # WRONG (description right); expecting [-7, -2, -1, -3, -1]
    # -1 moves between -3 and -2 => [-7, -1, -1, -2, -1]  # WRONG (description right); expecting [-7, -1, -3, -1, -2]

    # print(f"Part 1: {part1(lines)}")
    # print(f"Part 2: {part2(lines)}")
