# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# there are ten strings before the pipe " | ", and 4 strings after
# each string is separated by a space, the strings contain only {a,b,c,d,e,f,g}
# 2 segments is a 1 (cf); 3 segs is a 7 (acf); 4 segs is a 4 (bcdf)
# 5 segs is a 2, 3, 5; 6 segs is a 0, 6 or 9;
# 7 segs is a an 8 (abcdefg)
#
# digits the result of break_code(line) is a dict with key = jumbled code; value = the number
# 

def part1(lines):
    total = 0
    search = set([2,3,4,7])
    for line in lines:
        _, output = line.strip().split(" | ")
        for signal in output.split(" "):
            if len(signal) in search:
                total += 1
    return total

def part2(lines):
    total = 0
    for line in lines:        
        patterns, output_signals = line.strip().split(" | ")
        digits = break_code(patterns)
        # print(digits)
        output = [digits["".join(sorted(code))] for code in output_signals.split(" ")]
        number = make_number(output)
        # print(output, number)
        total += number
    return total

def break_code(pattern_string):
    digits = {}
    patterns = pattern_string.split(" ")
    fives = [] # codes with length five (2,3, or 5)
    sixes = [] # codes with length six (0, 6 or 9)
    one = ""
    four = ""
    seven = ""
    # find the easy ones
    for pattern in patterns:
        if len(pattern) == 2:
            digits["".join(sorted(pattern))] = 1
            one = pattern
        elif len(pattern) == 3:
            digits["".join(sorted(pattern))] = 7
            seven = pattern
        elif len(pattern) == 4:
            digits["".join(sorted(pattern))] = 4
            four = pattern
        elif len(pattern) == 5:
            fives.append(pattern)
        elif len(pattern) == 6:
            sixes.append(pattern)
        elif len(pattern) == 7:
            digits["".join(sorted(pattern))] = 8
        else:
            print("akk! Unexpected pattern in input")
    # figure out the other segments:
    # the top segment is the difference between the one and the seven

    # the 9 is the only 6 letter code that has all the characters in the 4
    nine = find_nine(sixes, four)
    digits["".join(sorted(nine))] = 9
    sixes.remove(nine)

    # the zero is the only 6 letter code (after removing 9) that has all the characters in the 7
    zero = find_zero(sixes, seven)
    digits["".join(sorted(zero))] = 0
    sixes.remove(zero)

    # the 6 is the only remaining six character code
    digits["".join(sorted(sixes[0]))] = 6    

    # The 3 is the only 5 character code with both characters of the 1
    three = find_three(fives, one)
    digits["".join(sorted(three))] = 3
    fives.remove(three)

    # the 5 is the only 5 character code with both characters of the four without the ones characters
    five = find_five(fives, four, one)
    digits["".join(sorted(five))] = 5
    fives.remove(five)

    # the 2 is the only remaining five character code
    digits["".join(sorted(fives[0]))] = 2    

    return digits

def find_nine(codes, four):
    # the nine is the only 6 letter code that has all the characters in the 4
    for code in codes:
        nine = True
        for c in four:
            if c not in code:
                nine = False
        if nine:
            return code
    print("Aak!, four not found in the sixes", four, codes)

def find_zero(codes, seven):
    # the zero is the only 6 letter code (after removing 9) that has all the characters in the 7
    for code in codes:
        zero = True
        for c in seven:
            if c not in code:
                zero = False
        if zero:
            return code
    print("Aak!, seven not found in the sixes", seven, codes)

def find_three(codes, one):
    for code in codes:
        if one[0] in code and one[1] in code:
            return code
    print("one not found in the fives", one, codes)

def find_five(codes, four, one):
    rem = []  # four - one
    for c in four:
        if c not in one:
            rem.append(c)
    for code in codes:
        if rem[0] in code and rem[1] in code:
            return code
    print("Aak! four less one not found in the fives", one, codes)
    
def make_number(digit_list):
    number = 0
    bases = [1000, 100, 10, 1]
    for i in range(0,4):
        number += digit_list[i]*bases[i]
    return number

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
