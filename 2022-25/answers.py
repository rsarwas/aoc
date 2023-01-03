"""A solution to an Advent of Code puzzle."""


def part1(lines):
    """Solve part 1 of the problem."""
    total = 0
    for line in lines:
        total += to_decimal(line.strip())
    return to_snafu(total)


SNAFU = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

DECIMAL = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def to_decimal(snafu):
    """Convert a snafu string to a decimal integer."""
    result = 0
    factor = 5 ** (len(snafu) - 1)
    for char in snafu:
        result += factor * SNAFU[char]
        factor //= 5
    return result


def to_snafu(decimal):
    """Convert a decimal integer to a snafu string."""
    quot = decimal // 5
    rem = decimal % 5
    digits = []
    while quot > 0 or rem > 2:
        if rem > 2:
            rem -= 5
            quot += 1
        digits.append(DECIMAL[rem])
        rem = quot % 5
        quot //= 5
    digits.append(DECIMAL[rem])
    digits.reverse()
    return "".join(digits)


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as data_file:
        data = data_file.readlines()
    print(f"Part 1: {part1(data)}")
