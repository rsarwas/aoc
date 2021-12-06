def part1(lines):
    fish = [int(n) for n in lines.split(",")]
    return brute_force(fish, 80)


def part2(lines):
    fish = [int(n) for n in lines.split(",")]
    return with_grouping(fish, 256)

def brute_force(fish, days):
    for _ in range(0, days):
        # print(fish)
        for i in range(0,len(fish)):
            if fish[i] == 0:
                fish.append(8)
                fish[i] = 6
            else:
                fish[i] -= 1
    return len(fish)

def with_grouping(fishes, days):
    # keep track of how many fish have a timer with a value of 0..8
    timers = {}
    # initialize the counts to 0
    for i in range(0,9):
        timers[i] = 0
    # count the existing fishes
    for fish in fishes:
        timers[fish] += 1
    # update the the timers once for each day 
    for _ in range(0, days):
        zeros = timers[0]
        for i in range(0,8):
            timers[i] = timers[i+1]
        timers[6] += zeros
        timers[8] = zeros
    total = sum(timers.values())
    return total

if __name__ == '__main__':
    # data = open("test.txt").read() # as one big string
    data = open("input.txt").read() # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
