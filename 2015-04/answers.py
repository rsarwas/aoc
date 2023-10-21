# Data Model:
# ===========

import hashlib

def part1(key):
    i = 0
    while True:
        test = key + bytes(str(i), 'utf-8')
        hash = hashlib.md5(test).hexdigest()
        if hash[:5] == '00000':
            return i
        i += 1
    return -1

def part2(line):
    i = 254575 # start at solution to part 1
    while True:
        test = key + bytes(str(i), 'utf-8')
        hash = hashlib.md5(test).hexdigest()
        if hash[:6] == '000000':
            return i
        i += 1
    return -1




if __name__ == '__main__':
    # print(f"test 1a: {part1(b'abcdef')} == 609043")
    # print(f"test 1b: {part1(b'pqrstuv')} == 1048970")
    key = b'bgvyzdsv'
    print(f"Part 1: {part1(key)}")
    print(f"Part 2: {part2(key)}")
