import sys
from computer import Computer


def solve(intcode):
    computers = []
    for i in range(50):
        computer = Computer(intcode)
        computer.push_input(-1)
        computer.push_input(i)
        status = computer.start()
        if status == Computer.DONE:
            print(
                "Computer {0} halted on startup.  Output {1}".format(
                    i, computer.get_and_clear_output()
                )
            )
            computers.append(None)
        else:
            computers.append(computer)
    while True:
        for i in range(50):
            computer1 = computers[i]
            y_val = computer1.pop_output()
            if y_val == None:
                # print("No messages from {0}".format(i))
                continue
            x_val = computer1.pop_output()
            dest = computer1.pop_output()
            if dest == 255:
                # Halt condition
                return y_val
            if dest < 0 or dest > 49:
                print("Error: Computer {0} does not exist.  Ignoring".format(dest))
                continue
            # print(dest, x_val, y_val)
            computer2 = computers[dest]
            if computer2 is None:
                print(
                    "Error: sending message to halted computer: from {0} to {1}".format(
                        i, dest
                    )
                )
            computer2.push_input(y_val)
            computer2.push_input(x_val)
            status = computer2.resume()
            if status == Computer.DONE:
                print(
                    "Computer {0} halted after message ({1},{2}) from {3}".format(
                        dest, x_val, y_val, i
                    )
                )
                print(
                    "Computer {0} output = {1}".format(
                        dest, computer.get_and_clear_output()
                    )
                )
                computers[dest] = None
    return 0


def main():
    program = [int(x) for x in sys.stdin.read().split(",")]
    answer = solve(program)
    print("Part 1: {0}".format(answer))


if __name__ == "__main__":
    main()
