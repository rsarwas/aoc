import sys
from computer import Computer

def print_scaffolding(intcode):
    computer = Computer(intcode)
    computer.start()
    scaffold = computer.get_and_clear_output()
    scaffold_string = ''.join([chr(a) for a in scaffold])
    print(scaffold_string)

def solve2(intcode):
    """
    These instructions were derived by printing the scaffolding (above), and
    manually reviewing the scaffolding. See the file scaffolding.txt for details.
    """
    instructions = [
        "A,A,B,C,B,C,B,C,B,A\n",
        "R,10,L,12,R,6\n",
        "R,6,R,10,R,12,R,6\n",
        "R,10,L,12,L,12\n",
        "n\n"
    ]
    instructions = [[ord(c) for c in s] for s in instructions]
    # print(instructions)
    # The computer will pop() integers off of the end input queue as needed
    # Therefore I need to add merge the lines and reverse the codes
    combined = []
    for instruction in instructions:
        combined += instruction
    combined.reverse()
    # print(combined)

    intcode[0] = 2
    computer = Computer(intcode)
    for code in combined:
        computer.push_input(code)
    computer.start()
    return computer.pop_output()

def solve(intcode):
    def is_intersections(scaffold, index, platform, nchars):
        if scaffold[index] != platform:
            return False
        if scaffold[index-1] != platform:
            return False
        if scaffold[index+1] != platform:
            return False
        if scaffold[index-nchars] != platform:
            return False
        if scaffold[index+nchars] != platform:
            return False
        return True
    computer = Computer(intcode)
    computer.start()
    scaffold = computer.get_and_clear_output()
    # From inspecting the printed scaffold (see print command above):
    nlines = 33
    nchars = 52 # includes the newline (13)
    platform = 35
    sum_of_locations = 0
    for line in range(1, nlines-1):
        for char in range(1, nchars-1):
            index = line*nchars + char
            if scaffold[index] == platform:
                if is_intersections(scaffold, index, platform, nchars):
                    # print((line, char))
                    sum_of_locations += line * char
    return sum_of_locations

def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    # print_scaffolding(program)
    answer = solve(program)
    print("Part 1: {0}".format(answer))
    answer = solve2(program)
    print("Part 1: {0}".format(answer))

if __name__ == '__main__':
    main()
