# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# instruction in a tuple (bool, int, int, int, int, int, int)
# representing (on/off, x_min, x_max, y_min, y_max, z_min, z_max)

# for part two, I will keep track of the segments in each dimension
# a segment is the distance between two given coordinate values.
# for example: given the following ranges for X: on -12..41, off -40..7, on -11..36, on -21..23
# I can create a sorted list of coordinates (-40, -21, -12, -11, 7, 23, 36, 41)
# creating 7 segments with the following sizes (19,9,1,18,16,13,5).  Each command will turn on/off
# one or more segments.
# the input file has 420 lines.  If we assume that there are no duplicates, then there will be 840 segments in
# each axis.  This will be 840*840*840 = 592,704,000 cells of varing size.  This reduces the size of the
# problem tremendously  (enough?);
# checking the input file, there is very little duplication of coords. 832, 830, 832 segments in the
# three axis.  this yields 574_545_920 cubes to track (1/2 billion is not a big number for the computer if
# I keep my code efficient). I will also only keep a list of the cubes that are on in a set with ints
# derived from the segment indexes
# if seg_x, seg_y, seg_z are the ordered lists of segments in each axis,
# the size of cube at segment 0,0,0 in (seg_x[1]-seg_x[0])*(seg_y[1]-seg_y[0])*(seg_z[1]-seg_z[0])
# Each cube from 0,0,0 to (nx,ny,nz) will be either on or off (all start off)
# they will be set to on/off by breaking each instruction up into segment parts and turning them on,
# in a similar manner to the sample puzzle (instead of +/- 50 we are +/- 420)
#
# PROBLEM: (in 1 dimension)
#   segment 10-10 is size 1  (10 - 10 + 1)
#   segment 10-13 is size 4,
#   10-11 is 2
#   10-11 + 12-13 is 4 (2 + 2)
#   but 10-11 + 11-12 should be 3 NOT 4 (because there is an overlap)
#
#   The answer to the total size depends on the overlaps.  In the one dimensional case,
#   I can erase 1 unit for each overlap. However the size of the overlap that needs to
#   be erased in the 3D problem depends on what is happening in the other dimensions
#
#   1 1 1 1
#   1 1 1 X 2 2
#   1 1 1 1 
#   1 1 1 x 3
#   1 1 1 x 3
#   The area #1 is 4x5 it overlaps with #2 (3x1) and #3 (2x2) with two overlaps for a total size of 3
#   Compared to
#   1 1 1 1
#   1 1 1 X 2 2
#   1 1 1 Z Y 2
#   1 1 1 x 3
#   1 1 1 x 3
#   #1 is still 4x5, but now #2 is 3x2 and 3 is 2x3, and #2 and #3 overlap at Y and Z (all 3 overlap at Z)

def part1(lines):
    instructions = parse(lines)
    on_set = build(instructions, -50, 50)
    return len(on_set)

def part2(lines):
    instructions = parse(lines)
    segments = ordered_coords(instructions)
    xs,ys,zs = segments
    print(segments)
    # print(len(xs)-1, len(ys)-1, len(zs)-1, (len(xs)-1)*(len(ys)-1)*(len(zs)-1))
    print(instructions)
    on_set = build2(instructions, segments)
    print(len(on_set))
    print(on_set)
    size = calc_size(on_set, segments)
    return size

def part2a(lines):
    instructions = parse(lines)
    print(len(instructions))
    instructions = cull(instructions)
    print(len(instructions))
    independent(instructions)
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

def build2(instructions, segments):
    xs, ys, zs = segments
    xl,yl,zl = len(xs), len(ys), len(zs)
    on_set = set()
    for cmd in instructions:
        state, x_min, x_max, y_min, y_max, z_min, z_max = cmd
        xi_min = xs.index(x_min)
        xi_max = xs.index(x_max) + 1 # we always want to include x_max
        yi_min = ys.index(y_min)
        yi_max = ys.index(y_max) + 1
        zi_min = zs.index(z_min)
        zi_max = zs.index(z_max) + 1
        # if x_min == x_max or y_min == y_max or z_min == z_max:
        #     print("akk, can't handle a unit cube")
        print(cmd)
        for xi in range(xi_min, xi_max):
            for yi in range(yi_min, yi_max):
                for zi in range(zi_min, zi_max):
                    # key = xi*yl*zl + (yi * zl) + zi
                    key = (xi,yi,zi)
                    print(xi, yi, zi, xl, yl, zl, key)
                    if state:
                        on_set.add(key)
                    else:
                        if key in on_set:
                            on_set.remove(key)
    return on_set

def calc_size(on_set, segments):
    size = 0
    xs, ys, zs = segments
    xl,yl,zl = len(xs), len(ys), len(zs)
    for xi,x1 in enumerate(xs[:-1]):
        x_size = xs[xi+1] - x1
        for yi,y1 in enumerate(ys[:-1]):
            y_size = ys[yi+1] - y1
            for zi,z1 in enumerate(zs[:-1]):
                # key = xi*yl*zl + yi * zl + zi
                key = (xi,yi,zi)
                if key in on_set:
                    z_size = zs[zi+1] - z1
                    size += x_size * y_size * z_size
    return size

if __name__ == '__main__':
    # lines = open("test2.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    # print(f"Part 1: {part1(lines)}")
    print(f"Part 2a: {part2a(lines)}")
