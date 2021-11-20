import sys

def part1(lines):
    return sum([int(line) for line in lines])

def part2(lines):
    frequency = 0
    frequencies = set()
    while True:
        for line in lines:
            frequency += int(line)
            if frequency in frequencies:
                return frequency
            frequencies.add(frequency)

if __name__ == '__main__':
   lines = sys.stdin.read().split("\n")[:-1] # remove the last empty line
   print(f"Part 1: {part1(lines)}")
   print(f"Part 2: {part2(lines)}")
