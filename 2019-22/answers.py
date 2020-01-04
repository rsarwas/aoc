"""
Advent of Code 2019 day 22
See https://adventofcode.com/2019/day/22 for the problem description
"""

import sys

# Shuffle commands
DEAL_NEW = 0  # deal into new stack
DEAL_INC = 1  # deal with increment n
CUT = 2       # cut n

def parse(cmd_lines):
    """ Reads a line of text and turns it into a suffle command and an optional argument"""
    for line in cmd_lines:
        parts = line.split()
        if parts[0] == 'cut':
            yield CUT, int(parts[1])
        elif parts[0] == 'deal':
            if parts[1] == 'into':
                yield DEAL_NEW, None
            elif parts[1] == 'with':
                yield DEAL_INC, int(parts[3])
            else:
                print('unexpected deal command', line)
                yield None, None
        else:
            print('unexpected command', line)
            yield None, None

def deal_into_new_stack(cards):
    """ Put top card on bottom of new stack, repeat for all cards"""
    cards.reverse()
    return cards

def deal_with_increment_n(cards, n):
    """
    To deal with increment N, start by clearing enough space on your table to lay out all of the cards
    individually in a long line. Deal the top card into the leftmost position. Then, move N positions
    to the right and deal the next card there. If you would move into a position past the end of the
    space on your table, wrap around and keep counting from the leftmost card again. Continue this process
    until you run out of cards.
    """
    size = len(cards)
    new_deck = [0] * size
    new_deck[0] = cards[0]
    position = 0
    for index, value in enumerate(cards[1:]):
        position += n
        new_index = position % size
        new_deck[new_index] = value
    return new_deck

def cut_n_cards(cards, n):
    """Move top (first) n cards to bottom (end) of the stack
       If n is negative moves from bottom to top
    """
    return cards[n:] + cards[:n]

def shuffle(cards, shuffle_commands):
    """Apply all the suffling commands to the deck of cards and return the cards"""
    for cmd, arg in parse(shuffle_commands):
        if cmd == DEAL_NEW:
            cards = deal_into_new_stack(cards)
        elif cmd == DEAL_INC:
            cards = deal_with_increment_n(cards, arg)
        elif cmd == CUT:
            cards = cut_n_cards(cards, arg)
        else:
            raise NotImplementedError("Command: {0}, not understood".format(cmd))
    return cards

def main():
    """Solve the puzzle"""
    shuffle_commands = sys.stdin.readlines()
    number_of_cards = 10007  # 10 for tests, 10007 for problem
    cards = list(range(number_of_cards))
        # Cards are numbered 0 to n-1 and are in factory order
        # that is increasing from top (front of list) to bottom (end)
    shuffled_cards = shuffle(cards, shuffle_commands)
    # for testing:
    # print(shuffled_cards)
    position2019 = shuffled_cards.index(2019)
    print("Part 1: {0}".format(position2019))

if __name__ == '__main__':
    main()
