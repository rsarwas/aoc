# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

def part1(serial_no):
    fuel_cells = {}
    for x in range(1,301):
        for y in range(1,301):
            fuel_cells[x,y] = power_level(x,y,serial_no)
    max_location = (0,0)
    max_value = 0
    for x in range(1,298):
        for y in range(1,298):
            square = 0
            for dx in range(3):
                for dy in range(3):
                    square += fuel_cells[x+dx,y+dy]
            if square > max_value:
                max_value = square
                max_location = (x,y)
    return max_location

def part2(serial_no):
    return -1

def power_level(x, y, serial_no):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_no
    power_level *= rack_id
    # get the hundreds place digit 12345 => 3; 45 => 0
    power_level = (power_level // 100) % 10
    power_level -= 5
    return power_level

if __name__ == '__main__':
    # print(f"Power Level Test 1: {power_level(3,5,8)} == 4")
    # print(f"Power Level Test 2: {power_level(122,79,57)} == -5")
    # print(f"Power Level Test 3: {power_level(217,196,39)} == 0")
    # print(f"Power Level Test 4: {power_level(101,153,71)} == 4")
    # print(f"test 1a: {part1(18)} == (33,45)")
    # print(f"test 2a: {part1(42)} == (21,61)")
    print(f"Part 1: {part1(9306)}")
    # print(f"Part 2: {part2(9306)}")
