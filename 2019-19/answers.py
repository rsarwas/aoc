import sys
from computer import Computer


def solve(intcode):
    # Simple brute force solution
    # we could print the 10 by 10 results to see if there is a cone pattern
    # and limit the edges of the cone, but this is just too easy.

    # While not stated clearly in the instructions, the program halts after
    # creating the output.  It cannot be resumed.  It can also not be restarted
    # I need to "reload" the int code for each run.

    total = 0
    results = []
    for y in range(50):
        row = []
        results.append(row)
        for x in range(50):
            computer = Computer(intcode)
            computer.push_input(y)
            computer.push_input(x)
            computer.start()
            output = computer.pop_output()
            row.append(output)
            if output == 1:
                total += 1
            # print(x, y, output, total)
        # print(''.join(['.' if i == 0 else '#' for i in row]))
    return total


def run(intcode, x, y):
    computer = Computer(intcode)
    computer.push_input(y)
    computer.push_input(x)
    computer.start()
    return computer.pop_output()


def solve2(intcode, x_avg, y_avg):
    """
    Scan the full width and height of the beam (+/- width) @ (x_avg,y_avg)
    """
    width = 120
    last_val = 0
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for x in range(x_avg - width, x_avg + width):
        beam = run(intcode, x, y_avg)
        if beam != last_val:
            if beam == 1:
                x_min = x
            else:
                x_max = x - 1
            # print("Y:", y_avg, "X:", x-1, last_val, x, beam)
            last_val = beam
    last_val = 0
    for y in range(y_avg - width, y_avg + width):
        beam = run(intcode, x_avg, y)
        if beam != last_val:
            if beam == 1:
                y_min = y
            else:
                y_max = y - 1
            # print("X:", x_avg, "Y:", y-1, last_val, y, beam)
            last_val = beam
    print(
        "@ ({0},{1}) X:{2}-{3}  Y:{4}-{5}".format(
            x_avg,
            y_avg,
            x_avg - x_min,
            x_max - x_avg + 1,
            y_avg - y_min,
            y_max - y_avg + 1,
        )
    )


def solve3(intcode, x_avg, y_avg):
    """
    Scan for the maximum edge of the beam @ (x_avg,y_avg)
    Assuming it is close to 100
    """
    size = 100
    for width in range(size - 5, size + 5):
        beam = run(intcode, x_avg + width, y_avg)
        if beam == 0:
            break
    for height in range(size - 5, size + 5):
        beam = run(intcode, x_avg, y_avg + height)
        if beam == 0:
            break
    print("@ ({0},{1}) W:{2}  H:{3}".format(x_avg, y_avg, width, height))


def main():
    program = [int(x) for x in sys.stdin.read().split(",")]
    answer = solve(program)
    print("Part 1: {0}".format(answer))
    # solve2(program, 1630, 1400)
    # solve2(program, 1640, 1400)
    # solve2(program, 1650, 1400)
    # solve2(program, 1822, 1556)
    # solve2(program, 1821, 1556)
    # solve2(program, 1822, 1557)
    # solve3(program, 1822, 1556)
    # solve3(program, 1821, 1556)
    # solve3(program, 1822, 1557)
    # solve3(program, 1868, 1596)
    # for x in range(1863, 1870):
    #    for y in range(1590, 1598):
    #        solve3(program, x, y)
    solve3(program, 1865, 1593)
    answer = 1865 * 10000 + 1593
    print("Part 2: {0}".format(answer))


if __name__ == "__main__":
    main()
