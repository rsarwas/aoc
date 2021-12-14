# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 
# Create a weighted graph of the cost to get from any node (start and each key)
# to any other connected node, then  use Dijkstra's Shortest Path Algorithm.
# Problem: node list and weights will change after each node is visited.
#
# Brute Force - recursively get the cost to find all keys from each path at the
# current location.  Do not consider the path you were just on, unless you just
# found a key.  Backup and prune if you get to a dead end (or fill all dead ends
# before searching). When a key is found, open the door.  done when you find the
# last key (return 1). This may have infinite (or long loops) since you could go
# back and forth on the same path, but only when a key is found, so it should be
# go to zero as the keys are removed.
# 
# This is the brute force solution, which works with all samples except 4, which
# with 16 keys and 5 intersections has way too many paths to try. Removing 6 keys
# and it solves in about 90 seconds, checking over 5 million possible paths. The
# real input fails because it exceeds the Python's recursion limit. Boo Hoo.
#
# doors is a dict with the location of door for key (key is the lowercase
# alpha of the door). it is not mutated. The maze reveals the state of a door
# open == OPEN, closed == WALL; not all keys unlock a door; i.e. key may not be
# doors
# 
# Locations, start, current, previous, doors and keys are in the form (row_index,
# column_index), typically abbreviated (r,c), they are used as follows: maze[r][c]
#
# keys: a dictionary of un-found keys and their locations

def part1(lines):
    maze, keys, start, doors = parse(lines)
    dist = find_min_dist(start, None, maze, keys, doors)
    return dist

def part2(lines):
    return -1

WALL = "#"
OPEN = "."
START = "@"

def parse(lines):
    maze = [line.strip() for line in lines]
    start = find_start(maze)
    keys = find_keys(maze)
    doors = find_doors(maze)
    print_maze(maze)
    print(start)
    print(doors)
    print(keys)
    clean(maze, start, doors)
    print_maze(maze)
    return maze, keys, start, doors

def find_start(maze):
    for r, row in enumerate(maze):
        for c, elem in enumerate(row):
            if elem == START:
                return (r,c)
    return None
    
def find_keys(maze):
    keys = {}
    for r, row in enumerate(maze):
        for c, elem in enumerate(row):
            if elem >= "a" and elem <= "z":
                keys[elem] = (r,c)
    return keys
    
def find_doors(maze):
    doors = {}
    for r, row in enumerate(maze):
        for c, elem in enumerate(row):
            if elem >= 'A' and elem <= 'Z':
                doors[elem.lower()] = (r,c)
    return doors

def clean(maze, start, doors):
    # Make each door a WALL; it will be turned into an OPEN when a key
    # is found that is in DOORS (location of door for key is stored in DOORS)
    # also make the start area an OPEN.  These changes reduce the number of
    # special cases to consider when looking for options.
    r, c = start
    # maze[r] is a string, which is indexable, but not updatable
    maze[r] = maze[r][:c] + OPEN + maze[r][c+1:] # equivalent to maze[r][c] = OPEN
    for (r, c) in doors.values():
        maze[r] = maze[r][:c] + WALL + maze[r][c+1:] # equivalent to maze[r][c] = OPEN

def find_min_dist(current, previous, grid, keys, doors):
    # current is the (x,y) location where I am in the grid
    # previous is the previous location (no go) or None
    # if previous is None, we can go in any direction
    # previous is None at the start and when we land on a key
    # keys is the list of un-found keys.

    # print(current)
    global COUNTER
    if COUNTER % 100_000 == 0: print(COUNTER)

    # if there is a key at the current location, remove it from the keys list
    # and unlock (update the grid): set the key and door locations to open grid
    key = key_here(grid, current)
    if key is not None:
        # print("found key",key, keys[key])
        # unlock mutates the grid; it requires the location of the key, so wait to mutate keys
        unlock(grid, key, keys, doors)
        # mutate the dictionary of keys
        del keys[key]
        # if len(keys) == 9: print(list(keys.keys()))
        previous = None

    # We are done if there are no more keys to find
    if not keys:
        COUNTER += 1
        return 0

    # get a list of choices from the current position, there are three
    # scenarios:
    # 1) 0 choices (we are are at a dead end), return None to back up
    #    to the previous branch
    # 2) 2-4 choices we need to try each branch and return the length 
    #    of the shortest successful branch.
    # 3) 1 choice, no need to recurse, just go down the path, until we
    #    get to a key (it is a branch point), a dead end (no choices),
    #    or an intersection (> 1 choice). At a dead end, just return None
    #    to prune this branch, with an intersection, Check each branch and
    #    return the number of steps we took plus the best branch.  If we
    #    find a key, return the path length plus the solution (recursive)
    #    at the key location.

    # get the possible paths to take from current position
    # if previous is not None, then that is not an option
    choices = get_options(current, previous, grid)
    path_length = 1
    while len(choices) == 1:
        if key_here(grid, choices[0]) is not None:
            dist = find_min_dist(choices[0], current, copy(grid), keys.copy(), doors)
            if dist is None:
                return None
            else:
                return path_length + dist
        previous = current
        current = choices[0]
        path_length += 1
        choices = get_options(current, previous, grid)

    # If we run into a dead end (walls and/or doors block all directions),
    # then return None to indicate it is not a profitable path (at least
    # from the previous choices made to get here)
    if not choices:
        # print("No choices - abandon this path")
        COUNTER += 1
        return None

    # print(path_length, choices)

    min_dist = None
    for choice in choices:
        # Find the shortest distance of all the choices
        # be sure to give each call an independent copy of the current state
        # doors is not mutated, so it does not need to be copied
        dist = find_min_dist(choice, current, copy(grid), keys.copy(), doors)
        if dist is not None:
            # print("solved", dist, min_dist)
            if min_dist is None:
                min_dist = dist
            elif dist < min_dist:
                min_dist = dist
    if min_dist is None:
        return None
    return min_dist + path_length

COUNTER = 1

def key_here(maze, current):
    r, c = current
    elem = maze[r][c]
    if elem >= "a" and elem <= "z":
        return elem
    return None

def unlock(maze, key, keys, doors):
    # the location of the key goes from being a key to being OPEN
    # the location of the related door goes from being a WALL to OPEN
    r, c = keys[key]
    row = maze[r]
    # maze[r] is a string, which is indexable, but not updatable
    maze[r] = maze[r][:c] + OPEN + maze[r][c+1:] # equivalent to maze[r][c] = OPEN
    if key not in doors:
        return
    r, c = doors[key]
    maze[r] = maze[r][:c] + OPEN + maze[r][c+1:] # equivalent to maze[r][c] = OPEN

def get_options(current, previous, maze):
    options = []
    r,c = current
    for (dr, dc) in [(0,-1), (1,0), (0,1), (-1,0)]:
        r,c = current[0] + dr, current[1] + dc
        elem = maze[r][c]
        # Allow all OPEN and keys; only WALL and the previous cell is a no go. 
        # Maze perimeter is a wall, so no need to bounds check on r and c
        if elem == WALL: continue
        if previous is not None:
            if r == previous[0] and c == previous[1]: continue
        options.append((r,c))
    return options

def copy(rows):
    new_rows = []
    for row in rows:
        # row is an immutable string, so it does not need to be copied
        # if one grid replace a row (string) with a new one, it will not
        # change other grids that have the replaced string
        new_rows.append(row)
    return new_rows

def print_maze(maze):
    for row in maze:
        print(row)

if __name__ == '__main__':
    # lines = open("test1.txt").readlines()
    # print("test 1", part1(lines) == 8)
    # lines = open("test2.txt").readlines() # as a list of line strings
    # print("test 2a", part1(lines) == 86)
    # lines = open("test3.txt").readlines() # as a list of line strings
    # print("test 3a", part1(lines) == 132)
    lines = open("test4a.txt").readlines() # as a list of line strings
    print("test 4a", part1(lines) == 136)
    print(COUNTER)
    # lines = open("test5.txt").readlines() # as a list of line strings
    # print("test 5a", part1(lines) == 81)
    # lines = open("input.txt").readlines() # as a list of line strings
    # print(f"Part 1: {part1(lines)}")
    # print(f"Part 2: {part2(lines)}")
