"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    for x, y in data:
        total += x * y
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = 0
    multiply = True
    for x, y in data:
        if x == 0:
            if y == 0:
                multiply = False
            else:
                multiply = True
        else:
            if multiply:
                total += x * y
    return total


def parse(lines):
    """Convert the lines of text into a useful data model.
    Add special number pairs to the output data to indicate additional
    instructions. (x,y) where x > 0 and y > 0 is a multiply instruction.
    (0,0) stop multiply instruction, (0,1) is a start multiply instruction.
    These additional instruction will not change the outcome of part 1"""
    data = []
    one_big_line = ""
    for line in lines:
        line = line.strip()
        one_big_line += line
    line = one_big_line
    index = 0
    while index < len(line) - 8:  # mul(x,y) to mul(xxx,yyy)
        if line[index : index + 4] == "do()":
            data.append((0, 1))
            index += 4
            continue
        if line[index : index + 7] == "don't()":
            index += 7
            data.append((0, 0))
            continue
        if line[index : index + 4] == "mul(":
            offset = index + 4
            number1, digits1 = get_number(line, offset)
            # print(offset, "number1", number1, digits1)
            if number1 is None:
                index = offset
            else:
                offset += digits1
                if line[offset] == ",":
                    offset += 1
                    number2, digits2 = get_number(line, offset)
                    # print(offset, "number2", number2, digits2)
                    if number2 is None:
                        index = offset
                    else:
                        offset += digits2
                        if offset < len(line) and line[offset] == ")":
                            data.append((number1, number2))
                            index = offset + 1
                        else:
                            index = offset
                else:
                    index = offset
        else:
            index += 1
    return data


def get_number(line, offset):
    """look for a 1 to 3 digit integer at offset in line.
    If found, return number as an integer, and the number of digits in the number
    otherwise return None, None."""
    # TODO: Check if index is out of bounds
    a = line[offset]
    b = line[offset + 1]
    c = line[offset + 2]
    if a in "123456789":
        if b in "1234567890":
            if c in "1234567890":
                return int(a + b + c), 3
            else:
                return int(a + b), 2
        else:
            return int(a), 1
    else:
        return None, None


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
