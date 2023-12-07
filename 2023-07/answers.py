"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

from functools import cmp_to_key

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    hands = parse(lines)
    # print(hands)
    hands = [convert_hand(hand) for hand in hands]
    # print(hands)
    hands = sorted(hands, key=cmp_to_key(compare_hands))
    # print(hands)
    total = 0
    for i, (_, bid) in enumerate(hands):
        total += (i + 1) * bid
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    hands = parse(lines)
    # print(hands)
    hands = [convert_hand_v2(hand) for hand in hands]
    # print(hands)
    hands = sorted(hands, key=cmp_to_key(compare_hands_v2))
    # print(hands)
    total = 0
    for i, (_, bid) in enumerate(hands):
        total += (i + 1) * bid
    return total


def parse(lines):
    """Convert the lines into a list of (hand, bid) tuples"""
    data = [line.strip().split() for line in lines]
    data = [(hand, int(bid)) for (hand, bid) in data]
    return data


def convert_hand(hand):
    """Converts a hand into a string that will sort correctly"""
    old = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    new = ["m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a"]
    cards, bid = hand
    for o, n in zip(old, new):
        cards = cards.replace(o, n)
    return (cards, bid)


def convert_hand_v2(hand):
    """Converts a hand into a string that will sort correctly; J = joker not Jacks"""
    old = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    new = ["m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a"]
    cards, bid = hand
    for o, n in zip(old, new):
        cards = cards.replace(o, n)
    return (cards, bid)


def compare_hands(hand1, hand2):
    """If it returns a positive number: h1 > h2
    If it returns 0: x == y
    If it returns a negative number: h1 < h2"""
    h1, _ = hand1
    h2, _ = hand2
    r1 = rank5(h1)
    r2 = rank5(h2)
    if r1 == r2:
        return (h1 > h2) - (h1 < h2)
    if r1 < r2:
        return -1
    return 1


def compare_hands_v2(hand1, hand2):
    """If it returns a positive number: h1 > h2
    If it returns 0: x == y
    If it returns a negative number: h1 < h2"""
    h1, _ = hand1
    h2, _ = hand2
    r1 = rank_v2(h1)
    r2 = rank_v2(h2)
    if r1 == r2:
        return (h1 > h2) - (h1 < h2)
    if r1 < r2:
        return -1
    return 1


# pylint: disable=too-many-return-statements
def rank5(hand):
    """0 = high card, 1 = one pair, 2 = two pair, 3 = 3 of a kind,
    4 = full house, 5 = four of a kind, 6 = five of a kind"""
    hand = sorted(hand)
    # carts are in order, so matching cards are adjacent
    if hand[0] == hand[4]:
        # 5 of a kind
        return 6
    if hand[0] == hand[3] or hand[1] == hand[4]:
        # 4 of a kind
        return 5
    if hand[0] == hand[2]:
        if hand[3] == hand[4]:
            # full house
            return 4
        # three of a kind
        return 3
    if hand[1] == hand[3]:
        # three of a kind
        return 3
    if hand[2] == hand[4]:
        if hand[0] == hand[1]:
            # full house
            return 4
        # three of a kind
        return 3
    if hand[0] == hand[1]:
        if hand[2] == hand[3] or hand[3] == hand[4]:
            # two pair
            return 2
        # one pair
        return 1
    if hand[1] == hand[2]:
        if hand[3] == hand[4]:
            # two pair
            return 2
        # one pair
        return 1
    if hand[2] == hand[3] or hand[3] == hand[4]:
        # one pair
        return 1
    # High Card
    return 0


# pylint: disable=inconsistent-return-statements
def rank_v2(hand):
    """Remove the Jokers ("a") and rank the smaller hand,
    then return the highest rank with the jokers"""
    hand = hand.replace("a", "")
    if len(hand) <= 1:
        # 4 or 5 jokers makes 5 of a kind
        return 6
    if len(hand) == 2:
        if hand[0] == hand[1]:
            return 6  # a pair + 3 jokers = 5 of a kind
        return 5  # 4 of kind
    if len(hand) == 3:
        return rank3(hand)
    if len(hand) == 4:
        return rank4(hand)
    if len(hand) == 5:
        return rank5(hand)


def rank3(hand):
    """rank 3 cards (2 other cards are wild)"""
    hand = sorted(hand)
    # carts are in order, so matching cards are adjacent
    if hand[0] == hand[2]:
        # 3 of a kind => 5 of a kind
        return 6
    if hand[0] == hand[1] or hand[1] == hand[2]:
        # pair => 4 of a kind
        return 5
    # High Card => 3 of a kind
    return 3


# pylint: disable=too-many-return-statements
def rank4(hand):
    """rank 4 cards (1 other card is wild)
    1 = one pair, 2 = two pair, 3 = 3 of a kind,
    4 = full house, 5 = four of a kind, 6 = five of a kind"""
    hand = sorted(hand)
    # carts are in order, so matching cards are adjacent
    if hand[0] == hand[3]:
        # 4 of a kind => 5 of a kind
        return 6
    if hand[0] == hand[2] or hand[1] == hand[3]:
        # 3 of a kind => 4 of a kind
        return 5
    if hand[0] == hand[1]:
        if hand[2] == hand[3]:
            # 2 pair => full house
            return 4
        # pair => three of a kind
        return 3
    if hand[1] == hand[2]:
        # 0 cannot equal 3
        # three of a kind
        return 3
    if hand[2] == hand[3]:
        if hand[0] == hand[1]:
            # 2 pair => full house
            return 4
        # pair => three of a kind
        return 3
    # High Card => 1 pair
    return 1


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
