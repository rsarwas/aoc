# Data Model:
# ===========
# A circular doubly-linked list, with a pointer to a "current" node
# A dict of the total score for any elf with a non-zero score

import collections  # for defaultdict

class Node:
    val = None
    prev = None
    next = None

    def __init__(self, v, p=None, n=None):
        self.val = v
        self.prev = p
        self.next = n

class CircleList:
    current = None
    def __init__(self):
        zero = Node(0)
        one = Node(1, zero, zero)
        zero.prev, zero.next = one, one
        self.current = one

    def print(self):
        if self.current is None:
            print("[]")
            return
        ptr = self.current
        print("[", end="")
        print(ptr.val, end=",")
        ptr = ptr.next
        while ptr != self.current:
            print(ptr.val, end=",")
            ptr = ptr.next
        print("]")

    def add(self, v):
        if v % 23 == 0:
            return self.give_points(v)
        n = Node(v)
        before = self.current.next
        after = before.next
        n.prev = before
        n.next = after
        after.prev = n
        before.next = n
        self.current = n
        return 0
    
    def give_points(self, v):
        pts = v
        pts += self.remove_minus7()
        return pts

    def remove_minus7(self):
        # remove the marble 7 before current,
        # reset current to marble after removed marble
        # return value of removed marble
        minus7 = self.current.prev.prev.prev.prev.prev.prev.prev
        before = minus7.prev
        after = minus7.next
        before.next = after
        after.prev = before
        self.current = after
        return minus7.val

def part1(number_players, last_marble):
    c = CircleList()
    # 0 and 1 are already in the CircleList, so this will fail in the trivial case of 1,1)
    scores = collections.defaultdict(int)
    for m in range(2,last_marble+1):
        score = c.add(m)
        if score:
            elf = 1 + m % number_players
            scores[elf] += score
    winning = 0
    for v in scores.values():
        if v > winning: winning = v
    return winning

if __name__ == '__main__':
    # print(f"Test 1: {part1(9, 25)} =? 32")
    # print(f"Test 2: {part1(10, 1618)} =? 8317")
    # print(f"Test 2: {part1(13, 7999)} =? 146373")
    # print(f"Test 2: {part1(17, 1104)} =? 2764")
    # print(f"Test 2: {part1(21, 6111)} =? 54718")
    # print(f"Test 2: {part1(30, 5807)} =? 37305")
    print(f"Part 1: {part1(405, 71700)}")
    print(f"Part 2: {part1(405, 7170000)}")
