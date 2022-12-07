# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# fs is a dictionary with key = path (unique) and value = contents
# path is a unix style path (i.e. parent_path/basename)
# contents is a tuple (list of dir names, list of files)
# file is a tuple (size (int), name (string))


def part1(lines):
    fs = parse(lines)
    print(len(fs))
    # print(len(fs))
    # fs_t = parse_test()
    # print(fs_t)
    sizes = {}
    get_sizes(fs, "/", sizes)
    total = 0
    print(len(sizes))
    # for size in sizes:
    #     print("  ", size, sizes[size])
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
        if root == "/":
            path = root + d
        else:
            path = root + "/" + d
        get_sizes(fs, path, sizes)
        size += sizes[path]
    sizes[root] = size


def parse(lines):
    fs = {}
    listing = False
    path = ""
    dir_lines = []
    for line in lines:
        line = line.strip()
        if listing:
            if line.startswith("$ "):
                # we are done collecting directory data
                listing = False
                if path in fs:
                    print("ERROR - non unique path", path)
                fs[path] = parse_dir(dir_lines)
                # now process the current line should start with "$ cd "
            else:
                dir_lines.append(line)
                continue
        if line == "$ ls":
            listing = True
            dir_lines = []
            continue
        if line == "$ cd ..":
            # print("cd ..", path)
            index = path.rindex("/")
            path = path[:index]
            if not path:
                path = "/"
            # print("  =>", path)
            continue
        if line.startswith("$ cd "):
            current_dir = line.replace("$ cd ", "")
            # print(line, path, current_dir)
            if not path or path[-1] == "/":
                path += current_dir
            else:
                path = path + "/" + current_dir
            # print("  =>", path)
    # At the EOF make sure we process the current listing
    if listing and path and dir_lines:
        if path in fs:
            print("ERROR - non unique path at EOF", path)
        fs[path] = parse_dir(dir_lines)
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
    d["/a"] = (["e"], [(29116,"f"), (2557,"g"), (62596,"h.lst")])
    d["/a/e"] = ([],[(584,"i")])
    d["/d"] = ([], [(4060174,"j"),(8033020,"d.log"),(5626152,"d.ext"),(7214296,"k")])
    return d
         

if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
