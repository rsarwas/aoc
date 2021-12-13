# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

def part1(lines):
    moons = parse(lines)
    # print(moons)
    for i in range(0,1000):
        update(moons)
        # print(i, moons)
    energy = add_energy(moons)
    return energy

def part2(lines):
    return -1

def parse(lines):
    moons = []
    for line in lines:
        line = line.strip().replace("<x=","").replace(" y=","").replace(" z=","").replace(">","")
        x,y,z = line.split(",")
        moons.append([int(x),int(y),int(z),0,0,0])
    return moons

def update(moons):
    for axis in [0,1,2]:
        apply_gravity(moons,axis)
        update_location(moons,axis)

def apply_gravity(moons, axis):
    n = len(moons)
    for i in range(0,n-1):
        for j in range(i+1,n):
            if moons[i][axis] == moons[j][axis]:
                continue
            if moons[i][axis] < moons[j][axis]:
                moons[i][axis+3] += 1
                moons[j][axis+3] -= 1
            else:
                moons[i][axis+3] -= 1
                moons[j][axis+3] += 1

def update_location(moons, axis):
    for moon in moons:
        moon[axis] += moon[axis+3]

def add_energy(moons):
    total = 0
    for moon in moons:
        pe = abs(moon[0]) + abs(moon[1]) + abs(moon[2])
        ke = abs(moon[3]) + abs(moon[4]) + abs(moon[5])
        total += (pe*ke)
    return total


if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
