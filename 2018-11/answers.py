# This is a brute force solution, and it is pretty slow (about 1 minute)
# Is there a better (math oriented) solution using the power cell formula?

def part1(serial_no):
    grid_size = 300
    fuel_cells = build_fuel_cells(grid_size, serial_no)
    _, max_location = max_cells(fuel_cells, grid_size, 3)
    return max_location

def part2(serial_no):
    grid_size = 300
    fuel_cells = build_fuel_cells(grid_size, serial_no)
    max_value = -100000
    max_location = (0,0)
    max_size = 0
    size = 25 #ignore larger squares (negatives will dominate)
    while size >= 3 and max_value < size*size*4:
        value, location = max_cells(fuel_cells, grid_size, size)
        print(size, location, value)
        if value > max_value:
            max_value = value
            max_location = location
            max_size = size
        size -= 1
    return max_location, max_size

def build_fuel_cells(size, serial_no):
    fuel_cells = {}
    max_range = size + 1
    for x in range(1, max_range):
        for y in range(1,max_range):
            fuel_cells[x,y] = power_level(x,y,serial_no)
    return fuel_cells 

def max_cells(fuel_cells, max_size, size):
    max_location = (0,0)
    max_value = -100000
    for x in range(max_size-size):
        for y in range(max_size-size):
            square = 0
            for dx in range(size):
                for dy in range(size):
                    square += fuel_cells[1+x+dx,1+y+dy]
            if square > max_value:
                max_value = square
                max_location = (1+x,1+y)
    return max_value, max_location

def power_level(x, y, serial_no):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_no
    power_level *= rack_id
    # get the hundreds place digit 12345 => 3; 45 => 0
    power_level = (power_level // 100) % 10
    power_level -= 5
    return power_level # -5 ... 4

if __name__ == '__main__':
    # print(f"Power Level Test 1: {power_level(3,5,8)} == 4")
    # print(f"Power Level Test 2: {power_level(122,79,57)} == -5")
    # print(f"Power Level Test 3: {power_level(217,196,39)} == 0")
    # print(f"Power Level Test 4: {power_level(101,153,71)} == 4")
    # print(f"test 1a: {part1(18)} == (33,45)")
    # print(f"test 2a: {part1(42)} == (21,61)")
    # print(f"test 1b: {part2(18)} == (90,269,16)")
    # print(f"test 2b: {part2(42)} == (232,251,12)")
    print(f"Part 1: {part1(9306)}")
    print(f"Part 2: {part2(9306)}")
