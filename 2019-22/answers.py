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

def deal_into_new_stack(index, num_cards):
    """
    Top card (0) goes to on bottom (num_cards-1).
    next card (1) goes on top of the new bottom card (num_cards-2)
    """
    last = num_cards - 1
    return last - index

def deal_with_increment_n(n, index, num_cards):
    """
    To deal with increment N, start by clearing enough space on your table to lay out all of
    the cards individually in a long line. Deal the top card into the leftmost position. Then,
    move N positions to the right and deal the next card there. If you would move into a
    position past the end of the space on your table, wrap around and keep counting from the
    leftmost card again. Continue this process until you run out of cards.
    """
    return (index * n) % num_cards

def cut_n_cards(n, index, num_cards):
    """
    Move top (first) n cards to bottom (end) of the stack
    If n is negative moves from bottom to top
    """
    if n < 0:
        n = num_cards + n
    if index < n:
        return num_cards - n + index
    return index - n

def find_card(starting_index, num_cards, shuffle_commands):
    """
    Apply all the suffling commands to the card at the starting index,
    and return the ending index of the card.
    Simpler alternative to the list manipulation that worked for part 1
    """
    index = starting_index
    for cmd, arg in shuffle_commands:
        if cmd == DEAL_NEW:
            index = deal_into_new_stack(index, num_cards)
        elif cmd == DEAL_INC:
            index = deal_with_increment_n(arg, index, num_cards)
        elif cmd == CUT:
            index = cut_n_cards(arg, index, num_cards)
        else:
            raise NotImplementedError("Command: {0}, not understood".format(cmd))
    return index

def find_card_part2(starting_index, num_cards, shuffle_commands, loops):
    """
    find the index of the starting card after applying the shuffle commands 'loops' times.
    Since iterations can be a very large number, I am hoping that I will find a repeating pattern,
    within a few (< 1,000,000) iterations.  Once I know the cycle size, I can take the index
    at iterations modulo cycle_size

    FAILED to find a pattern after 1,000,000 iterations (more than the 15 second estimate)
    """
    iteration = {} # keep track of the iteration at which this solution was found
    max_loops = 20
    index = starting_index
    iteration[index] = 0
    for i in range(1, loops):
        index = find_card(index, num_cards, shuffle_commands)
        print(index)
        if index in iteration:
            other = iteration[index]
            print("found index {0} at try # {1} and {2}".format(index, other, i))
            break
        iteration[index] = i
        if i == max_loops:
            msg = "Could not find a repeating pattern after {0} iterations".format(max_loops)
            raise OverflowError(msg)
    return index

def main():
    """Solve the puzzle"""
    shuffle_commands = sys.stdin.readlines()
    cmd_list = list(parse(shuffle_commands))  # save time when iterating (part 2)
    number_of_cards = 10007  # 10 for tests, 10007 for part 1, 119315717514047 for part 2
    card_to_find = 2019      # 3 for testing, 2019 for part 1, 2020 for for part 2
    location = find_card(card_to_find, number_of_cards, cmd_list)
    print("Part 1: {0}".format(location))  # 3074
    number_of_cards = 119315717514047
    card_to_find = 2020
    iterations = 101741582076661
    location = find_card_part2(card_to_find, number_of_cards, cmd_list, iterations)
    print("Part 2: {0}".format(location))

if __name__ == '__main__':
    main()
