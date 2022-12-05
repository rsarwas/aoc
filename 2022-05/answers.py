# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    stacks, instructions = parse(lines)
    reorg(stacks, instructions)
    # print(stacks)
    tops = [stack[-1] for stack in stacks]
    # print(tops)
    return "".join(tops)


def part2(lines):
    return -1


def parse(lines):
    stack_lines = []
    instructions = []
    for line in lines:
        if line.startswith("move"):
            line = line.replace("move ","")
            a, rest = line.split(" from ")
            b, c = rest.split(" to ")
            n = int(a)
            src = int(b)
            dest = int(c)
            instructions.append((n,src, dest))
        else:
            if line == "\n":
                continue
            stack_lines.append(line)
    # print(instructions)
    stacks = make_stacks(stack_lines)
    # print(stacks)
    return (stacks,instructions)


def make_stacks(stack_lines):
    count = int(stack_lines.pop().split().pop())
    # stacks = [[]]*count # BAD - list has count references to the same empty list
    stacks = []
    for _ in range(count):
        stacks.append([])
    for _ in range(len(stack_lines)):
        bottom = stack_lines.pop()
        for i in range(count):
            index = i*4+1
            crate = bottom[index:index+1]
            if crate != " ":
               stacks[i].append(crate)
    return stacks


def reorg(stacks, instructions):
    for (n, src, dest) in instructions:
        move(stacks[src-1], stacks[dest-1], n)


def move(s1,s2,n):
    for _ in range(n):
        x = s1.pop()
        s2.append(x)

if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
