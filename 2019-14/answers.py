import math
import sys

def get_reactions(lines):
    reactions = {}
    # the key is the output compound, the value is a tuple (product_qty, list of inputs)
    # the inputs are tuples (qty, compound)
    def parse(text):
        qty, compound = text.strip().split(' ')
        return int(qty), compound

    for line in lines:
        src, dst = line.strip().split('=>')
        qty, compound = parse(dst)
        reactions[compound] = (qty, [parse(c) for c in src.strip().split(',')])
    return reactions


def get_depths(reactions, start):
    depths = {}
    for mtl in reactions:
        depths[mtl] = depth(mtl, start, reactions)
    return depths

def depth(mtl, bottom, reactions):
    if mtl == bottom:
        return 0
    # otherwise 1 + max depth of all constiuents
    consituents = [c[1] for c in reactions[mtl][1]]
    return 1 + max([depth(c, bottom, reactions) for c in consituents])

def expand(reactions, mtl, depths):
    """
    for every material count it's height in the graph, ORE is 0, everything created by ORE is 1,
    everything created by level 1 items is on level 2, etc until FUEL is n
    I will work down expanding all level n-1 items in the FUEL list with it's consituents,
    then combining like components and iterating down to level 0.
    Since I will be expanding all items on a level at the same time, I can expand without
    fear that I am not grouping all like components together before expanding.
    """
    level = depths[mtl[1]] - 1
    mtls = expand_item(mtl, reactions)
    while level > 0:
        # expand level
        new_mtls = []
        for mtl in mtls:
            new_mtls += expand_item(mtl, reactions) if depths[mtl[1]] == level else [mtl]
        mtls = combine(new_mtls)
        level -= 1
        #print(mtls)
    return mtls

def expand_item(material, reactions):
    qty, mtl = material
    qty2, mtls = reactions[mtl]
    return [(math.ceil(qty/qty2)*q, m) for q, m in mtls]

def combine(items):
    if len(items) < 2:
        return items
    counts = {}
    for qty, mtl in items:
        if mtl not in counts:
            counts[mtl] = 0
        counts[mtl] += qty
    new_items = []
    for mtl in counts:
        new_items.append((counts[mtl], mtl))
    return new_items

def main():
    reactions = get_reactions(sys.stdin.readlines())
    #print(reactions)
    depths = get_depths(reactions, 'ORE')
    #print(depths)
    results = expand(reactions, (1, 'FUEL'), depths)
    #print(results)
    qty_ore = results[0][0]
    print("Part 1: {0}".format(qty_ore))

if __name__ == '__main__':
    main()

