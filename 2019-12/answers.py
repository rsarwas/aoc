# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# moons is a list of moons each moon is a 6 item list [x,y,z,vx,vy,vz]
# a list is used rather than a tuple to allow in place mutation.

import math  # for lcm


def part1(lines):
    moons = parse(lines)
    # print(moons)
    for i in range(0, 1000):
        update(moons)
        # print(i, moons)
    energy = add_energy(moons)
    return energy


def part2(lines):
    moons = parse(lines)
    # the three axis are independent
    x_start, x_len = find_cycle(moons, 0)
    print(x_start, x_len)
    y_start, y_len = find_cycle(moons, 1)
    print(y_start, y_len)
    z_start, z_len = find_cycle(moons, 2)
    print(z_start, z_len)
    # the problem statement does not state that initial state will be the first to repeat.
    # However it turns out that it is true for the test cases and my input.
    # Since each cycle starts at the same time, The LCM of the 3 cycle lengths is the answer.
    return math.lcm(x_len, y_len, z_len)


def parse(lines):
    moons = []
    for line in lines:
        line = (
            line.strip()
            .replace("<x=", "")
            .replace(" y=", "")
            .replace(" z=", "")
            .replace(">", "")
        )
        x, y, z = line.split(",")
        moons.append([int(x), int(y), int(z), 0, 0, 0])
    return moons


def update(moons):
    for axis in [0, 1, 2]:
        apply_gravity(moons, axis)
        update_location(moons, axis)


def apply_gravity(moons, axis):
    n = len(moons)
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            if moons[i][axis] == moons[j][axis]:
                continue
            if moons[i][axis] < moons[j][axis]:
                moons[i][axis + 3] += 1
                moons[j][axis + 3] -= 1
            else:
                moons[i][axis + 3] -= 1
                moons[j][axis + 3] += 1


def update_location(moons, axis):
    for moon in moons:
        moon[axis] += moon[axis + 3]


def add_energy(moons):
    total = 0
    for moon in moons:
        pe = abs(moon[0]) + abs(moon[1]) + abs(moon[2])
        ke = abs(moon[3]) + abs(moon[4]) + abs(moon[5])
        total += pe * ke
    return total


def find_cycle(moons, axis):
    previous_state = {}
    previous_state[get_state(moons, axis)] = 0
    for i in range(1, 1_000_000):
        apply_gravity(moons, axis)
        update_location(moons, axis)
        state = get_state(moons, axis)
        if state in previous_state:
            start = previous_state[state]
            return start, i - start
        else:
            previous_state[state] = i
    return -1, -1


def get_state(moons, axis):
    return (
        moons[0][axis],
        moons[1][axis],
        moons[2][axis],
        moons[3][axis],
        moons[0][axis + 3],
        moons[1][axis + 3],
        moons[2][axis + 3],
        moons[3][axis + 3],
    )


if __name__ == "__main__":
    lines = open("input.txt").readlines()  # as a list of line strings
    # lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("test2.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
