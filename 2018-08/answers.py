# Data Model:
# ===========
# data is small integers separated by spaces; it appears to be {0..99}
# 

def part1(data):
    tree = parse(data)
    metadata, end = read_all_metadata(tree, 0)
    if end != len(tree):
        print("PANIC, unread data at end of tree")
    return sum(metadata)

def part2(data):
    tree = parse(data)
    value, end = node_value(tree, 0)
    if end != len(tree):
        print("PANIC, unread data at end of tree")
    return value

def parse(data):
    return [int(n) for n in data.split(" ")]

def read_all_metadata(tree,start):
    metadata = []
    node_count = tree[start]    
    metadata_count = tree[start+1]
    # print("start", start, "nodes", node_count, "metas", metadata_count)
    start += 2
    for n in range(0,node_count):
        node_meta, start = read_all_metadata(tree, start)
        # print("  node",n, node_meta)
        metadata += node_meta
    end = start + metadata_count
    my_metadata = tree[start:end]
    # print("My metadata", my_metadata)
    metadata += my_metadata
    # print("All metadata", metadata)
    return metadata,end

def node_value(tree, start):
    sub_nodes = [] # a list of lists; the index is the child node, the list is it's metadata value
    node_count = tree[start]    
    metadata_count = tree[start+1]
    # print("start", start, "nodes", node_count, "metas", metadata_count)
    start += 2
    for n in range(0,node_count):
        value, start = node_value(tree, start)
        sub_nodes.append(value)
        # print("  node value",n, value)
    end = start + metadata_count
    my_metadata = tree[start:end]
    # print("My metadata", my_metadata)
    # print("sub nodes", sub_nodes)

    # determine value
    value = 0
    if node_count == 0:
        value = sum(my_metadata)
    else:
        for i in my_metadata:
            index = i - 1  # our list is zero based
            if index < 0 or index > len(sub_nodes) - 1:
                continue
            value += sub_nodes[index]
    # print("Value", value)
    return value, end

if __name__ == '__main__':
    # data = open("test.txt").read() # as one big string
    data = open("input.txt").read() # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
