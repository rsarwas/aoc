# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# Each line is an integer or empty (just a newline)
# There is no empty line at the end


def part1(lines):
    totals = addup_calories(lines)
    return max(totals)


def part2(lines):
    totals = addup_calories(lines)
    totals.sort()
    top_three = totals[-3:]
    return sum(top_three)


def addup_calories(lines):
    totals = []
    total_elf = 0
    for line in lines:
        line = line.strip()
        if line:
            # add this amount to the current elf's total
            total_elf += int(line)
        else:
            totals.append(total_elf)
            total_elf = 0
    # there is no empty line at the end, so add the last elf
    totals.append(total_elf)
    return totals


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
