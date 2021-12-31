# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# scan_data is a list of scanner data for n scanners
# each scanner has a list of 3D coordinates (x,y,z) tuples for several beacons
# The frame of reference and orientation of each scanner is unknown
# Each scanner sees the same beacons, but in a different order, it may not see
# a beacon if it is more than 1000 units away along any axis.

def part1(lines):
    data = parse(lines)
    # print(data)
    data1 = organize(data)
    # print(data1)
    data2 = compare_deltas(data1)
    xforms, offsets = transformations(data,data2)
    # print("Xforms; ")
    # for k in sorted(xforms.keys()):
    #     print(f"  {k} -> {xforms[k]}")

    # TODO: build multistep transformation automatically 
    # The following routines are hard coded by looking at the transformation relationships
    # location_count = sample_locations(data, xforms, offsets)
    location_count = puzzle_locations(data, xforms, offsets)
    return location_count

def sample_locations(data, xforms, offsets):
    locations = set()
    # Add sonar 1
    for beacon in data[1]:
        locations.add(beacon)
    print("Sonar #1", len(data[1]))
    for l in sorted(data[1]):
        print("   ", l)

    # Add sonar 3 (3->1)
    locs = []
    for beacon in convert_to(data[3], 3, 1, xforms, offsets):
        locations.add(beacon)
        locs.append(beacon)
    print("Sonar #3 (as Sonar #1", len(locs))
    for l in sorted(locs):
        print("   ", l)

    # Add sonar 4 (4->1)
    locs = []
    for beacon in convert_to(data[4], 4, 1, xforms, offsets):
        locations.add(beacon)
        locs.append(beacon)
    print("Sonar #4 (as Sonar #1 ", len(locs))
    for l in sorted(locs):
        print("   ", l)

    # Add sonar 2 (2->4 (reverse)) ->1)
    locs = []
    tmp = convert_to(data[2], 2, 4, xforms, offsets)
    beacons = convert_to(tmp, 4, 1, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
        locs.append(beacon)
    print("Sonar #2 (as Sonar #1 ", len(locs))
    for l in sorted(locs):
        print("   ", l)

    # add Sonar #0 0 -> 1 (reverse)
    locs = []
    for beacon in convert_to(data[0], 0, 1, xforms, offsets):
        locations.add(beacon)
        locs.append(beacon)
    print("Sonar #0 (as Sonar #1 ", len(locs))
    for l in sorted(locs):
        print("   ", l)

    return len(locations)

def puzzle_locations(data, xforms, offsets):
    locations = set()
    # Add sonar 17
    for beacon in data[17]:
        locations.add(beacon)
    # Add sonar 7 (7->17)
    for beacon in convert_to(data[7], 7, 17, xforms, offsets):
        locations.add(beacon)
    # Add sonar 9 (9->17)
    for beacon in convert_to(data[9], 9, 17, xforms, offsets):
        locations.add(beacon)
    # Add sonar 14 (14->17)
    for beacon in convert_to(data[14], 14, 17, xforms, offsets):
        locations.add(beacon)
    # Add sonar 15 (15->17)
    for beacon in convert_to(data[15], 15, 17, xforms, offsets):
        locations.add(beacon)
    # Add sonar 25 (25->17)
    for beacon in convert_to(data[25], 25, 17, xforms, offsets):
        locations.add(beacon)
    # Add sonar 0 (0->7->17)
    tmp = convert_to(data[0], 0, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 2 (2->7->17)
    tmp = convert_to(data[2], 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 21 (21->9->17)
    tmp = convert_to(data[21], 21, 9, xforms, offsets)
    beacons = convert_to(tmp, 9, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 11 (11->14->17)
    tmp = convert_to(data[11], 11, 14, xforms, offsets)
    beacons = convert_to(tmp, 14, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 12 (12->15->17)
    tmp = convert_to(data[12], 12, 15, xforms, offsets)
    beacons = convert_to(tmp, 15, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 4 (4->25->17)
    tmp = convert_to(data[4], 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 1 (1->2->7->17)
    tmp = convert_to(data[1], 1, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 16 (16->2->7->17)
    tmp = convert_to(data[16], 16, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 18 (18->4->25->17)
    tmp = convert_to(data[18], 18, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 19 (19->4->25->17)
    tmp = convert_to(data[19], 19, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 5 (5->21->9->17)
    tmp = convert_to(data[5], 5, 21, xforms, offsets)
    tmp = convert_to(tmp, 21, 9, xforms, offsets)
    beacons = convert_to(tmp, 9, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 23 (23->21->9->17)
    tmp = convert_to(data[23], 23, 21, xforms, offsets)
    tmp = convert_to(tmp, 21, 9, xforms, offsets)
    beacons = convert_to(tmp, 9, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 8 (8->1->2->7->17)
    tmp = convert_to(data[8], 8, 1, xforms, offsets)
    tmp = convert_to(tmp, 1, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 22 (22->1->2->7->17)
    tmp = convert_to(data[22], 22, 1, xforms, offsets)
    tmp = convert_to(tmp, 1, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 20 (20->16->2->7->17)
    tmp = convert_to(data[20], 20, 16, xforms, offsets)
    tmp = convert_to(tmp, 16, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 6 (6->18->4->25->17)
    tmp = convert_to(data[6], 6, 18, xforms, offsets)
    tmp = convert_to(tmp, 18, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 10 (10->6->18->4->25->17)
    tmp = convert_to(data[10], 10, 6, xforms, offsets)
    tmp = convert_to(tmp, 6, 18, xforms, offsets)
    tmp = convert_to(tmp, 18, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 13 (13->6->18->4->25->17)
    tmp = convert_to(data[13], 13, 6, xforms, offsets)
    tmp = convert_to(tmp, 6, 18, xforms, offsets)
    tmp = convert_to(tmp, 18, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 24 (24->6->18->4->25->17)
    tmp = convert_to(data[24], 24, 6, xforms, offsets)
    tmp = convert_to(tmp, 6, 18, xforms, offsets)
    tmp = convert_to(tmp, 18, 4, xforms, offsets)
    tmp = convert_to(tmp, 4, 25, xforms, offsets)
    beacons = convert_to(tmp, 25, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    # Add sonar 3 (3->8->1->2->7->17)
    tmp = convert_to(data[3], 3, 8, xforms, offsets)
    tmp = convert_to(tmp, 8, 1, xforms, offsets)
    tmp = convert_to(tmp, 1, 2, xforms, offsets)
    tmp = convert_to(tmp, 2, 7, xforms, offsets)
    beacons = convert_to(tmp, 7, 17, xforms, offsets)
    for beacon in beacons:
        locations.add(beacon)
    return len(locations)

def part2(lines):
    return -1

def parse(lines):
    scan_data = []
    data = None
    for line in lines:
        if line.startswith("---"):
            data = []
            scan_data.append(data)
            continue
        else:
            if "," not in line:
                # skip lines without a comma
                continue
            x,y,z = [int(n) for n in line.split(",")]
            data.append((x,y,z))
    return scan_data

def organize(data):
    # ordered is a list (one item for each scanner).
    # each item is a list with 3 lists one for each axis
    # each axis list is the distance between adjacent beacons along that axis.
    ordered = []
    for scanner in data:
        order = []
        for axis in [0,1,2]:
            cs = [b[axis] for b in scanner]
            cs.sort()
            deltas = []
            previous = cs[0]
            for this in cs[1:]:
                deltas.append(this - previous)
                previous = this
            order.append(deltas)
        ordered.append(order)
    return ordered

def compare_deltas(order_data):
    overlap = []
    for s1, scanner1 in enumerate(order_data[:-1]):
        for s2, scanner2 in enumerate(order_data):
            if s2 <= s1: continue
            for a1, axis1 in enumerate(scanner1):
                for a2, axis2 in enumerate(scanner2):
                    matches = deltas_match(axis1,axis2)
                    if matches:
                        l,i1,i2 = matches
                        # print(f"Match {l}! Sensor {s1}-{a1}[{i1}:{i1+l}] == Sensor {s2}-{a2}[{i2}:{i2+l}]")
                        overlap.append((s1,a1,i1,l,s2,a2,"F",i2,l))
                    # try reversing the axis
                    axis2r = list(reversed(axis2))
                    matches = deltas_match(axis1,axis2r)
                    if matches:
                        l,i1,i2 = matches
                        # print(f"Match {l}! Sensor {s1}-{a1}[{i1}:{i1+l}] == Sensor {s2}-{a2}rev[{i2}:{i2+l}]")
                        overlap.append((s1,a1,i1,l,s2,a2,"R",i2,l))
    return overlap

def deltas_match(l1,l2):
    # l1 and l2 are lists of deltas (distances between beacons).
    # The lists may not have the same length or starting points
    # [3,4,2,7,1,3] and [3,9,8,3,4,2] overlap at l1[0:3] and l2[2:]
    # They also overlap at l1[-1:] and l2[0:1], but not at l1[0:1] or l2[0:1]
    # one list must include the first element of one list must match
    # an element in the other list, and the last element in one list
    # must match an element in the other list (first and last can be
    # in the same list). and all element in between must match
    # returns the length of the longest match and the starting point in l1
    # or None if there is no match.

    def match_length(l1,l2):
        # l1 and l2 are list slices that have a matching first element
        # return length of the matching elements as long as it
        # exhausts one of the slices
        c = 0
        for (a,b) in zip(l1,l2):
            if a != b: return None
            c += 1
        return c

    matches = []
    for i1 in range(len(l1)):
        if l1[i1] == l2[0]:
            length = match_length(l1[i1:],l2[0:])
            if length is not None and length > 10:
                # Per spec, A match must be at least 12 beacons (11 deltas)
                matches.append((length, i1, 0))
    for i2 in range(1,len(l2)):
        if l1[0] == l2[i2]:
            length = match_length(l1[0:],l2[i2:])
            if length is not None and length > 10:
                # Per spec, A match must be at least 12 beacons (11 deltas)
                matches.append((length, 0, i2))
    best = None
    for match in matches:
        if best is None or match[0] > best[0]:
            best = match
    return best

def beacon_coordinates(data, sensor_id,axis_id,index,direction,length):
    # print the index # and coords for the beacons that match the parameters
    # the beacons are those with the sorted coordinates in the axis
    beacons= []
    sensor_coords = []
    sensor = data[sensor_id]
    beacon_coords = {b[axis_id]: i for (i,b) in enumerate(sensor)}
    coords = [b[axis_id] for b in sensor]
    coords.sort()
    if direction == "R":
        coords.reverse()
    for coord in coords[index:index+length]:
        b = beacon_coords[coord]
        # print("  beacon ", b," at ", sensor[b])
        beacons.append(b)
        sensor_coords.append(sensor[b])
    return beacons, sensor_coords


def transformations(sensors,matches):
    # returns {sensor: {other_sensor1:xform_matrix, other_sensor2:xform_matrix, ...}, ...}
    sensor_xforms = {}
    sensor_offsets = {}
    for s in range(len(sensors)):
        sensor_xforms[s] = {}
        sensor_offsets[s] = {}
    for e in matches:
        (s1,a1,i1,l,s2,a2,d,i2,l) = e
        _,c1 = beacon_coordinates(sensors, s1,a1,i1,"F",l) 
        _,c2 = beacon_coordinates(sensors, s2,a2,i2,d,l)
        # forward
        x,o = align(a1,c1,a2,c2, d=="F")
        sensor_xforms[s1][s2] = x
        sensor_offsets[s1][s2] = o
        # reverse
        x,o = align(a2,c2,a1,c1, d=="F")
        sensor_xforms[s2][s1] = x
        sensor_offsets[s2][s1] = o
    return sensor_xforms, sensor_offsets

def align(a1,c1,a2,c2, same_dir):
    # xform matrices align axis in s2 to s1
    # s_in_s1 = s2 * matrix
    matrix = [[0,0,0],[0,0,0],[0,0,0]]
    #align the primary axis 
    matrix[a2][a1] = 1 if same_dir else -1
    # To align the axis, find the scale and direction
    # between the first two matching beacons
    # this seems risky, since the delta for different axis may be the same;
    #   however, maybe in this case, it doesn't matter if we mismatch.
    s1_scale = [0,0,0]
    s2_scale = [0,0,0]
    a1_rem = [0,1,2]
    a1_rem.remove(a1)
    a2_rem = [0,1,2]
    a2_rem.remove(a2)
    for axis in a1_rem:
        s1_scale[axis] = c1[1][axis] - c1[0][axis]
    for axis in a2_rem:
        s2_scale[axis] = c2[1][axis] - c2[0][axis]
    for axis1 in a1_rem:
        for axis2 in a2_rem:
            if s1_scale[axis1] == s2_scale[axis2]:
                matrix[axis2][axis1] = 1
            if s1_scale[axis1] == -s2_scale[axis2]:
                matrix[axis2][axis1] = -1
    new_c20 = multiply(c2[0], matrix)
    offsets = subtract(c1[0], new_c20)
    # print("matrix", matrix)
    # print(c2[0]," ==> ", new_c20)
    # print(" c1[0] - new_c2: ", c1[0], " - ", new_c20," = ", offsets[s2])
    # for i,c in enumerate(c2):
        # o = add(multiply(c, matrix), offsets[s2])
        # print(c, " => ", o, " == ", c1[i])
    return matrix, offsets

def multiply(c,m):
    new_c = [0,0,0]
    for i in range(3):
        for j in range(3):
            new_c[i] += (c[j] * m[j][i])
    return (new_c[0], new_c[1], new_c[2])

def subtract(v1,v2):
    # v1 - v2
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])
    
def add(v1,v2):
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

def convert_to(coords, src, dst, xforms, offsets):
    if src not in xforms[dst]:
        print("Panic! No xform between", src," and ",dst)
        return None
    xform = xforms[dst][src]
    offset = offsets[dst][src]
    new = []
    for c in coords:
        c2 = add(multiply(c, xform), offset)
        # print(c, c2)
        new.append(c2)
    return new

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    # print(f"Part 2: {part2(lines)}")
