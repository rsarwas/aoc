# Data Model:
# ===========
# input is a single line of 4 characters {<,>,^,v}
# visits is a dictionary with an (x,y) tuple for the key
# and value is the number of times visited

def part1(line):
    visits = {}
    (x,y) = (0,0)
    visits[(x,y)] = 1
    for move in line:
        if move == 'v':
            y -= 1
        elif move == '^':
            y += 1
        elif move == '<':
            x -= 1
        elif move == '>':
            x += 1
        else:
            print(f'unexpected input: {move}; Skipping.')
            continue
        if (x,y) in visits:
            visits[(x,y)] += 1
        else:
            visits[(x,y)] = 1
    return len(visits)

def part2(line):
    visits = {}
    (x,y) = (0,0)
    (rx,ry) = (0,0)
    visits[(x,y)] = 2
    real_santa = True
    for move in line:
        if real_santa:
            if move == 'v':
                y -= 1
            elif move == '^':
                y += 1
            elif move == '<':
                x -= 1
            elif move == '>':
                x += 1
            else:
                print(f'unexpected input: {move}; Skipping.')
                continue
            if (x,y) in visits:
                visits[(x,y)] += 1
            else:
                visits[(x,y)] = 1
        else:
            if move == 'v':
                ry -= 1
            elif move == '^':
                ry += 1
            elif move == '<':
                rx -= 1
            elif move == '>':
                rx += 1
            else:
                print(f'unexpected input: {move}; Skipping.')
                continue
            if (rx,ry) in visits:
                visits[(rx,ry)] += 1
            else:
                visits[(rx,ry)] = 1
        real_santa = not real_santa
    return len(visits)



if __name__ == '__main__':
    # print(f"test 1a {part1('>')} == 2")
    # print(f"test 2a {part1('^>v<')} == 4")
    # print(f"test 3a {part1('^v^v^v^v^v')} == 2")
    # print(f"test 1b {part2('^v')} == 3")
    # print(f"test 2b {part2('^>v<')} == 3")
    # print(f"test 3b {part2('^v^v^v^v^v')} == 11")
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines[0])}")
    print(f"Part 2: {part2(lines[0])}")
