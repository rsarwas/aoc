"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import sys  # for exit() during debugging
import time  # for timing during debugging

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    inputs, gates = parse(lines)
    # print(inputs, gates)
    values = fill_circuit(inputs, gates)
    # print(values)
    return get_value("z", values)


def part2(lines):
    """Solve part 2 of the problem."""
    inputs, gates = parse(lines)
    z_out = get_z_values(inputs)
    # print(inputs)
    # print(z_out)
    #
    # Maybe we can work backwards what gates immediately influence the final gates?
    # for name in z_out:
    #     op, in1, in2 = gates[name]
    #     print(in1, op, in2, "->", z_out[name])
    # Hmm, that looks too tricky, especially with XOR ops

    # How many gates influence a given output node?
    # show_depth(z_out, gates)
    #
    # what does this dependency heirarchy look like?
    # for name in ["z09", "z39"]:
    #     print(f"{name}={z_out[name]}")
    #     show_me(0, name, inputs, gates)

    # lets look at all the final output gates to see if they are already correct
    # i.e we do not want to change any inputs ( or  change multiple in a canceling way),
    # and those that are wrong, and need to have some gate swapped to get the right output
    # fix_or_keep(inputs, gates, z_out)
    # output:  final gate that is wrong, and the number of gates influencing it
    # all other z gates are fine as is.
    # z09 FIX  56
    # z10 FIX  58
    # z13 FIX  76
    # z21 FIX  124
    # z22 FIX  130
    # z23 FIX  136
    # z39 FIX  2
    # z40 FIX  238
    # z41 FIX  244
    # z42 FIX  250

    # Lets take a look at the dependency graph of a few of these
    # for name in ["z09", "z39"]:
    #     print(f"{name}={z_out[name]}")
    #     show_me(0, name, inputs, gates)

    # Reviewing these manually, I can see that both z09 and z39 will be fixed if I swap z39 and mnm
    # making the swap will mean that mnm puts out a False instead of the True it did before
    # will this have much influence on other outputs besides z09?
    # dependents = all_dependents(inputs, gates)
    # # display_dependents(dependents)
    # # display_influence(dependents)
    # mnm_zgates = [g for g in list(dependents["mnm"]) if g.startswith("z")]
    # print(len(mnm_zgates), mnm_zgates)
    # turns out swapping mnm will influence 36 out of the 44 final z gates.  some may not change,
    # but I suspect too many of the current keepers will need to be fixed.

    # Looking at
    # display_influence(dependents)
    # which list each gate by the number of other gates it influences, I can try to pick those
    # from the top of the list.
    # looking at
    # for name in ["z09", "z10", "z13", "z21", "z22", "z23", "z39", "z40", "z41", "z42"]:
    #     i_gates = list(influencers(name, inputs, gates))
    #     i_gates.sort()
    #     print(name, i_gates)

    # TODO: Rank each of the influener gates above, by the count of dependencies
    # in display_influence(dependents) find gates that will impact the final
    # gate I'm interested in without hopefully influencing any others
    # hopefully I can find some level1 gates that are in this category

    # I can see a set of gates that could be swapped, not all of those will
    # change the results, for that I need to explore the results of show_me()

    # these gates will not change, since they are only influenced by the input parameters.
    # they should be the first to test on influencing a broken output
    # show_level1(inputs, gates)
    # looking at just these is still almost 2000 pairs or opposite value swaps
    # which 2000, choose 4 is still too large of a number to explore

    # fix_or_keep(inputs, gates, z_out)
    # try_safe_swap(inputs, gates, z_out)

    # 65 gates that are only used in an OR or AND, where
    # changing its value will not change the outcome of the parent gate
    # of course these become relevant if the sibling is changed.
    # so it is possible that they will need to be part of a swap if the
    # sibling is swapped.
    # try and remove these from the pairings that should be checked
    # to see if the problem become tractable, and maybe we get lucky
    # These optimizations help, but do not get the total number of
    # pairs below 2900.

    # values = gates_values(inputs, gates)
    # l = irrelevant(values, inputs, gates)
    # for n in inputs:
    #     if n in l:
    #         l.remove(n)
    # print(len(l), l)

    # # print("z00", display("z00", gates))
    # sys.exit()

    values = gates_values(inputs, gates)
    ignore = irrelevant(values, inputs, gates)
    pairs = find_mutations(z_out, inputs, gates, values, ignore)
    if pairs is None:
        return "Failed!"
    gate_list = []
    for name1, name2 in pairs:
        gate_list.append(name1)
        gate_list.append(name2)
    gate_list.sort()
    answer = ",".join(gate_list)
    return answer


def display_alpha(dependents):
    names = list(dependents.keys())
    names.sort()
    for name in names:
        print(name, len(dependents[name]))


def display_influence(dependents):
    counts = []
    for name, deps in dependents.items():
        counts.append((len(deps), name))
    counts.sort()
    for count, name in counts:
        print(name, count)


def all_dependents(inputs, gates):
    """Return a dictionary of all gates (except the z gates),
    returning the set of all other gates that are dependent on
    (influenced by) the gate."""
    results = {}
    for name in gates:
        results[name] = set()
    for name1 in gates:
        for name2 in gates:
            if name1 in influencers(name2, inputs, gates):
                results[name1].add(name2)
    return results


# cache for the dependency heirarchy.  will need to be cleared and recreated
# if any gates are swapped
i_cache = {}


def influencers(name, inputs, gates):
    """Return the set of all gates that are influence on this node"""
    if name in inputs:
        return set()
    if name in i_cache:
        return i_cache[name]
    _, n1, n2 = gates[name]
    results = influencers(n1, inputs, gates)
    results = results.union(influencers(n2, inputs, gates))
    results.add(n1)
    results.add(n2)
    i_cache[name] = results
    return results


def gates_values(inputs, gates):
    values = {}
    for name in gates:
        value = calc(name, inputs, gates)
        values[name] = value
    return values


def irrelevant(values, inputs, gates):
    ignore = set()
    for name in gates:
        op, n1, n2 = gates[name]
        if n1 in values:
            v1 = values[n1]
        else:
            v1 = inputs[n1]
        if n2 in values:
            v2 = values[n2]
        else:
            v2 = inputs[n2]
        if op == "OR":
            if v1:
                ignore.add(n2)
            else:
                if n2 in ignore:
                    ignore.remove(n2)
            if v2:
                ignore.add(n1)
            else:
                if n1 in ignore:
                    ignore.remove(n1)
        if op == "AND":
            if not v1:
                ignore.add(n2)
            else:
                if n2 in ignore:
                    ignore.remove(n2)
            if not v2:
                ignore.add(n1)
            else:
                if n1 in ignore:
                    ignore.remove(n1)
    return ignore


def try_safe_swap(inputs, gates, z_out):
    swap, _ = fix_or_keep(inputs, gates, z_out)
    pairs = list(swap)
    n1, n2 = pairs
    print(n1, calc(n1, inputs, gates))
    # show_me(0, n1, inputs, gates)
    print(n2, calc(n2, inputs, gates))
    # show_me(0, n2, inputs, gates)
    print(gates[n1], gates[n2])
    temp = gates[n1]
    gates[n1] = gates[n2]
    gates[n2] = temp
    cache1.clear()
    cache2.clear()
    print(gates[n1], gates[n2])
    print(n1, calc(n1, inputs, gates))
    # show_me(0, n1, inputs, gates)
    print(n2, calc(n2, inputs, gates))
    # show_me(0, n2, inputs, gates)
    fix_or_keep(inputs, gates, z_out)


def fix_or_keep(inputs, gates, z_out):
    keepers = set()
    keep = 0
    fixers = set()
    fix = 0
    for name in z_out:
        v1 = z_out[name]
        v2 = calc(name, inputs, gates)
        if v1 == v2:
            keep += 1
            print(name, "Keep", len(influencers(name, inputs, gates)))
            keepers = keepers.union(contributors(name, inputs, gates))
        else:
            fix += 1
            print(name, "FIX ", len(influencers(name, inputs, gates)))
            fixers = fixers.union(contributors(name, inputs, gates))
    print(keep, "are good", fix, "need to be fixed")
    inputs = set(inputs.keys())
    fixers -= inputs
    keepers -= inputs
    print("keepers", len(keepers), "fixers", len(fixers), "all", len(gates))
    safe_to_fix = fixers - keepers
    ignore = keepers - fixers
    print(len(safe_to_fix), "safe to fix", safe_to_fix)
    print(len(ignore), "safe to ignore", ignore)
    return safe_to_fix, ignore


def show_depth(z_out, gates):
    # loc = []
    for name in z_out:

        # loc.clear()
        # loc = display(name, gates)
        print(name, depth(name, gates))


def depth(name, gates):
    return len(display(name, gates))


def show_me(level, name, inputs, gates):
    indent = "     " * level
    if name in gates:
        op, in1, in2 = gates[name]
        print(f"{indent}{name} = {in1} {op} {in2}")
        show_me(level + 1, in1, inputs, gates)
        show_me(level + 1, in2, inputs, gates)
    if name in inputs:
        if inputs[name]:
            print(f"{indent}{name}=1")
        else:
            print(f"{indent}{name}=0")


def show_level1(inputs, gates):
    names = list(gates.keys())
    names.sort()
    for name in names:
        (op, in1, in2) = gates[name]
        if in1 in inputs and in2 in inputs:
            val1, val2 = inputs[in1], inputs[in2]
            value = True
            if op == "AND":
                value = val1 & val2
            if op == "OR":
                value = val1 | val2
            if op == "XOR":
                value = val1 ^ val2
            print(f"{name} = {value} = {in1} {op} {in2}")


def level1gates(inputs, gates):
    names = []
    for name in gates.keys():
        (op, in1, in2) = gates[name]
        if in1 in inputs and in2 in inputs:
            names.append(name)
    return names


def display(name, gates):
    """Display the heirarchy of gates ending in name"""
    loc = display2(name, gates)
    # horizontally space by col # and vertically space by row #
    # print(loc)
    return loc


def display2(name, gates, row=0, col=0, loc={}):
    """Display the heirarchy of gates ending in name"""
    loc[name] = (row, col)
    if name.startswith("x") or name.startswith("y"):
        return loc
    op, name1, name2 = gates[name]
    loc = display2(name1, gates, row - 1, col + 1, loc)
    # loc[op] = (row, col + 1)
    loc = display2(name2, gates, row + 1, col + 1, loc)
    return loc


cache1 = {}


def calc(name, inputs, gates):
    """Recursively calculate the value of name"""
    if name in cache1:
        return cache1[name]
    if name in inputs:
        cache1[name] = inputs[name]
        return inputs[name]
    op, in1, in2 = gates[name]
    v1 = calc(in1, inputs, gates)
    v2 = calc(in2, inputs, gates)
    v = None
    if op == "OR":
        v = v1 | v2
    if op == "AND":
        v = v1 & v2
    if op == "XOR":
        v = v1 ^ v2
    cache1[name] = v
    return v


cache2 = {}


def contributors(name, inputs, gates):
    """Find the set of gates that contribute to the value of name"""
    if name in cache2:
        return cache2[name]
    if name in inputs:
        return set()
    # name is in gates, recurse
    _, in1, in2 = gates[name]
    results = set([in1, in2])
    results = results.union(contributors(in1, inputs, gates))
    results = results.union(contributors(in2, inputs, gates))
    cache2[name] = results
    return results


def parse(lines):
    """Convert the lines of text into a useful data model."""
    inputs = {}
    gates = {}
    in_part1 = True
    for line in lines:
        line = line.strip()
        if not line:
            in_part1 = False
            continue
        if in_part1:
            name, value = line.split(": ")
            inputs[name] = value == "1"
        else:
            wire1, op, wire2, _, output = line.split(" ")
            gates[output] = (op, wire1, wire2)
    return inputs, gates


def fill_circuit(inputs, gates):
    """Create a set of values for the circuit"""
    values = dict(inputs)
    # print(gates)
    names = gates.keys()
    unchecked = set(names)
    n = len(unchecked) + 1
    while len(unchecked) < n:
        n = len(unchecked)
        for name in gates:
            if name in values:
                continue
            op, name1, name2 = gates[name]
            if name1 in values and name2 in values:
                v1, v2 = values[name1], values[name2]
                value = None
                if op == "OR":
                    value = v1 | v2
                if op == "XOR":
                    value = v1 ^ v2
                if op == "AND":
                    value = v1 & v2
                values[name] = value
                unchecked.remove(name)
    return values


def find_mutations(z_out, inputs, gates, values, ignore):
    """Find the 4 swaps that make x + y == z"""
    x = get_value("x", inputs)
    y = get_value("y", inputs)
    # names = list(gates.keys())
    # t1 = time.time()
    # # swap_list = list(potential_swaps4(z_out, gates, values, ignore))
    # t2 = time.time()
    # total = t2 - t1
    # print(f"{total} to generate a list of {len(swap_list)} swaps to check")
    # n = 0
    for swaps in potential_swaps4(z_out, inputs, gates, values, ignore):  # swap_list:
        # print(swaps)
        # n += 1
        # t1 = time.time()
        values = process_swaps(inputs, gates, swaps)
        # t2 = time.time()
        # total += t2 - t1
        # if n == 1000:
        #     print(f"Average swap check is {total/1000}")  # 0.00035 sec/check
        #     print(f"{60*1000/total} checks per minute")  # 172000 checks per minute
        #     # print(f"Estimated run time is {total*len(swap_list)/1000}")
        z = get_value("z", values)
        # print(x, y, z)
        if x + y == z:
            return swaps
    return None


def potential_swaps2(gates):
    """Return a list of all 4 pairs of potential swaps"""
    pairs = get_pairs(gates)
    for i1, p1 in enumerate(pairs[:-1]):
        for p2 in pairs[i1 + 1 :]:
            yield [p1, p2]


def potential_swaps4(z_out, inputs, gates, values, ignore):
    """Return a list of all 4 pairs of potential swaps"""
    # pairs = get_pairs(z_out, gates, values, ignore)
    pairs = get_pairs2(values, inputs, gates)
    print("Number of pairs", len(pairs))
    count = len(pairs) ** 4
    minutes = count / 172000
    print(f"{count} sets of 4 pairs to check.  Estimated time = {minutes} minutes")
    for i1, p1 in enumerate(pairs[:-3]):
        s1 = set([p1[0], p1[1]])
        # print("p1", p1)
        # print(time, time.time())  # estimated 100 minutes for 2950 pairs
        for i2, p2 in enumerate(pairs[i1 + 1 : -2]):
            if p2[0] in s1 or p2[1] in s1:
                continue
            s2 = set([p2[0], p2[1]])
            # print("p2", p2)
            # print(time, time.time()) approx 2 sec per loop w/ ~2950 pairs
            for i3, p3 in enumerate(pairs[i1 + i2 + 2 : -1]):
                if p3[0] in s1 or p3[1] in s1 or p3[0] in s2 or p3[1] in s2:
                    continue
                s3 = set([p3[0], p3[1]])
                # print("p3", p3)
                for p4 in pairs[i1 + i2 + i3 + 3 :]:
                    if (
                        p4[0] in s1
                        or p4[1] in s1
                        or p4[0] in s2
                        or p4[1] in s2
                        or p4[0] in s3
                        or p4[1] in s3
                    ):
                        continue
                    # print("p4", p4)
                    yield [p1, p2, p3, p4]


def get_pairs(z_out, gates, values, ignore):
    """Return a list of all the pairs of names"""
    pairs = []
    ignore_z = set(z_out.keys())
    names = set(gates.keys()) - ignore - ignore_z
    # print(len(names), "names")
    names = list(names)
    for index, name1 in enumerate(names[:-1]):
        for name2 in names[index + 1 :]:
            if values[name1] != values[name2]:
                pairs.append((name1, name2))
    return pairs


def get_pairs2(values, inputs, gates):
    """Return a list pairs of the level1 gates
    swapping these gates will no cause any of these
    gates to change."""
    pairs = []
    gates = level1gates(inputs, gates)
    for index, name1 in enumerate(gates[:-1]):
        for name2 in gates[index + 1 :]:
            if values[name1] != values[name2]:
                pairs.append((name1, name2))
    return pairs


def process_swaps(inputs, gates, swaps):
    """Change the ops per the swaps, and return the circuit output values"""
    # mutate ops_xxx per swaps
    do_swap(gates, swaps)
    values = fill_circuit(inputs, gates)
    # revert the swaps, by swapping again.
    do_swap(gates, swaps)
    return values


def do_swap(gates, swaps):
    """swap the input on the pairs of gates in the ops"""
    for name1, name2 in swaps:
        temp = gates[name1]
        gates[name1] = gates[name2]
        gates[name2] = temp


def get_value(name, values):
    """Get the value on the wires starting with name."""
    names = [key for key in values.keys() if key.startswith(name)]
    names.sort()
    names.reverse()
    # print(names)
    output = []
    binary = {True: "1", False: "0"}
    for name in names:
        output.append(binary[values[name]])
    output = "".join(output)
    output = int(output, 2)
    return output


def get_z_values(inputs):
    """create a dictionary of the desired output"""
    output = {}
    x = get_value("x", inputs)
    y = get_value("y", inputs)
    z = x + y
    z = "{0:b}".format(z)
    # print(z)
    z = z[::-1]  # .reverse()
    # print(z)
    for index, bit in enumerate(z):
        name = "z{:02}".format(index)
        output[name] = bit == "1"
    return output


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
