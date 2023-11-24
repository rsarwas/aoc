import sys
from computer import Computer


def boost(code, input):
    c = Computer(code)
    c.push_input(input)
    c.start()
    return c.pop_output()


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.read().split(",")]
    boost_keycode = boost(program, 1)
    print("Part 1: {0}".format(boost_keycode))
    coords = boost(program, 2)
    print("Part 2: {0}".format(coords))
