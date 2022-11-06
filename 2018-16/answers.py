# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

import ast # for literal_eval() to convert "[1,2,3]" to python list

ADDR = 0
ADDI = 1
MULR = 2
MULI = 3
BANR = 4
BANI = 5
BORR = 6
BORI = 7
SETR = 8
SETI = 9
GTIR = 10
GTRI = 11
GTRR = 12
EQIR = 13
EQRI = 14
EQRR = 15


def part1(lines):
    r_ins, ops, r_outs = parse1(lines)
    count = 0
    for i in range(len(r_ins)):
        r_in = r_ins[i]
        r_out = r_outs[i]
        opcode = ops[i]
        matches = test(r_in, r_out, opcode[1:])
        if matches >= 3:
            count += 1
    return count

def part2(lines):
    r_ins, ops, r_outs = parse1(lines)
    fixes = match_ops(r_ins, ops, r_outs)
    ops = parse2(lines)
    reg = compute(ops, fixes)
    return reg[0]

def parse1(lines):
    """parse the first part of the input file and
    return 3 lists
      1: the input registers (list of 4 ints) - line 1/3
      2: the instructions (list of 4 ints) - line 2/3
      3: the output registers (list of 4 ints) - line 3/3

    i.e.
    Before: [0, 2, 0, 2]
    6 0 1 1
    After:  [0, 1, 0, 2]
    """
    r_ins = []
    ops = []
    r_outs = []
    last_line_empty = False
    for line in lines:
        line = line.strip()
        if not line:
            if last_line_empty:
                return r_ins, ops, r_outs
            last_line_empty = True
            continue
        last_line_empty = False        
        if line.startswith("Before: "):
            reg = ast.literal_eval(line.replace("Before: ",""))
            r_ins.append(reg)
        elif line.startswith("After: "):
            reg = ast.literal_eval(line.replace("After:  ",""))
            r_outs.append(reg)
        else:
            ops.append([int(i) for i in line.split()])

def parse2(lines):
    empty_line_count = 0
    ops = []
    for line in lines:
        line = line.strip()
        if empty_line_count == 3:
            ops.append([int(i) for i in line.split()])
        else:
            if not line:
                empty_line_count += 1
            else:
                empty_line_count = 0
    return ops

def test(r_in, r_out, op_tail):
    count = 0
    for ins in range(16):
        reg = execute(r_in, [ins] + op_tail)
        if reg == r_out:
            count += 1
    return count

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

def compute(ops, fixes):
    reg = [0,0,0,0]
    for op in ops:
        op[0] = fixes[op[0]]
        reg = execute(reg, op)
    return reg

def match_ops(r_ins, ops, r_outs):
    all_matches = []
    for i in range(len(r_ins)):
        r_in = r_ins[i]
        r_out = r_outs[i]
        opcode = ops[i]
        all_matches.append(matches(r_in, r_out, opcode))
    fixes = analyze(all_matches)
    return fixes

def matches(r_in, r_out, opcode):
    in_op = opcode[0]
    op_tail = opcode[1:]
    matches = []
    for ins in range(16):
        reg = execute(r_in, [ins] + op_tail)
        if reg == r_out:
            matches.append(ins)
    return (in_op,matches)

def analyze(all_matches):
    fixes = {}
    while len(fixes) < 16:
        # find one to one matches
        remove_ops = set()
        for match in list(all_matches):
            their_op, my_ops = match
            # ins is the their number, match is a list of my numbers for the matching ops 
            if their_op in fixes:
                all_matches.remove(match)
                continue
            if len(my_ops) == 1:
                # update fixes
                fixes[their_op] = my_ops[0]
                remove_ops.add(my_ops[0])
                all_matches.remove(match)
                # do not break here, there may be more than one match
                # assume the matches are not broken i.e. 1 -> 3 and 1 -> 5
        # remove matches that are resolved
        for i, match in enumerate(all_matches):
            their_op, my_ops = match
            for remove_op in remove_ops:
                if remove_op in my_ops:
                    my_ops.remove(remove_op)
                    all_matches[i] = (their_op, my_ops)
    return fixes

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
