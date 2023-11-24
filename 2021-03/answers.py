def part1(lines):
    ones = [0] * len(
        lines[0].strip()
    )  # index = bit location 0..., and value = count of 1s seen so far
    break_point = len(lines) // 2
    for line in lines:
        for i, c in enumerate(line.strip()):
            if c == "1":
                ones[i] += 1
    # gamma_rate = []; index = bit location 0..., and value = most common bit (0 or 1)
    gamma_rate = [1 if count > break_point else 0 for count in ones]
    # epsilon_rate = least common bit, or the inverse of the gamma_rate
    epsilon_rate = [0 if bit == 1 else 1 for bit in gamma_rate]
    # convert list to string then to int
    gamma_rate = int("".join(["1" if bit == 1 else "0" for bit in gamma_rate]), base=2)
    epsilon_rate = int(
        "".join(["1" if bit == 1 else "0" for bit in epsilon_rate]), base=2
    )
    power_consumption = gamma_rate * epsilon_rate
    return power_consumption


def common(lines, indexes, bit, kind):
    # lines is the list of all the numbers
    # indexes is the only ones to consider
    # bit is the index within the line to consider
    # returns the indexes of the satisfying lines
    ones = 0
    breakpoint = len(indexes) / 2
    for index in indexes:
        line = lines[index]
        c = line[bit]
        if c == "1":
            ones += 1
    keep = "0"
    if ones >= breakpoint:
        keep = "1"
    most_common = []
    least_common = []
    for index in indexes:
        if lines[index][bit] == keep:
            most_common.append(index)
        else:
            least_common.append(index)
    if kind == "most":
        return most_common
    else:
        return least_common


def part2(lines):
    bit_count = len(lines[0].strip())

    oxygen_generator_rating = 0
    indexes = list(range(0, len(lines)))
    for bit in range(0, bit_count):
        indexes = common(lines, indexes, bit, "most")
        if len(indexes) == 1:
            oxygen_generator_rating = int(lines[indexes[0]], base=2)
            break

    CO2_scrubber_rating = 0
    indexes = list(range(0, len(lines)))
    for bit in range(0, bit_count):
        indexes = common(lines, indexes, bit, "least")
        if len(indexes) == 1:
            CO2_scrubber_rating = int(lines[indexes[0]], base=2)
            break
    life_support_rating = oxygen_generator_rating * CO2_scrubber_rating
    return life_support_rating


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    lines = open("input.txt").readlines()  # as a list of line strings
    # lines = open("test.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
