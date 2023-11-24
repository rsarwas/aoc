import sys


def man_dist(a, b):
    return abs(a) + abs(b)


def intersection(l1, l2):
    l1x1 = min(l1[0][0], l1[1][0])
    l1x2 = max(l1[0][0], l1[1][0])
    l1y1 = min(l1[0][1], l1[1][1])
    l1y2 = max(l1[0][1], l1[1][1])
    l2x1 = min(l2[0][0], l2[1][0])
    l2x2 = max(l2[0][0], l2[1][0])
    l2y1 = min(l2[0][1], l2[1][1])
    l2y2 = max(l2[0][1], l2[1][1])
    dx1 = l1x2 - l1x1
    dy1 = l1y2 - l1y1
    dx2 = l2x2 - l2x1
    dy2 = l2y2 - l2y1
    # print((l1x1,l1y1),(l1x2,l1y2),dx1,dy1)
    # print((l2x1,l2y1),(l2x2,l2y2),dx2,dy2)

    # co-linear vertical lines (return point in overlap closest to (0,0))
    if dx1 == 0 and dx2 == 0 and l1x1 == l2x1:
        # print("co-linear vertical lines")
        if l1y1 < l2y1:
            if l2y1 <= l1y2:
                return (l1x1, l2y1)
        else:
            if l1y1 <= l2y2:
                return (l1x1, l1y1)

    # co-linear horizontal lines (return point in overlap closest to (0,0))
    if dy1 == 0 and dy2 == 0 and l1y1 == l2y1:
        # print("co-linear horizontal lines")
        if l1x1 < l2x1:
            if l2x1 <= l1x2:
                return (l2x1, l1y1)
        else:
            if l1x1 <= l2x2:
                return (l1x1, l1y1)

    # line1 horizontal and line2 vertical
    if dy1 == 0 and dy2 != 0:
        # print("line1 horizontal and line2 vertical")
        if l1x1 <= l2x1 and l2x1 <= l1x2 and l2y1 <= l1y1 and l1y1 <= l2y2:
            return (l2x1, l1y1)
    # line1 vertical and line2 horizontal
    if dx1 == 0 and dx2 != 0:
        # print("line1 vertical and line2 horizontal")
        if l2x1 <= l1x1 and l1x1 <= l2x2 and l1y1 <= l2y1 and l2y1 <= l1y2:
            return (l1x1, l2y1)
    return None


def parse_cmds_from_string(s):
    return [(i[0], int(i[1:])) for i in s.split(",")]


def vertices_from_cmds(start, cmds):
    vertices = [start]
    previous = start
    for cmd in cmds:
        x, y = previous
        if cmd[0] == "R":
            x += cmd[1]
        elif cmd[0] == "L":
            x -= cmd[1]
        elif cmd[0] == "U":
            y += cmd[1]
        elif cmd[0] == "D":
            y -= cmd[1]
        else:
            raise NotImplementedError
        vertices.append((x, y))
        previous = (x, y)
    return vertices


def vertices_from_string(s):
    return vertices_from_cmds((0, 0), parse_cmds_from_string(s))


def intersections_md(line1, line2):
    for i in range(len(line1) - 1):
        segment1 = (line1[i], line1[i + 1])
        for j in range(len(line2) - 1):
            segment2 = (line2[j], line2[j + 1])
            # print(segment1, segment2)
            int_pt = intersection(segment1, segment2)
            # print(int_pt)
            if int_pt is not None and int_pt != (0, 0):
                yield man_dist(*int_pt)


def length(segment):
    dx = abs(segment[1][0] - segment[0][0])
    dy = abs(segment[1][1] - segment[0][1])
    return dx + dy


def intersections_time(line1, line2):
    distance1 = 0
    for i in range(len(line1) - 1):
        distance2 = 0
        segment1 = (line1[i], line1[i + 1])
        for j in range(len(line2) - 1):
            segment2 = (line2[j], line2[j + 1])
            # print(segment1, segment2)
            int_pt = intersection(segment1, segment2)
            # print(int_pt)
            if int_pt is not None and int_pt != (0, 0):
                d1 = length((segment1[0], int_pt))
                d2 = length((segment2[0], int_pt))
                yield distance1 + distance2 + d1 + d2
            distance2 += length(segment2)
        distance1 += length(segment1)


def test():
    line1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72\n"
    line1 = vertices_from_string(line1)
    line2 = "U62,R66,U55,R34,D71,R55,D58,R83\n"
    line2 = vertices_from_string(line2)
    print("Part 1 - test1 {0} == 159".format(min(intersections_md(line1, line2))))
    print("Part 2 - test1 {0} == 610".format(min(intersections_time(line1, line2))))
    line1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n"
    line1 = vertices_from_string(line1)
    line2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7\n"
    line2 = vertices_from_string(line2)
    print("Part 1 - test2 {0} == 135".format(min(intersections_md(line1, line2))))
    print("Part 2 - test2 {0} == 410".format(min(intersections_time(line1, line2))))


def main():
    lines = sys.stdin.readlines()
    line1 = vertices_from_string(lines[0])
    line2 = vertices_from_string(lines[1])
    part1 = min(intersections_md(line1, line2))
    part2 = min(intersections_time(line1, line2))
    print("Part 1: {0}".format(part1))
    print("Part 2: {0}".format(part2))


if __name__ == "__main__":
    # test()
    main()
