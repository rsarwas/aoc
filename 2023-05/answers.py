"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
DEBUG = False
START = "seed"
END = "location"


def part1(lines):
    """Solve part 1 of the problem."""
    seeds, transforms = parse(lines)
    locations = [find_value(START, END, seed, transforms) for seed in seeds]
    return min(locations)


def part2(lines):
    """Solve part 2 of the problem."""
    seeds, transforms = parse(lines)
    seed_ranges = fix_seeds(seeds)
    transforms = fix_transforms(transforms)
    seed_offsets = combine_transforms(START, END, transforms)
    ordered_seeds = make_ordered_seed_ranges(seed_offsets)
    # ordered_seeds are seed ranges ordered by location and may not be valid
    # base_seed is the valid seed with the lowest location number
    best_seed = min_overlap(ordered_seeds, seed_ranges)
    min_location = location_of_seed(best_seed, seed_offsets)
    if DEBUG:
        print(f"seed_ranges = {seed_ranges}")
        for start, (end, maps) in transforms.items():
            print(start, "->", end)
            for m in maps:
                print("  ", m)
        print(f"Combined Offsets: {START} -> {END}")
        for i in seed_offsets:
            print(i)
        print(f"ordered_seeds = {ordered_seeds}")
        print(f"best_seed = {best_seed}")
    return min_location


def parse(lines):
    """Parse the input lines into a list of seeds and transformations"""
    data = "".join(lines).strip()
    sections = data.split("\n\n")
    seeds = sections[0].strip().replace("seeds: ", "").split(" ")
    seeds = [int(seed) for seed in seeds]
    transforms = {}
    for section in sections[1:]:
        source, destination, ranges = parse_section(section)
        transforms[source] = (destination, ranges)
    return (seeds, transforms)


def parse_section(section):
    """Parse a transformation section of the input into the identifying names and the map"""
    lines = section.split("\n")
    source, destination = lines[0].strip().replace(" map:", "").split("-to-")
    maps = []
    for line in lines[1:]:
        dest, src, length = [int(item) for item in line.strip().split(" ")]
        maps.append((dest, src, length))
    return (source, destination, maps)


def find_value(start_name, end_name, seed, transforms):
    """Find the final transformed value (at end_name) of the seed"""
    end_value = seed
    while start_name != end_name:
        # print(f"{start_name} {end_value} ->")
        start_name, ranges = transforms[start_name]
        end_value = transform(end_value, ranges)
        # print(f"   {start_name} {end_value}")
    return end_value


def transform(end_value, ranges):
    """Transform a single value given its range map"""
    for dest, src, length in ranges:
        if src <= end_value <= src + length:
            new_end_value = dest + (end_value - src)
            return new_end_value
    return end_value


def fix_seeds(seeds):
    """Turn a list of seed numbers (part1) into a list ranges (part2)
    The range we want/return is a (start_seed_number, end_seed_number) pair.
    The pairs need to be in sorted order.
    The input is unsorted (start_seed_number, length_of_range) pairs."""
    seed_ranges = []
    for number_index in range(0, len(seeds), 2):
        length_index = number_index + 1
        pair = (seeds[number_index], seeds[number_index] + seeds[length_index] - 1)
        seed_ranges.append(pair)
    seed_ranges.sort()
    return seed_ranges


def fix_transforms(transforms):
    """Reorganizes the transformation ranges so they are easier for part 2."""
    for name in transforms:
        dest, maps = transforms[name]
        maps = fix_maps(maps)
        transforms[name] = (dest, maps)
    return transforms


def fix_maps(maps):
    """Fix the transformation ranges so they are easier to use in part 2."""
    temp_map = {}
    for dest, src, length in maps:
        temp_map[src] = (src + length, dest - src)
    add_ins = {}
    for end, _ in temp_map.values():
        if end not in temp_map:
            add_ins[end] = (None, 0)
    for k, v in add_ins.items():
        temp_map[k] = v
    if 0 not in temp_map:
        temp_map[0] = (None, 0)
    offsets = []
    for start, (_, delta) in temp_map.items():
        offsets.append((start, delta))
    offsets.sort()
    # remove redundant offsets
    new_maps = [offsets[0]]
    last_offset = offsets[0][1]
    for offset in offsets[1:]:
        if offset[1] == last_offset:
            continue
        new_maps.append(offset)
        last_offset = offset[1]
    return new_maps


def combine_transforms(start_name, end_name, transforms):
    """Combines all the transformation into one list of ordered (start, offset) pairs"""
    start_name, offsets = transforms[start_name]
    while start_name != end_name:
        start_name, next_offsets = transforms[start_name]
        offsets = combine_offsets(offsets, next_offsets)
    return offsets


def combine_offsets(offsets, next_offsets):
    """Merges the list of next_offsets with the existing offsets"""
    new_offsets = []
    start = offsets[0][0]
    last = offsets[-1][0]
    while True:
        offset1 = get_offset(start, offsets)
        offset2 = get_offset(start + offset1, next_offsets)
        offset = offset1 + offset2
        new_offsets.append((start, offset))
        if start == last:
            break
        start1 = find_next_start(start, 0, offsets)
        start2 = find_next_start(start, offset1, next_offsets)
        start = min(start1, start2)
    return new_offsets


def find_next_start(value, offset, offsets):
    """Find the first starting value in offsets that is greater than value"""
    # print(f"find_next_start({value}, {offset}")
    offset_value = value + offset
    first_start = offsets[0][0]
    if offset_value < first_start:
        if DEBUG:
            print(f"offset_value < first_start: {offset_value} < {first_start}")
            print(f"return first_start - offset: {first_start} - {offset}")
        return first_start - offset
    for index, (start, _) in enumerate(offsets[:-1]):
        next_start = offsets[index + 1][0]
        if start <= offset_value < next_start:
            if DEBUG:
                print(f"{start} <= {offset_value} < {first_start}")
                print(f"return next_start - offset: {next_start} - {offset}")
            return next_start - offset
    # value must be larger than the last stating position, so the next value is infinity
    return 1e38


def make_ordered_seed_ranges(offsets):
    """Return a list of seed ranges [(s1,s2), (s3,s4), ...] ordered by the offset value.
    Offsets looks like [(x1,o1), (x2,o2), ... (xn, on)] where the xs are ordered.
    offset i applies to all x where xi <= x <= x(i+1). x >= xn can be ignored.
    When x is a seed number and o is the offset to the matching location number,
    then we can create a list of ordered location to the input seed number:
    [(l1,l2), ((l3,l4), ...],  [(s1, s2)), (s3,s4), ...], where l1 < l2 < l3 < l4 ...
    and location li + x derives from seed si + x, where x >= 0 and x < l(i+1) - li.
    With this the first seed number in s1..s2, s3..s4, ... that is a valid seed
    has the lowest location number."""
    locations = []
    for index, (start_seed, offset) in enumerate(offsets[:-1]):
        location = start_seed + offset
        next_seed = offsets[index + 1][0]
        locations.append((location, start_seed, next_seed - 1))
    locations.sort()
    seed_ranges = [(s1, s2) for (_, s1, s2) in locations]
    return seed_ranges


def min_overlap(ranges1, ranges2):
    """Find the minimal value in ranges1, that is in ranges2.
    Ranges are ordered lists of (min,max) tuples"""
    for min1, max1 in ranges1:
        for min2, max2 in ranges2:
            if min1 < max2 and max1 > min2:
                # We have an overlap
                return max(min1, min2)
    # Should never happen
    return None


def location_of_seed(best_seed, seed_location_offsets):
    """best seed is a number, and seed_location_offsets is [(s1,o1), (s2, o2), ...]
    where s1 < s2 < ... and location i = si + oi.
    oi applies to all s where s >= s1 and s < s2."""
    return best_seed + get_offset(best_seed, seed_location_offsets)


def get_offset(value, offsets):
    """Transform value to a new_value, based on the offsets.
    Offsets = [(s1,o1), (s2,o2), ... (sn,on)] where si is the starting value for
    offset oi. s1 < s2 < ... sn.  offset oi applies to all values from si to s(i+1) - 1.
    all values sn or larger get offset on."""
    for index, (start, offset) in enumerate(offsets[:-1]):
        next_start = offsets[index + 1][0]
        if start <= value < next_start:
            # new_value = value + offset
            return offset
    # value must be larger than the last stating position, so add the last offset
    last_offset = offsets[-1][1]
    return last_offset


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
