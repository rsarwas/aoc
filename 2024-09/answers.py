"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    blocks = parse(lines)
    # print(blocks)
    blocks = compress(blocks)
    # print(blocks)
    return checksum(blocks)


def part2(lines):
    """Solve part 2 of the problem."""
    blocks = parse(lines)
    # print(blocks)
    blocks = compress2(blocks)
    # print(blocks)
    return checksum(blocks)


def parse(lines):
    """Convert the lines of text into a useful data model."""
    blocks = []
    line = lines[0].strip()
    file = True
    id = 0
    block = 0
    for c in line:
        n = int(c)
        if file:
            blocks.append((block, n, id))
            id += 1
            file = False
        else:
            blocks.append((block, n, -1))
            file = True
        block += n
    return blocks


def compress(blocks):
    """Compress the list of blocks by moving the last file block into the
    first free block.  Continue until all the file blocks are before all the
    free blocks."""
    new_blocks = []
    while blocks:
        first = blocks.pop(0)
        start, length, id = first
        if id != -1:
            # keep the file blocks where they are
            new_blocks.append(first)
        else:
            # fill the free space
            free = length
            while free > 0 and blocks:
                last = blocks.pop()
                last_start, last_length, last_id = last
                # ignore and remove the free space at the end of the block list
                if last_id == -1:
                    continue
                size = min(free, last_length)
                new_block = (start, size, last_id)
                start += size
                new_blocks.append(new_block)
                if last_length > free:
                    # write the unused part back to the end of the list
                    last_block = (last_start, last_length - size, last_id)
                    blocks.append(last_block)
                free -= size
    return new_blocks


def compress2(blocks):
    """Compress the list of blocks by working from the end to the beginning, moving the
    whole last file into the first chunk of free space big enough for it.  If there is no
    free space big enough it does not move.

    Because a single chunk of free space in the list maybe replaced by a chunk of file,
    and a smaller chunk of free space, the indexing of blocks will change as we work.

    To change chunks at the end of the list that go from file to free space, we keep track
    of the starting block number and then convert them all at the end."""
    copy = list(blocks)
    copy.reverse()
    free_chunks = []
    for rindex, last in enumerate(copy):
        last_start, last_length, last_id = last
        if last_id == -1:
            continue
        # print("blocks", blocks)
        # print("process", last)
        for index, block in enumerate(blocks):
            start, length, id = block
            if start >= last_start:
                # print("No room for it")
                break
            if id == -1 and last_length <= length:
                # print("Space at ", block)
                if last_length == length:
                    blocks[index] = (start, length, last_id)
                else:
                    # write the file blocks and the remainder as free block
                    # insert() adds an item before index, so put the free space at index
                    # and insert the file
                    free = (start + last_length, length - last_length, -1)
                    file = (start, last_length, last_id)
                    # print("file", file, "free", free)
                    blocks[index] = free
                    blocks.insert(index, file)
                # mark this chunk for reclamation
                free_chunks.append(last_start)
                break

    # reclaim free space from the files that moved.
    for index, (start, l, _) in enumerate(blocks):
        if start in free_chunks:
            blocks[index] = (start, l, -1)
    return blocks


def checksum(blocks):
    """Sum of the block number (0..n) times the file id. skip free space."""
    total = 0
    for block, length, id in blocks:
        if id == -1:
            continue
        for n in range(block, block + length):
            total += n * id
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
    main(INPUT)
