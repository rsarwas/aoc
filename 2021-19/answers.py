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

    # for s, sl in enumerate(data1):
    #     print("Scanner",s)
    #     for a,axis in enumerate(sl):
    #         print("   axis ",a,"F = ", axis)
    #         print("   axis ",a,"R = ", list(reversed(axis)))

    # for e in data2:
    #      (s1,a1,i1,l,s2,a2,d,i2,l) = e
    #      print(f"Match {l}! Sensor {s1}-{a1}[{i1}:{i1+l}] == Sensor {s2}-{a2}{d}[{i2}:{i2+l}]")

# Test1
# Match 11! Sensor 0-1[0:11] == Sensor 1-1F[13:24]
    # print("-----0,1,0,12")
    # beacon_coordinates(data, 0,1,0,"F",12)    
    # print("-----1,1,13,12")
    # beacon_coordinates(data, 1,1,13,"F",12)
# test2
#Match 11! Sensor 0-2[0:11] == Sensor 1-0R[14:25]
    # print("-----0,2,0,12")
    # beacon_coordinates(data, 0,2,0,"F",12)    
    # print("-----1,0R,14,12")
    # beacon_coordinates(data, 1,0,14,"R",12)
    # print("-----")

    xforms, offsets = transformations(data,data2)
    # print(xforms)
    # print(offsets)

    locations = set()
    for beacon in data[0]:
        locations.add(beacon)
    print(len(locations))
    for beacon in convert_to(data[1], 1, 0, xforms, offsets):
        locations.add(beacon)
    print(len(locations))
    # For test3 (two step transformation)
    tmp = convert_to(data[2], 2, 1, xforms, offsets)
    tmp2 = convert_to(tmp, 1, 0, xforms, offsets)
    # print(tmp2)
    for beacon in tmp2:
        locations.add(beacon)
    print(len(locations))

# Testing Sample:
#       The sample yields: 1->0, 3->1, 4->1, and 4->2
#       Tested: 1 -> 0 (test1); 4->1 (test2); 3->1->0 (test3) 
# TODO: 2) build multistep transformation (this is done manually for testing)
# TODO: 1) Test reverse transformations: create 2->4 from 4->2; then build 2->4->1->0
# TODO: 3) create the correct transformation n -> ... -> 0 for each sensor list



    # scanner_coords = { 0:(0,0,0) }
    # get_coords(scanner_coords, data, data2)
    # print(scanner_coords)
    # aliases = make_aliases(data, data2)
    #alias_count = count_aliases(aliases)
    #print(alias_count)
    #total -= alias_count
    return -1

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
        xforms = sensor_xforms[s1]
        offsets = sensor_offsets[s1]
        # xform matrices align axis in s2 to s1
        # s_in_s1 = s2 * matrix
        matrix = [[0,0,0],[0,0,0],[0,0,0]]
        xforms[s2] = matrix
        origin = [0,0,0]
        #align the primary axis 
        matrix[a2][a1] = 1 if d == "F" else -1
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
                
        new_c20 = transform(c2[0], matrix)
        offsets[s2] = subtract(c1[0], new_c20)
        # print("matrix", matrix)
        # print(c2[0]," ==> ", new_c20)
        # print(" c1[0] - new_c2: ", c1[0], " - ", new_c20," = ", offsets[s2])
        for i,c in enumerate(c2):
            o = add(transform(c, matrix), offsets[s2])
            # print(c, " => ", o, " == ", c1[i])
    return sensor_xforms, sensor_offsets

def transform(c,m):
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
        print("Panic! cannot xform", src," to ",dst)
        return
    xform = xforms[dst][src]
    offset = offsets[dst][src]
    new = []
    for c in coords:
        c2 = add(transform(c, xform), offset)
        # print(c, c2)
        new.append(c2)
    return new

# def get_coords(scanner_coords, sensors, matches):
#     aliases = {}
#     for e in matches:
#         (s1,a1,i1,l,s2,a2,d,i2,l) = e
#         _,c1 = beacon_coordinates(sensors, s1,a1,i1,"F",l) 
#         _,c2 = beacon_coordinates(sensors, s2,a2,i2,d,l)
#         if s1 in scanner_coords:
#             print(s1,s2, c1[0], c2[0])
#             x0,y0,z0 = scanner_coords[s1]
#             x1,y1,z1 = c1[0]
#             x2,y2,z2 = c2[0]
#             x3,y3,z3 = x0+x1-x2,y0+y1-y2,z0+z1-z2,
#             scanner_coords[s2]=(x3,y3,z3)

# def make_aliases(sensors, matches):
#     aliases = {}
#     for e in matches:
#         (s1,a1,i1,l,s2,a2,d,i2,l) = e
#         b1,_ = beacon_coordinates(sensors, s1,a1,i1,"F",l) 
#         b2,_ = beacon_coordinates(sensors, s2,a2,i2,d,l)
#         for (a,b) in zip(b1,b2):
#             key1 = (s1,a)
#             key2 = (s2,b)
#             keys = {key1, key2}
#             if key1 in aliases:
#                 keys = keys.union(aliases[key1])
#             if key2 in aliases:
#                 keys = keys.union(aliases[key2])
#             keys = list(keys)
#             for i, key1 in enumerate(keys[:-1]):
#                 for key2 in keys[i+1:]:
#                     if key1 not in aliases:
#                         aliases[key1] = set([key2]) # without the bracket tuple will get exploded
#                     else:
#                         aliases[key1].add(key2)
#                     if key2 not in aliases:
#                         aliases[key2] = set([key1]) # without the bracket tuple will get exploded
#                     else:
#                         aliases[key2].add(key1)

#     return aliases

# def count_aliases(aliases):
#     counts = {}
#     for k,v in aliases.items():
#         if len(v) == 2:
#             print(k," = ", v)
#     for v in aliases.values():
#         l = len(v)
#         if l in counts:
#             counts[l] += 1
#         else:
#             counts[l] = 1
#     total = 0
#     print(counts)
#     for n in counts:
#         total += (n * (counts[n] // (n + 1)))
#     return total

if __name__ == '__main__':
    lines = open("test3.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    # print(f"Part 2: {part2(lines)}")
