# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# instruction in a tuple (bool, int, int, int, int, int, int)
# representing (on/off, x_min, x_max, y_min, y_max, z_min, z_max)

def part1(lines):
    instructions = parse(lines)
    on_set = build(instructions, -50, 50)
    return len(on_set)

def part2(lines):
    return -1

def parse(lines):
    instructions = []
    for line in lines:
        state,coords = line.strip().split(" ")
        state = state == "on"
        x,y,z = coords.split(",")
        x1,x2 = x.replace("x=","").split("..")
        y1,y2 = y.replace("y=","").split("..")
        z1,z2 = z.replace("z=","").split("..")
        instructions.append((state, int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)))
    return instructions

def build(instructions, lower, upper):
    on_set = set()
    for cmd in instructions:
        state, x_min, x_max, y_min, y_max, z_min, z_max = cmd
        for x in range(max(x_min,lower),min(x_max,upper)+1):
            for y in range(max(y_min,lower),min(y_max,upper)+1):
                for z in range(max(z_min,lower),min(z_max,upper)+1):
                    if state:
                        on_set.add((x,y,z))
                    else:
                        if (x,y,z) in on_set:
                            on_set.remove((x,y,z))
    return on_set

if __name__ == '__main__':
    lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
