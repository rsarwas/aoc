"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    initial_secrets = parse(lines)
    total = 0
    for secret in initial_secrets:
        # print(secret)
        for _ in range(2000):
            secret = next_secrets(secret)
        # print(secret)
        total += secret
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    initial_secrets = parse(lines)
    sequences = []
    for secret in initial_secrets:
        secrets = [secret]
        for _ in range(2000):
            secret = next_secrets(secret)
            secrets.append(secret)
        values = sequence_value(secrets)
        sequences.append(values)
    # search all sequences for the best sequence
    sequence, total_value = find_best_sequence(sequences)
    # print(sequence)
    return total_value


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return [int(line) for line in lines]


def next_secrets(secret):
    """Apply the formula in the puzzle to create a new secret"""
    secret ^= 64 * secret
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= 2048 * secret
    secret %= 16777216
    return secret


def sequence_value(secrets):
    """Return a dictionary of first values for all sequences in this list of secrets"""
    values = {}
    price = [x % 10 for x in secrets]
    changes = [None]
    for i in range(len(secrets) - 1):
        change = price[i + 1] - price[i]
        changes.append(change)
    for i in range(4, len(secrets)):
        sequence = (changes[i - 3], changes[i - 2], changes[i - 1], changes[i])
        if sequence not in values:
            values[sequence] = price[i]
    return values


def find_best_sequence(sequences):
    """Search all the sequences and return the sequence and total value of that sequence"""
    max_total = 0
    max_sequence = None
    checked = set()
    for values in sequences:
        for sequence, value in values.items():
            if sequence in checked:
                continue
            value = total_value(sequence, sequences)
            if value > max_total:
                max_total = value
                max_sequence = sequence
            checked.add(sequence)
    return max_sequence, max_total


def total_value(sequence, sequences):
    """Return the total value of sequence in all the buyers sequences"""
    total = 0
    for values in sequences:
        if sequence in values:
            total += values[sequence]
    return total


def test():
    secret = 123
    for _ in range(10):
        secret = next_secrets(secret)
        print(secret)


def test2():
    secret = 123
    secrets = [secret]
    for _ in range(10 - 1):
        secret = next_secrets(secret)
        secrets.append(secret)
    print(secrets)
    values = sequence_value(secrets)
    print(values)


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
    # test2()
