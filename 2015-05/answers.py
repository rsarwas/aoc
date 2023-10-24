# Data Model:
# ===========

def at_least_three_vowels(line):
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    for char in line:
        if char in vowels:
            vowel_count += 1
            if vowel_count == 3:
                return True
    return False

def at_least_one_letter_twice_in_a_row(line):
    for i in range(len(line)-1):
        if line[i] == line[i+1]:
            return True
    return False


def contain_special(line):
    for special in ["ab", "cd", "pq", "xy"]:
        if special in line:
            return True
    return False


def nice(line):
    return at_least_three_vowels(line) and \
    at_least_one_letter_twice_in_a_row(line) and \
    not contain_special(line)


def part1(lines):
    total = 0
    for line in lines:
        if nice(line):
            total += 1
    return total


def part2(lines):
    return len(lines)


if __name__ == '__main__':
    # print(f"test 1a: {nice('ugknbfddgicrmopn')} == True")
    # print(f"test 1b: {nice('aaa')} == True")
    # print(f"test 1c: {nice('jchzalrnumimnmhp')} == False")
    # print(f"test 1d: {nice('haegwjzuvuyypxyu')} == False")
    # print(f"test 1e: {nice('dvszwmarrgswjxmb')} == False")
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
