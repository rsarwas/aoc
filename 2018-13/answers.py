# Data Model:
# ===========
# Create a list of carts.
# Each cart as the following state: (y, x, dir, intersections)
#  x and y are zero based indexes to the map for the current location
#  the y comes first in the tuple, so that the sorted list will be
#  the order they should move.
#  dir is one of '>','<','^','v' for the direction the cart is moving
#  intersection starts at zero and is the number of intersections the cart has
#  been through. intersection % 3  == 0 means go left, 1 means go straight, 2 means right
# The map is a dictionary with (x,y) keys and
# the value is one of {'|','-','+','/','\'}
# When building the map replace '>' and '<' with '-'
# and 'v', '^' with '|', and add it to the carts list

def part1(lines):
    map = lines
    carts, map = find_carts(map)
    # display(map,carts)
    location = run_until_crash(map,carts)
    # convert from row,col to x,y
    return (location[1], location[0])

def part2(lines):
    return -1

def find_carts(map):
    carts = []
    for row_index in range(len(map)):
        row = map[row_index]
        for col_index in range(len(row)):
            char = row[col_index]
            if char == '>' or char == '<' or char == '^' or char == 'v':
                cart = [row_index,col_index,char,0]
                carts.append(cart)
    for row_index in range(len(map)):
        row = map[row_index]
        row = row.replace('>','-').replace('<','-').replace('^','|').replace('v','|')
        map[row_index] = row
    return carts, map

def display(map,carts):
    map = list(map)  # make a copy
    for cart in carts:
        row = list(map[cart[0]])
        row[cart[1]] = cart[2]
        map[cart[0]] = "".join(row)
    print("".join(map))

def run_until_crash(map,carts):
    # carts are already sorted in order of precedence
    while True:
        for c in range(len(carts)):
            # make a copy, so we do not update the cart in the list until
            # after the crash check
            cart = list(carts[c])
            update_cart(cart, map)
            location = (cart[0], cart[1])
            if crash(location, carts):
                return location
            carts[c] = cart
        carts.sort()
        # display(map,carts)

def update_cart(cart, map):
    direction = cart[2]
    # bounds checking is not required since cart will always be on the track in the map
    if direction == '>':
        cart[1] += 1
    if direction == '<':
        cart[1] -= 1
    if direction == 'v':
        cart[0] += 1
    if direction == '^':
        cart[0] -= 1
    track = map[cart[0]][cart[1]]
    # track under a > or < is - and under v or ^ is |, except corners and intersections
    if track == '\\':
        if direction == '>': cart[2] = 'v'
        if direction == '<': cart[2] = '^'
        if direction == 'v': cart[2] = '>'
        if direction == '^': cart[2] = '<'
    if track == '/':
        if direction == '>': cart[2] = '^'
        if direction == '<': cart[2] = 'v'
        if direction == 'v': cart[2] = '<'
        if direction == '^': cart[2] = '>'
    if track == '+':
        if direction == '>':
            if cart[3] % 3 == 0: cart[2] = '^' # left
            if cart[3] % 3 == 1: cart[2] = '>' # straight
            if cart[3] % 3 == 2: cart[2] = 'v' # right
        if direction == '<':
            if cart[3] % 3 == 0: cart[2] = 'v' # left
            if cart[3] % 3 == 1: cart[2] = '<' # straight
            if cart[3] % 3 == 2: cart[2] = '^' # right
        if direction == 'v':
            if cart[3] % 3 == 0: cart[2] = '>' # left
            if cart[3] % 3 == 1: cart[2] = 'v' # straight
            if cart[3] % 3 == 2: cart[2] = '<' # right
        if direction == '^':
            if cart[3] % 3 == 0: cart[2] = '<' # left
            if cart[3] % 3 == 1: cart[2] = '^' # straight
            if cart[3] % 3 == 2: cart[2] = '>' # right
        cart[3] += 1
    return cart

def crash(location, carts):
    # a cart will not crash into itself, because the cart in the
    # list has the old location, and location is the new location
    for cart in carts:
        if cart[0] == location[0] and cart[1] == location[1]:
            return True
    return False

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
