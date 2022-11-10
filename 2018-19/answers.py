# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

ADDR = 'addr'
ADDI = 'addi'
MULR = 'mulr'
MULI = 'muli'
BANR = 'banr'
BANI = 'bani'
BORR = 'borr'
BORI = 'bori'
SETR = 'setr'
SETI = 'seti'
GTIR = 'gtir'
GTRI = 'gtri'
GTRR = 'gtrr'
EQIR = 'eqir'
EQRI = 'eqri'
EQRR = 'eqrr'

def part1(lines):
    ip_reg, ops = parse(lines)
    value = compute(ops,ip_reg)
    return value

def part2(lines):
    return -1

def parse(lines):
    """parse the first part of the input file and
    return 1 list of operations and the instruction
    pointer register. each operation is a 5 item list
    [op_code, reg_A, reg_B, reg_C]
    """
    ops = []
    ip_reg = int(lines[0].strip().replace("#ip ",""))
    for line in lines[1:]:
        line = line.strip()
        items = line.split()
        op = [items[0]] + [int(r) for r in items[1:]]
        ops.append(op)
    return ip_reg, ops

def compute(ops, ip_reg):
    reg = [0,0,0,0,0,0]
    ip = 0
    while 0 <= ip and ip < len(ops):
        reg[ip_reg] = ip
        # print(ip, reg, ops[ip], end='')
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
        reg_out[c] =  1 if reg[a] > b else 0
    if ins == GTRR:
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] > reg[b] else 0
    if ins == EQIR:
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if a == reg[b] else 0
    if ins == EQRI:
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        reg_out[c] =  1 if reg[a] == b else 0
    if ins == EQRR:
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        reg_out[c] = 1 if reg[a] == reg[b] else 0
    return reg_out       

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
