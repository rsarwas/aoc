# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# fs is a dictionary with key = dir name (unique) and value = contents
# contents is a tuple (list of dir names, list of files)
# file is a tuple (size (int), name (string))


def part1(lines):
    fs = parse(lines)
    print(fs)
    fs_t = parse_test()
    print(fs_t)
    sizes = {}
    get_sizes(fs_t, "/", sizes)
    total = 0
    # print(sizes)
    for d in sizes:
        if sizes[d] <= 100000:
            total += sizes[d]
    return total


def part2(lines):
    return -1


def get_sizes(fs, root, sizes):
    dirs, files = fs[root]
    size = 0
    for file in files:
        size += file[0]
    for d in dirs:
        get_sizes(fs, d, sizes)
        size += sizes[d]
    sizes[root] = size

def parse(lines):
    return {}

def parse_test():
    d = {}
    d["/"] = (["a", "d"], [(14848514, "b.txt"), (8504156, "c.dat")])
    d["a"] = (["e"], [(29116,"f"), (2557,"g"), (62596,"h.lst")])
    d["e"] = ([],[(584,"i")])
    d["d"] = ([], [(4060174,"j"),(8033020,"d.log"),(5626152,"d.ext"),(7214296,"k")])
    return d
         

if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
