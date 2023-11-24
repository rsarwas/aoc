import sys
from computer import Computer


def max_amplification(program):
    max_thrust = 0
    for phase_order in phase_setting_sequences(0, 4):
        output = 0
        for index in [0, 1, 2, 3, 4]:
            c = Computer(program)
            c.push_input(output)
            c.push_input(phase_order[index])
            c.start()  # do not need to check return status as it will not pause.
            output = c.pop_output()
        max_thrust = max(output, max_thrust)
    return max_thrust


def feedback_amplification(program):
    max_thrust = 0
    for phase_order in phase_setting_sequences(5, 9):
        computers = []
        output = 0
        for index in range(5):
            c = Computer(program)
            computers.append(c)
            c.push_input(output)
            c.push_input(phase_order[index])
            c.start()  # do not need to check return status as it pause when it needs new input.
            output = c.pop_output()
        done = False
        i = 0
        while not done:
            c = computers[i]
            c.push_input(output)
            status = c.resume()
            output = c.pop_output()
            done = i == 4 and status == Computer.done
            i = (i + 1) % 5
        max_thrust = max(output, max_thrust)
        # print(phase_order, output)
    return max_thrust


def phase_setting_sequences(start, end):
    settings = []
    all = set(range(start, end + 1))
    for i in all:
        for j in all - set([i]):
            for k in all - set([i, j]):
                for l in all - set([i, j, k]):
                    for m in all - set([i, j, k, l]):
                        settings.append((i, j, k, l, m))
    return settings


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.read().split(",")]
    thrust = max_amplification(program)
    print("Part 1: {0}".format(thrust))
    thrust = feedback_amplification(program)
    print("Part 2: {0}".format(thrust))
