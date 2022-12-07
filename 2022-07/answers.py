# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# fs is a dictionary with key = dir name (unique) and value = contents
# contents is a tuple (list of dir names, list of files)
# file is a tuple (size (int), name (string))


def part1(lines):
    fs = parse(lines)
    print(fs)
    print(len(fs))
    # fs_t = parse_test()
    # print(fs_t)
    sizes = {}
    get_sizes(fs, "/", sizes)
    total = 0
    print(len(sizes))
    for size in sizes:
        print("  ", size, sizes[size])
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
    fs = {}
    listing = False
    current_dir = None
    dir_lines = []
    for line in lines:
        line = line.strip()
        if listing:
            if line.startswith("$ "):
                # we are done collecting directory data
                listing = False
                if current_dir in fs:
                    print("ERROR IN UNIQUE ASSUMPTION", current_dir)
                fs[current_dir] = parse_dir(dir_lines)
                dir_lines = []
                #ignore the current line unles it is "$ cd {name}"
                if line.startswith("$ cd ") and line != "$ cd ..":
                    current_dir = line.replace("$ cd ", "")
                continue
            dir_lines.append(line)
            continue
        if line == "$ ls":
            listing = True
            continue
        if line == "$ cd ..":
            # ignore, it will always be followed by zero or more "$ cd .." then a "$ cd {name}"
            continue
        if line.startswith("$ cd "):
            current_dir = line.replace("$ cd ", "")
    # the last thing in the input is a directory listing, which needs to be parsed
    if current_dir and dir_lines:
        if current_dir in fs:
            print("ERROR IN UNIQUE ASSUMPTION (last)", current_dir)
        fs[current_dir] = parse_dir(dir_lines)
    return fs

def parse_dir(lines):
    dirs = []
    files = []
    for line in lines:
        if line.startswith("dir "):
            dirs.append(line.replace("dir ",""))
        else:
            size,name = line.split(" ")
            files.append((int(size),name))
    return (dirs, files)


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
