# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# edges is a list of (str,str) in the form (end1, end2) for the edges in the graph
# each edge is bidirectional
#


def part1(lines):
    edges = parse(lines)
    count = count_paths(["start"], edges)
    return count


def part2(lines):
    edges = parse(lines)
    count = count_paths2(["start"], edges, False)
    return count


def parse(lines):
    edges = []
    # nodes = {}
    for line in lines:
        start, end = line.strip().split("-")
        edges.append((start, end))
        # this may try to add a cove multiple times
        # this is simpler, with little cost, than checking before inserting
        # nodes[start] = is_big(start)
        # nodes[end] = is_big(end)
    return edges


def is_big(s):
    return s[0] in "ABCDEFGHIJKLMNOPQRSTUVWXY"


def count_paths(path, edges):
    # recursive counting solution
    # be sure to copy path, as each call needs its own copy
    branches = 0
    for node in adjacent_nodes(path, edges):
        if node == "end":
            # print(path + ["end"])
            branches += 1
        else:
            branches += count_paths(path.copy() + [node], edges)
    return branches


def adjacent_nodes(path, edges):
    # return a list of nodes, which are the other end of all edges
    # that have the last node in path at an end
    # skip the small nodes if they are already in the path
    adjacent = []
    node = path[-1]
    for edge in edges:
        end = None
        if edge[0] == node:
            end = edge[1]
        if edge[1] == node:
            end = edge[0]
        if end is None:
            continue
        if is_big(end) or end not in path:
            adjacent.append(end)
    return adjacent


def count_paths2(path, edges, has_double):
    # The similar to above, except it calls adjacent_nodes2
    branches = 0
    for node, has_double in adjacent_nodes2(path, edges, has_double):
        if node == "end":
            # print(path + ["end"])
            branches += 1
        else:
            branches += count_paths2(path.copy() + [node], edges, has_double)
    return branches


def adjacent_nodes2(path, edges, has_double):
    # return a list of (nodes,bool), which are the other end of all edges
    # that have the last node in path at an end, and if this adds a double small cave
    # skip the small nodes if they are already in the path
    # EXCEPT: 1 small cave can be visited twice (all other small caves can only be visited once)
    #         small caves "start", "end" can only be visited once
    adjacent = []
    node = path[-1]
    for edge in edges:
        end = None
        if edge[0] == node:
            end = edge[1]
        if edge[1] == node:
            end = edge[0]
        if end is None:
            continue
        if end == "start":
            continue
        if is_big(end):
            adjacent.append((end, has_double))
        else:
            if end not in path:
                adjacent.append((end, has_double))
            else:
                if not has_double:
                    adjacent.append((end, True))
    return adjacent


if __name__ == "__main__":
    # lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("test2.txt").readlines() # as a list of line strings
    # lines = open("test3.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
