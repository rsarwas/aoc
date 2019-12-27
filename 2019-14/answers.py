import sys

def get_reactions(lines):
    reactions = {}
    # the key is the output compound, the value is a tuple (product_qty, list of inputs)
    # the inputs are tuples (qty, compound)
    def parse(text):
        qty,compound = text.strip().split(' ')
        return int(qty), compound

    for line in lines:
        input,output = line.strip().split('=>')
        qty,compound = parse(output)
        reactions[compound] = (qty, [parse(c) for c in input.strip().split(',')])
    return reactions

# Recursive solution - simplify:
# if all the items in the list are not in the reactions, then done,
# otherwise simplify the list of all items expanded
# expanding all items is recursive, but only replaces the list of items with a # expanding returns all the 
# trick is that if a reaction needs 7 of item A and it comes in multiples of 10, I need
# to add up all reactions that need item A, and then get the closest multiple, so if all
# if there are 4 reactions that need 7 A, and 10 A => 1B, then I will end up with 3B (4*7 => 30),
# not 4B (i.e not 4*(7=>10))
def simplify(reactions, compound_list):
    done = True
    # if all the compounds are basic (i.e. no further reactions), we are done
    for amt, mtl in compound_list:
        if mtl in reactions:
            done = False
    if done:
        print('simplified ', compound_list)
        return compound_list
    print('simplify ', compound_list)
    expanded_list = []
    for amt, mtl in compound_list:
        if mtl not in reactions:
            expanded_list.append((amt, mtl))
        else:
            expanded_list += expand(reactions, amt, mtl)
    expanded_list = combine(expanded_list)
    print('simplify EL', expanded_list)
    # replace quantities of non-even multiples of compounds with even multiples
    expanded_list = [new_part(p, reactions) for p in expanded_list]
    return simplify(reactions, expanded_list) 

def new_part(old_part, reactions):
    qty, mtl = old_part
    if mtl not in reactions:
        return (qty, mtl)
    else:
        qty2, _ = reactions[mtl]
        qty2 *= (qty // qty2 + 1)  # i.e. qty = 28, qty2 = 10 => qty2 = 30
        return (qty2, mtl)

def expand(reactions, quantity, compound):
    # Expand only expands reactions when they are an even multiple
    # this way I can collect all of the various amounts of a component together
    # before replacing it with the next even multiple of the following reaction.
    print('expand ', quantity, compound)
    # returns a list of tuples.  Each tuple is the quantity and name of root components 
    if compound not in reactions:
        return [(quantity, compound)]
    qty, sources = reactions[compound]
    if quantity % qty != 0:
        return [(quantity, compound)]
    qty = quantity // qty
    compounds = []
    for amt, mtl in sources:
        compounds += expand(reactions, qty * amt, mtl)
    return compounds

def combine(l):
    if len(l) < 2:
        return l
    counts = {}
    for qty,mtl in l:
        if mtl not in counts:
            counts[mtl] = 0
        counts[mtl] += qty
    new_l = []
    for mtl in counts:
        new_l.append((counts[mtl],mtl))
    return new_l

if __name__ == '__main__':
    reactions = get_reactions(sys.stdin.readlines())
    print(reactions)
    core = simplify(reactions, [(1, 'FUEL')]) 
    print(core)
    print("Part 1: {0}".format(core[0][0]))

# t1:31, t2:165, t3:13312, t4:180697, t5:2210736
# The recursive solution works for tests 1 and 2, but not the others.
# Here is an example of the problem (from test 3):
# after 1st simplify, 1 FUEL =
#   [(154, 'B'), (3938, 'ORE'), (5, 'JJ'), (1, 'KK'), (29, 'A'), (9, 'E'), (48, 'D')]
# Since these are not multiples of the constituent reactions, we need to get the following:
#   [(156, 'B'), (3938, 'ORE'), (8, 'JJ'), (9, 'KK'), (30, 'A'), (10, 'E'), (50, 'D')]
# However, JJ and KK are made up of A,B,D, and E, which changes the amount of those
# components that are required.
