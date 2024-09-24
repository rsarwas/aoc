# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
#

ADDR = "addr"
ADDI = "addi"
MULR = "mulr"
MULI = "muli"
BANR = "banr"
BANI = "bani"
BORR = "borr"
BORI = "bori"
SETR = "setr"
SETI = "seti"
GTIR = "gtir"
GTRI = "gtri"
GTRR = "gtrr"
EQIR = "eqir"
EQRI = "eqri"
EQRR = "eqrr"


def part1(lines):
    ip_reg, ops = parse(lines)
    reg = [0, 0, 0, 0, 0, 0]
    value = compute(reg, ops, ip_reg)
    return value


def part2(lines):
    # The following obvious solution is way too slow
    # ip_reg, ops = parse(lines)
    # reg = [1,0,0,0,0,0]
    # value = compute(reg, ops,ip_reg)
    # return value

    # by reverse engineering the input code, I discovered the following:
    #   with r0 = 0 (part1) code sets r4 to 906 (instructions 17 to 24) then runs
    #     instructions 1 to 15 to completion (when r5 > r4 and ip is set to 256 which is invalid)
    #   with r0 = 1 (part2) code sets r4 to 10551306 in instructions 17 to 33
    #     then sets r0 to 0 and proceeds as in part1
    # I tried running part 1 with various small limits (r4) to see if I could find a pattern
    # in the output (r0)
    # r4 r0
    # 2 3
    # 3 4
    # 4 7
    # 5 6
    # 6 12
    # 7 8
    # 8 15
    # 9 13
    # 10 18
    # 11 12
    # 12 28
    # 13 14
    # 14 24
    # 15 24
    # 16 31
    # 17 18
    # 18 39
    # 19 20
    # No luck there, so I rewrote the input code (instructions 1 to 16) in python,
    # see part2_py(r4), and tested with various limits to ensure correctness.
    # unfortunately, this code is too slow:
    # r4, time
    # 1000,  0.15 sec
    # 5000,  3.3 sec
    # 10000, 13 sec
    # 20000, 52 sec
    # 10551306, infinite seconds

    # I rewrote the python code again as part2_py2, verified it was correct, and realized
    # that it was returning the sum of all the factors of r4, just very inefficiently.
    # an efficient solution follows
    # return sum(factors(906)) # 1824 (part1)
    return sum(factors(10551306))  # 21340800 (part2)


def part2_test(lines):
    ip_reg, ops = parse(lines)
    for i in range(2, 50):
        reg = [0, 0, 0, 0, 0, 0]
        ops[24] = ["seti", i, 0, 4]
        value = compute(reg, ops, ip_reg)
        print(i, value, part2_py(i), part2_py2(i), sum(factors(i)))


def part2_py(r4):
    # main body of input code in psuedo python (with gotos -- not supported in python)
    # r5 = 1
    # .label2. r2 = 1
    # .label3. r3 = r2 * r5
    # if r3 == r4:
    #     r0 += r5
    # r2 += 1
    # if r2 > r4:
    #     r5 += 1
    #     if r5 > r4:
    #         goto .end.
    #     else:
    #         goto .label2.
    # else:
    #     goto .label3.
    # .end.

    # input code with gotos rewritten in while loops

    r0 = 0
    r5 = 1
    while r5 <= r4:
        r2 = 1
        while r2 <= r4:
            r3 = r2 * r5
            if r3 == r4:
                r0 += r5
            r2 += 1
        r5 += 1
    return r0


def part2_py2(r4):
    # input code rewritten again for clarity
    # now it is obvious that this returns the sum of all factors of r4
    # if r4 is prime it will return r4+1
    r0 = 0
    for r5 in range(1, r4 + 1):
        for r2 in range(1, r4 + 1):
            if r2 * r5 == r4:
                r0 += r5
    return r0


def factors(n):
    a = [i for i in range(1, int(n**0.5) + 1) if n % i == 0]
    b = [n // i for i in a]
    return set(a + b)


def parse(lines):
    """parse the first part of the input file and
    return 1 list of operations and the instruction
    pointer register. each operation is a 5 item list
    [op_code, reg_A, reg_B, reg_C]
    """
    ops = []
    ip_reg = int(lines[0].strip().replace("#ip ", ""))
    for line in lines[1:]:
        line = line.strip()
        items = line.split()
        op = [items[0]] + [int(r) for r in items[1:]]
        ops.append(op)
    return ip_reg, ops


def compute(reg, ops, ip_reg):
    ip = 0
    while 0 <= ip and ip < len(ops):
        reg[ip_reg] = ip
        # print(ip, reg, ops[ip], ' ', end='')
        reg = execute(reg, ops[ip])
        # print(reg)
        ip = reg[ip_reg] + 1
    return reg[0]


def execute(reg, opcode):
    reg_out = list(reg)
    ins, a, b, c = opcode
    if ins == ADDR:
        # addr (add register) stores into register C the result of adding register A and register B.
        reg_out[c] = reg[a] + reg[b]
    if ins == ADDI:
        # addi (add immediate) stores into register C the result of adding register A and value B.
        reg_out[c] = reg[a] + b
    if ins == MULR:
        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        reg_out[c] = reg[a] * reg[b]
    if ins == MULI:
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        reg_out[c] = reg[a] * b
    if ins == BANR:
        # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        reg_out[c] = reg[a] & reg[b]
    if ins == BANI:
        # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        reg_out[c] = reg[a] & b
    if ins == BORR:
        # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        reg_out[c] = reg[a] | reg[b]
    if ins == BORI:
        # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        reg_out[c] = reg[a] | b
    if ins == SETR:
        # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        reg_out[c] = reg[a]
    if ins == SETI:
        # seti (set immediate) stores value A into register C. (Input B is ignored.)
        reg_out[c] = a
    if ins == GTIR:
        # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if a > reg[b] else 0
    if ins == GTRI:
        # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] > b else 0
    if ins == GTRR:
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] > reg[b] else 0
    if ins == EQIR:
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if a == reg[b] else 0
    if ins == EQRI:
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] == b else 0
    if ins == EQRR:
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] == reg[b] else 0
    return reg_out


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    # part2_test(lines)
    print(f"Part 2: {part2(None)}")
