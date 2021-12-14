# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 
# In Part 1 I use a brute force solution, and assume each letter
# pair in the template and all mutations will be valid rules
# There for I convert each rule in the form "CH -> B" to a dictionary
# entry with key = "CH" and value = "CBH". Therefore I can replace
# each pair in the input with the dictionary look up (because of the
# overlap, all but the last triple will be truncated to two characters.
# Note this solution grows very quickly doubling on each iteration, and
# within a few dozen iteration will yield a string that does not fit in
# memory.

# In part 2, I use a new algorithm which keeps track of all character
# pairs in the input as well as how many times they exist.  This dictionary
# will always be no bigger than the list of rules, and the counts can grow
# as large as the system can handle (the counts will be bigger than a Int32,
# but smaller than an int64, although Python can grow ints arbitrarily large)
# I convert each rule in the form "CH -> B" to a dictionary entry with
# key = "CH" and value = ("CB", "BH"). on each iteration, a new dictionary
# of pairs is created. If for example, I found there were 12 pairs of "CH" in the
# the input, I would add 12 to the counts for "CB" and "BH".
# counting is more complicated, because of the duplicates.  I noted that the first
# and last characters are always the same after each mutation, and they are the only
# locations that are not counted twice in the total of the pairs.
# for example in the stating sample template "NNCB", ends = (N,B) and
# pairs = {"NN":1, "NC":1, "CB":1}, the character counts in ends {N:1,B:1}, added
# to the character counts in pairs {N:3,C:2,B:1} = {N:4,C:2,B:2}, which is exactly
# double the real character counts

# Obviously the solution for Part2 also is a valid solution for Part1, but I kept
# both for comparison.

import collections # for Counter dictionary

def part1(lines):
    template, rules = parse(lines)
    polymer = template
    for i in range(0,10):
        polymer = mutate(polymer, rules)
    count = max_less_min(polymer)
    return count

def part2(lines):
    pairs, rules, ends = parse2(lines)
    for i in range(0,40):
        pairs = mutate2(pairs, rules)
    count = max_less_min2(pairs, ends)
    return count

#########
# Part 1 functions
#########

def parse(lines):
    template = lines[0].strip()
    rules = {}
    for line in lines[2:]:
        pair, result = line.strip().split(" -> ")
        rules[pair] = pair[0] + result + pair[1]
    return template, rules

def mutate(template, rules):
    result = "X"
    # assume that there is a valid pair (in rules) at each step in the polymer
    for i in range(0, len(template) - 1):
        pair = template[i:i+2]
        # if the assumption fails, i.e. a character pair in the polymer does not mutate,
        # the following lookup in rules will fail
        triple = rules[pair]
        result = result[:-1] + triple
    return result

def max_less_min(polymer):
    counts = collections.Counter(polymer)
    max = 0
    min = len(polymer)
    for count in counts.values():
        if count > max:
            max = count
        if count < min:
            min = count
    return max - min

#########
# Part 2 versions
#########

def parse2(lines):
    template = lines[0].strip()
    rules = {}
    pairs = {}
    for line in lines[2:]:
        pair, result = line.strip().split(" -> ")
        rules[pair] = (pair[0] + result, result + pair[1])
    for i in range(0, len(template) - 1):
        pair = template[i:i+2]
        if pair not in pairs: pairs[pair] = 0
        pairs[pair] += 1
    # The ends of the template are always the same, and they need to be added to the
    # character counts in pairs before halving the counts to get true count
    ends = (template[0],template[-1])
    return pairs, rules, ends

def mutate2(pairs, rules):
    # update has to happen simultaneously, so write to a new dictionary
    new_pairs = {}
    for pair, count in pairs.items():
        one, two = rules[pair]
        if one not in new_pairs: new_pairs[one] = 0
        new_pairs[one] += count
        if two not in new_pairs: new_pairs[two] = 0
        new_pairs[two] += count
    return new_pairs

def max_less_min2(pairs, ends):
    counts = {}
    counts[ends[0]] = 1
    counts[ends[1]] = 1
    for chars, count in pairs.items():
        if chars[0] not in counts: counts[chars[0]] = 0
        if chars[1] not in counts: counts[chars[1]] = 0
        counts[chars[0]] += count
        counts[chars[1]] += count
    max = 0
    min = 1_000_000_000_000_000
    for count in counts.values():
        if count > max:
            max = count
        if count < min:
            min = count
    # all the counts are doubles since adjacent pairs overlap
    return (max - min)//2

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
