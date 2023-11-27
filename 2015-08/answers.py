# Data Model:
# ===========


def part1(lines):
    total = 0
    for line in lines:
        line = line.strip()
        last_index = len(line) - 1
        index = 0
        mem_count = 0
        while index <= last_index:
            c = line[index]
            if c == '"' and (index == 0 or index == last_index):
                index += 1
            elif (
                c == "\\"
                and index < last_index
                and (line[index + 1] == '"' or line[index + 1] == "\\")
            ):
                index += 2
                mem_count += 1
            elif is_hex_code(line, index):
                index += 4
                mem_count += 1
            else:
                index += 1
                mem_count += 1
        # print(len(line), mem_count)
        total += len(line) - mem_count
    return total


def is_hex_code(line, index):
    hex = "0123456789abcdefABCDEF"
    if (
        line[index] == "\\"
        and index + 3 < len(line)
        and line[index + 1] == "x"
        and line[index + 2] in hex
        and line[index + 3] in hex
    ):
        return True
    return False


def part2(lines):
    total = 0
    for line in lines:
        line = line.strip()
        escape_char_count = 0
        for c in line:
            if c == "\\" or c == '"':
                escape_char_count += 1
        new_char_count = 2 + escape_char_count
        # print(len(line) + new_char_count, len(line))
        total += new_char_count
    return total


if __name__ == "__main__":
    # lines = open("test.txt").readlines()  # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
