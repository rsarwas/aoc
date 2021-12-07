# Data Model:
# ===========
# Numbers is a list of non-negative integers less than 2000
#  The upper limit is based on a quick scan of the input and is not guaranteed.
# 

def part1(numbers):
    return solve_with(linear_fuel_cost)

def part2(numbers):
    return solve_with(triangle_fuel_cost)

def solve_with(solver):
    # solver is the fuel_cost function
    # print(numbers)
    avg = sum(numbers) // len(numbers)
    # start with the average, and then look up and down while total cost is not increasing
    min_cost = solver(numbers, avg)
    min_cost_down = solver(numbers, avg-1)
    min_cost_up = solver(numbers, avg+1)
    # print(avg, min_cost, min_cost_down, min_cost_up)
    if min_cost_down < min_cost:
        min_cost = min_cost_down
        delta = -1
    elif min_cost_up < min_cost:
        min_cost = min_cost_up
        delta = 1
    else:
        return min_cost
    for n in range(avg+delta,avg+(delta*avg),delta):
        new_cost = solver(numbers, n)
        # print(n, new_cost, min_cost)
        if new_cost <= min_cost:
            min_cost = new_cost
        else:
            print(n)
            return min_cost
    return -1

def linear_fuel_cost(numbers, target):
    return sum([abs(n - target) for n in numbers])

def triangle_fuel_cost(numbers, target):
    return sum([TRI[abs(n - target)] for n in numbers])

# The first 2000 triangle numbers; ignore 0; TRI[1] = 1, TRI[2] = 3, TRI[3] = 6 ...
TRI = [1]*2000
for i in range(2,2000):
    TRI[i] = i + TRI[i-1]

if __name__ == '__main__':
    # data = open("test.txt").read() # as one big string
    data = open("input.txt").read() # as one big string
    numbers = [int(n) for n in data.split(",")]
    print(f"Part 1: {part1(numbers)}")
    print(f"Part 2: {part2(numbers)}")
