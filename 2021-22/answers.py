# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# instruction in a tuple (bool, int, int, int, int, int, int)
# representing (on/off, x_min, x_max, y_min, y_max, z_min, z_max)

# for part two,
# the bounds are not limited to -50x50 = 100x100x100 = 1_000_000 points
# now there are ~200_000^3 points. 8*10^15 which is way too much to memory to manage
# Instead, I will keep track of the bounds of all instructions in each dimension
# the bounds are the min/max+1 values for a command.
# max+1 is used because each coordinate is the center of a unit cube, and we want the bounds
# of the cubes.  This is required to correctly calculate the size of each command and partial command.
# for example: given the following ranges for X: on -12..41, off -40..7, on 45..45
# the bounds will be [-12, 42, -40, 8, 45, 46] and the sorted bounds are:
# [-40, -12, 8, 42, 45, 46]
# this creates 7 segments.  (-40,-12), (-12,8), ... (45,46).  each segment has the size of x2-x1
# each command has one or more segments. each segment is entirely within or outside every command
# status of the segment is the status of the last command that contains the segment.
# if a segment is not in any command it is off.
# (-40,-12)=off, (-12,8)=off, (8,42)=on, (42,45)=un found (off), (45,46)=on.
# The total size is the size of all on/found segments (42-8) + (46-45) = 35
# this can be expanded to multiple dimensions.
# this reduces the memory requirement to 3 lists of ordered coordinates, and a single size totalizer.
# However, the input file has 420 lines.  If we assume that there are no duplicates,
# then there will be 840 segments in each axis.  so the complexity is 840^3 * 420/2 (the list of
# instructions must be searched for each segment, assume on average we go half way through the list.
# This is a lot of computations.  A sample problem with 60 instructions took about 15 seconds.
# 30*120^3 = 15s; 210*840^3 = Xs  => 36015sec (10hours!!!)
# I cleaned up the inner loop, and the sample now runs in about 5.7sec problem size is 48869730
# compared to 121527369600 for the actual puzzle.  estimated run time is now 14174 seconds (3.93 hours)

def part1_set(lines):
    instructions = parse(lines)
    on_set = build_set(instructions, -50, 50)
    return len(on_set)

def part1(lines):
    instructions = parse(lines)
    size = build(instructions, -50, 51)
    return size

def part2(lines):
    instructions = parse(lines)
    size = build(instructions)
    return size

def parse(lines):
    instructions = []
    for line in lines:
        state,coords = line.strip().split(" ")
        state = state == "on"
        x,y,z = coords.split(",")
        x1,x2 = x.replace("x=","").split("..")
        y1,y2 = y.replace("y=","").split("..")
        z1,z2 = z.replace("z=","").split("..")
        # Add one to the maximum, so the the difference is the size in that dimension
        instructions.append((state, int(x1), int(x2)+1, int(y1), int(y2)+1, int(z1), int(z2)+1))
    return instructions

def build_set(instructions, lower, upper):
    on_set = set()
    for cmd in instructions:
        state, x_min, x_max, y_min, y_max, z_min, z_max = cmd
        # For the set solution, the coords are center points, not bounds
        # subtract the 1 added to the maximum to created bounds from the center points
        x_max, y_max, z_max = x_max-1, y_max-1, z_max-1
        for x in range(max(x_min,lower),min(x_max,upper)+1):
            for y in range(max(y_min,lower),min(y_max,upper)+1):
                for z in range(max(z_min,lower),min(z_max,upper)+1):
                    if state:
                        on_set.add((x,y,z))
                    else:
                        if (x,y,z) in on_set:
                            on_set.remove((x,y,z))
    return on_set

def build(instructions, lower=None, upper=None):
    coords = ordered_coords(instructions)
    xs, ys, zs = clamp_coords(coords, lower, upper)
    reverse_cmds = list(reversed(instructions))
    # print("Problem_size = ", len(xs)*len(ys)*len(zs)*len(instructions)/2)
    total = 0
    for xi in range(len(xs)-1):
        x1, x2 = xs[xi], xs[xi+1]
        for yi in range(len(ys)-1):
            y1, y2 = ys[yi], ys[yi+1]
            for zi in range(len(zs)-1):
                z1, z2 = zs[zi], zs[zi+1]
                for cmd in reverse_cmds:
                    # each segment will be all in or all out of a cmd
                    # the last command will determine the status of the segment
                    # only add it to the total if it is on.
                    # if the last cmd containing the segment is off, then we can stop searching
                    if x1 >= cmd[1] and x2 <= cmd[2] and y1 >= cmd[3] and y2 <= cmd[4] and z1 >= cmd[5] and z2 <= cmd[6]:
                        if cmd[0]:
                            size = (x2-x1)*(y2-y1)*(z2-z1)
                            total += size
                        break
    return total

def ordered_coords(instructions):
    xs,ys,zs= (set(), set(), set())
    for cmd in instructions:
        _, x_min, x_max, y_min, y_max, z_min, z_max = cmd
        xs.add(x_min)
        xs.add(x_max)
        ys.add(y_min)
        ys.add(y_max)
        zs.add(z_min)
        zs.add(z_max)
    xs = list(xs)
    xs.sort()
    ys = list(ys)
    ys.sort()
    zs = list(zs)
    zs.sort()
    return xs, ys, zs

def clamp_coords(coords, lower=None, upper=None):
    if lower == None and upper == None:
        return coords
    new_coords = [[], [], []]
    for axis in [0, 1, 2]:
        for c in coords[axis]:
            if (lower is None or c >= lower) and (upper is None or c <= upper):
                new_coords[axis].append(c)
    return new_coords

def within(cmd1, cmd2):
    # return true is cmd1 is within cmd1, borders can touch
    # the state does not matter: if cmd1 is within, the state of cmd2
    # will govern the action when the cmds are processed
    # short circuit quit when False; fastest when expecting not within
    # cmd = (state, x_min, x_max, y_min, y_max, z_min, z_max)

    # compare mins
    for i in range(1, len(cmd1), 2):
        if cmd1[i] < cmd2[i]: return False
    # compare maxes
    for i in range(2, len(cmd1), 2):
        if cmd1[i] > cmd2[i]: return False
    return True

# The following are tests on the input to see if I can cull instructions
# because they are entirely within another command
# turns out there is very little opportunity here. 

def can_i_optimize(lines):
    instructions = parse(lines)
    print(len(instructions))
    instructions = cull(instructions)
    print(len(instructions))
    independent(instructions)
    return -1

def cull(instructions):
    new_instructions = []
    for i, cmd1 in enumerate(instructions[:-1]):
        skip = False
        for cmd2 in instructions[i+1:]:
            if within(cmd1, cmd2):
                print("skip", cmd1, "within", cmd2)
                skip = True
                break
        if not skip:
            new_instructions.append(cmd1)
    # we can't skip the last cmd
    new_instructions.append(instructions[-1]) 
    return new_instructions

def independent(instructions):
    total = len(instructions)
    for cmd1 in instructions:
        touch = total
        for cmd2 in instructions:
            if cmd1 == cmd2: continue
            if touches(cmd1, cmd2):
                touch -= 1
        print(cmd1, "touches", touch, "of", total)

def touches(cmd1, cmd2):
    # return true if cmd1 overlaps/touches cmd2. Ignore state.
    # short circuit quit when False; fastest when expecting not within
    # cmd = (state, x_min, x_max, y_min, y_max, z_min, z_max)

    # compare mins
    for i in range(1, len(cmd1), 2):
        c1_min = cmd1[i]
        c2_min = cmd2[i]
        c1_max = cmd1[i+1]
        c2_max = cmd2[i+1]
        if c2_min <= c1_max and c1_min <= c2_max :
            return True
    return False

if __name__ == '__main__':
    #lines = open("test.txt").readlines() # as a list of line strings
    #lines = open("test1.txt").readlines() # as a list of line strings
    #lines = open("test2.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    #print(f"Part 1: {part1_set(lines)}")
    print(f"Part 1: {part1(lines)}")

    # WARNING, Part 2 takes about 4 hours to compute
    #print(f"Part 2: {part2(lines)}")
    
    # print(f"Can I optimize the instructions: {can_i_optimize(lines)}")
