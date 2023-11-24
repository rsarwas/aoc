# Data Model:
# ===========
# data is hexadecimal string (possibly with an "\n" termination.
# it is binary data that contains packets of packets
# to read the packets and the payloads, I need to read a fixed
# number of bits at a given bit position. i.e. bits 0,1,2 are
# the main packet version number and bits 3,4,5 are the ID
# sub-packets and their payload do not align on byte or word
# boundaries. representing the data as a byte array will be
# most memory efficient, but building the bit masks will be
# tricky. converting the hex string to a "binary string" will
# convert each character to 4 characters.  The 1400 byte input
# will still only be a 5600 character array, with a "0" or a "1"
# at each index.  This will make it much easier to manage the
# current bit pointer and to take non-aligned slices of bits.

# a packet is a tuple (version, type, payload)
# version and type are 3 bit ints
# payload is an integer (type == 4), or a list of subpackets (type != 4)
# The sub packets may have nested sub packets, and so on ...)

import math  # for prod (product of list elements)

HEX = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def part1(data):
    bits = parse(data)
    packet, i = read_packet(bits, 0)
    total = totalize_versions(packet)
    return total


def part2(data):
    bits = parse(data)
    packet, i = read_packet(bits, 0)
    result = evaluate(packet)
    return result


def parse(data):
    bits = [HEX[c] for c in data.strip()]
    return "".join(bits)


def read_packet(bits, i):
    # return a packet, and the index after the packet
    packet_id, i = read_id(bits, i)
    packet_type, i = read_type(bits, i)
    payload = None
    if packet_type == 4:
        payload, i = read_literal(bits, i)
    else:
        payload, i = read_packets(bits, i)
    packet = (packet_id, packet_type, payload)
    return packet, i


def read_packets(bits, i):
    # return a list of packets starting at bit i
    # and the index after the last packet (padded to mod 4)
    length_type_id = bits[i]
    i += 1
    if length_type_id == "0":
        # next 15 bits is the total bit LENGTH of the sub packets (NUMBER is unknown)
        length = read_int(bits, i, 15)
        i += 15
        return read_len_packets(bits, i, length)
    else:  # length_type_id == "1"
        # next 11 bits is the NUMBER of the sub packets (total bit LENGTH is unknown)
        num = read_int(bits, i, 11)
        i += 11
        return read_n_packets(bits, i, num)


def read_len_packets(bits, i, l):
    # return a list of packet within the n bits starting at i
    # and the index after the last packet (padded to mod 4)
    end = i + l
    packets = []
    while i < end:
        packet, i = read_packet(bits, i)
        packets.append(packet)
    return packets, i


def read_n_packets(bits, i, n):
    # return a list of n packet starting at i
    # and the index after the last packet (padded to mod 4)
    packets = []
    for _ in range(0, n):
        packet, i = read_packet(bits, i)
        packets.append(packet)
    return packets, i


def read_id(bits, i):
    return read_int(bits, i, 3), i + 3


def read_type(bits, i):
    return read_int(bits, i, 3), i + 3


def read_length(bits, i):
    size = 11 if bits[i] == "1" else 15
    length = read_int(bits, i + 1, size)
    return length, i + 1 + size


def read_literal(bits, i):
    # groups of 5 xnnnn: if x = 0 this is the last group
    # the nnnn groups are concatenated and converted to an int
    # there may be "0" after the last group in a literal type packet
    # so that the next packet starts with a hex character
    # returns the index after the end of the last group
    groups = []
    done = False
    while not done:
        if bits[i] == "0":
            done = True
        groups.append(bits[i + 1 : i + 5])
        i += 5
    return int("".join(groups), base=2), i


def read_int(bits, i, n):
    return int(bits[i : i + n], base=2)


def totalize_versions(packet):
    (p_id, p_type, payload) = packet
    total = p_id
    if p_type != 4:
        for sub_packet in payload:
            total += totalize_versions(sub_packet)
    return total


def evaluate(packet):
    (_, p_type, payload) = packet
    if p_type == 0:  # sum
        return sum([evaluate(p) for p in payload])
    elif p_type == 1:  # product
        return math.prod([evaluate(p) for p in payload])
    elif p_type == 2:  # minimum
        return min(([evaluate(p) for p in payload]))
    elif p_type == 3:  # maximum
        return max(([evaluate(p) for p in payload]))
    elif p_type == 4:  # literal
        return payload
    elif p_type == 5:  # greater than
        gt = evaluate(payload[0]) > evaluate(payload[1])
        return 1 if gt else 0
    elif p_type == 6:  # less than
        lt = evaluate(payload[0]) < evaluate(payload[1])
        return 1 if lt else 0
    elif p_type == 7:  # equal to
        equal = evaluate(payload[0]) == evaluate(payload[1])
        return 1 if equal else 0
    else:
        print("Aak, an unexpected packet type", p_type)


if __name__ == "__main__":
    # tests part 1
    # print(read_packet(parse("D2FE28"), 0))
    # print(read_packet(parse("38006F45291200"), 0))
    # print(read_packet(parse("EE00D40C823060"), 0))
    # print(part1("8A004A801A8002F478") == 16)
    # print(part1("620080001611562C8802118E34") == 12)
    # print(part1("C0015000016115A2E0802F182340") == 23)
    # print(part1("A0016C880162017C3686B18A3D4780") == 31)

    # test part 2
    # print(part2("C200B40A82") == 3)
    # print(part2("04005AC33890") == 54)
    # print(part2("880086C3E88112") == 7)
    # print(part2("CE00C43D881120") == 9)
    # print(part2("D8005AC2A8F0") == 1)
    # print(part2("F600BC2D8F") == 0)
    # print(part2("9C005AC2F8F0") == 0)
    # print(part2("9C0141080250320F1802104A08") == 1)

    # puzzle data
    data = open("input.txt").read()  # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
