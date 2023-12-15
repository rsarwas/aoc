"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    for step in data:
        total += my_hash(step)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    instructions = parse2(data)
    boxes = make_boxes()
    boxes = apply(instructions, boxes)
    # print(boxes)
    total = add_focus_power(boxes)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = lines[0].strip().split(",")
    return data


def parse2(data):
    """Return a dictionary of the values in the input"""
    result = []
    for item in data:
        if item.endswith("-"):
            name = item[:-1]
            value = 0
        else:
            name = item[:-2]
            value = int(item[-1])
        result.append((my_hash(name), name, value))
    return result


def my_hash(s):
    """Implement the puzzles hash algorithm."""
    result = 0
    for char in s:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def make_boxes():
    """Return a list of 256 empty independent lists"""
    boxes = []
    for _ in range(256):
        boxes.append([])
    return boxes


def apply(instructions, boxes):
    """Apply each of the instructions (per the puzzle rules) to the boxes."""
    for box_id, label, focal in instructions:
        if focal == 0:
            remove(boxes[box_id], label)
            # remove all lenses with the label in the box with box_id
        else:
            update(boxes[box_id], label, focal)
    return boxes


def remove(box, label):
    """Remove from box (a list of lenses) all lenses with label. Preserve ordering"""
    for i, lens in enumerate(box):
        if lens[0] == label:
            _ = box.pop(i)
            return


def update(box, label, focal):
    """Update the lenses in box.
    if label is in the box, update the focal length
    else add it to the end."""
    for i, lens in enumerate(box):
        if lens[0] == label:
            box[i] = (label, focal)
            return
    box.append((label, focal))


def add_focus_power(boxes):
    """Return the total focal power of the lenses in the boxes, per the puzzle rules"""
    total = 0
    for i, box in enumerate(boxes):
        box_num = i + 1
        for j, lens in enumerate(box):
            lens_num = j + 1
            focal_length = lens[1]
            power = box_num * lens_num * focal_length
            total += power
    return total


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    # print(my_hash("HASH"))
    main(INPUT)
