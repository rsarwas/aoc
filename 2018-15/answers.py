# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# map is a dictionary keyed with a (row,col) tuple, containing values
# indicating the contents of the location '.' open floor, ('G',hp) or ('E',hp)

POWER = 3
HP = 200
WALL = "#"
OPEN = "."
GOBLIN = "G"
ELF = "E"


def part1(lines):
    map = parse(lines)
    # display(32, map)
    round = do_battle(map)
    return score(round, map)


def do_battle(map, elf_power=POWER, goblin_power=POWER):
    round = 0
    while True:
        for unit in ordered_units(map):
            # Safety valve during testing
            if round > 100:
                display(7, map)
                print(round, map)
                return -1

            if not unit in map or map[unit] == OPEN:
                # unit was killed before it's turn began, skip it
                continue
            targets = get_targets(map, unit)
            if not targets:
                # If there are no targets for this unit, we are done!
                # print(round)
                # display(32, map)
                return round

            target = first_attackable_target(unit, targets, map)
            if target:
                if map[target][0] == ELF:
                    power = goblin_power
                else:
                    power = elf_power
                attack(map, target, power)
            else:
                best_move = find_best_move(map, unit, targets)
                if best_move:
                    unit = move(map, unit, best_move)
                    target = first_attackable_target(unit, targets, map)
                    if target:
                        if map[target][0] == ELF:
                            power = goblin_power
                        else:
                            power = elf_power
                        attack(map, target, power)
        round += 1
        # print(round)
        # display(7,map)


def part2(lines):
    map = parse(lines)
    # display(32, map)
    initial_elf_count = count_elves(map)
    elf_power = POWER
    while True:
        # safety valve
        if elf_power > 100:
            print("aborting")
            return -1
        map = parse(lines)
        round = do_battle(map, elf_power)
        lost_elves = initial_elf_count - count_elves(map)
        if lost_elves == 0:
            print("Elf Power Required", elf_power)
            return score(round, map)
        # print(elf_power, lost_elves, round)
        elf_power += 1


def count_elves(map):
    elves = 0
    for unit in map:
        unit_type = map[unit][0]
        if unit_type == ELF:
            elves += 1
    return elves


def parse(lines):
    map = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == OPEN:
                map[(r, c)] = char
            if char == GOBLIN or char == ELF:
                map[(r, c)] = (char, 200)
    return map


def display(size, map):
    output = []
    for row in range(size):
        line = [WALL] * size
        output.append(line)
    for key in map:
        (r, c) = key
        value = map[key]
        line = output[r]
        line[c] = value[0]
    for line in output:
        print("".join(line))
    for key in map:
        if map[key][0] != OPEN:
            print(f"{map[key][0]}{key} = {map[key][1]}")


def ordered_units(map):
    units = []
    for location in map:
        unit = map[location]
        if (unit[0] == GOBLIN or unit[0] == ELF) and unit[1] > 0:
            units.append(location)
    units.sort()
    return units


def get_targets(map, unit):
    unit_type = map[unit][0]
    if unit_type == GOBLIN:
        search_type = ELF
    else:
        search_type = GOBLIN
    targets = []
    for location in map:
        unit = map[location]
        if unit[0] == search_type:
            targets.append(location)
    return set(targets)


def first_attackable_target(unit, targets, map):
    # To attack, the unit first determines all of the targets that
    # are in range of it by being immediately adjacent to it.
    # If there are no such targets, the unit ends its turn.
    # Otherwise, the adjacent target with the fewest hit points is selected;
    # in a tie, the adjacent target with the fewest hit points which is
    # first in reading order is selected.
    r, c = unit
    target = None
    min_hp = 201
    # search in reading order
    for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:  # reading order
        loc = (r + dr, c + dc)
        if loc in targets:
            loc_hp = map[loc][1]
            if loc_hp < min_hp:
                target = loc
                min_hp = loc_hp
    return target


def attack(map, target_location, force):
    unit = map[target_location]
    unit = (unit[0], unit[1] - force)
    if unit[1] <= 0:
        map[target_location] = OPEN
    else:
        map[target_location] = unit


def find_first_move(map, unit, targets):
    # JUST FOR TESTING
    # find first open space in reading order and move to it
    r, c = unit
    if (r - 1, c) in map and map[(r - 1, c)] == OPEN:
        return (r - 1, c)
    if (r, c - 1) in map and map[(r, c - 1)] == OPEN:
        return (r, c - 1)
    if (r, c + 1) in map and map[(r, c + 1)] == OPEN:
        return (r, c + 1)
    if (r + 1, c) in map and map[(r + 1, c)] == OPEN:
        return (r + 1, c)
    return None


def find_best_move(map, unit_loc, targets):
    # prune to reachable targets
    # identify all attack points of reachable targets
    # find closest attack point (ties resolved in reading order)
    # find shortest path to closest attack point (ties resolved in reading order of first move)
    # return first move in shortest path

    # alternatively look at the 4 adjacent location in reading order and
    # calculate the path length to the closest reachable target, return the shortest

    # alternatively, lock at the 4 adjacent in reading order, if we find a target, return
    # otherwise, similarly check each of the adjacent that is open, ad infinitum until we find a target
    # or there is nothing left to check
    loc = unit_loc
    new_set = {loc}
    total_set = set()
    path = {loc: []}
    while True:
        if not new_set:  # empty, i.e nothing was found in last iteration
            break
        total_set = total_set | new_set
        search_list = list(new_set)
        search_list.sort()  # put in reading order
        new_set = set()
        for loc in search_list:
            for r, c in [(-1, 0), (0, -1), (0, 1), (1, 0)]:  # reading order
                new_loc = (loc[0] + r, loc[1] + c)
                if new_loc in targets:
                    # print(targets)
                    # print(new_loc)
                    # print(total_set)
                    # print(path)
                    return path[loc][0]
                if new_loc in total_set or new_loc in new_set:
                    continue
                if new_loc in map and map[new_loc] == OPEN:
                    new_set.add(new_loc)
                    path[new_loc] = path[loc] + [new_loc]
    return None


def move(map, unit, best_move):
    map[best_move] = map[unit]
    map[unit] = OPEN
    return best_move


def score(round, map):
    total_g = 0
    total_e = 0
    for location in map:
        unit = map[location]
        if unit[0] == GOBLIN:
            total_g += unit[1]
        if unit[0] == ELF:
            total_e += unit[1]
    if total_e == 0:
        return round * total_g
    if total_g == 0:
        return round * total_e
    # oops, we called for the score before all battles are done
    return -1


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    # lines = open("test6.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
