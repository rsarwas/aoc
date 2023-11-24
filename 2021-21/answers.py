# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# Part 1 is trivial, read the problem statement and the code
# Part 2:
# after 1 roll there are 3 universe, after 2 rolls, 3^2 = 9; 3 rolls = 3^3 = 27 universes
# the rolls could be (1,1,1), (1,1,2), (1,1,3) , (1,2,1), ... (3,3,3) or 27 permutations
# the number of spaces moved after 3 rolls in 3,4,5; 5,6,7; 5,6,7; 4,5,6; 5,6,7, 6,7,8; 5,6,7; 6,7,8; 7,8,9
# that is number of spaces moved along with the probability is:
#  3 (1/27), 4 (4/27), 5 (6/27), 6 (7/27), 7 (6/27), 8 (3/27), and 9 (1/27)
# I will keep track of how many universes have a given score.
# The fastest game will be over in 3 turns for one of the players. For example the first turn lands on 8
# then 7, then 6 to get 21 points. There is no way for either player to win in only 2 turns.
# In the unluckiest universes, the first turn will land then on 1 or 4, then the next turn will land
# them on 4 or 1 respectively: in both cases they will need 9 turns to win
# (1+4) * 4 or (4+1) * 4 = 20 points in 8 turns, then next turn will ensure they win.
# There is no way that player1 will not have at least 21 points by the end of their 9th turn.
# Player 2 will never get a 9th turn.  We need to play at least 9+8 = 17 turns or 3*17 = 51 dice rolls
# creating 3^51 = 2_153_693_963_075_557_766_310_747 possible universes; however, each universe stops splitting
# once there is a winner, so there will be far less than that in the total (~10^15 in sample)
# I can keep track of how many universes exist for each score.  For example, assuming player 1 starts on
# square 1, after player1's first turn there is one universe with a score of (4,0) having rolled 1+1+1 in
# only one of 27 universes.  There are 3 with (5,0).  The full list is:
# 1x(4,0), 3x(5,0), 6x(6,0), 7x(7,0), 6x(8,0), 3x(9,0), and 1x(10,0)
# in player2's first turn, each of these universes split 27 times or 7 different possible player2 scores
# for each player 1 score 7*7 = 49 different scores combinations.  Assuming player2 also starts on square 1
# there is 1x1=1 universe with (4,4), 1x3 with (4,5), 1x6 w/ (4,6), ... 1x1 w/ (4,10)
#   3x1 (5,4), 3x3 (5,5), 3x6 (5,6), ... 3x1 (5,10)
#   .......7x7 (7,7)  .....
#   1x1 (10,4), 1x3 (10,5), 1x6 (10,6), .... 1x1 (10,10)
# during each turn the old list of scores is read and forgotten, and a new list of scores is remembered.
# the total of the scores that are winning after a turn are added to a totalizer for each player, and
# not remembered or used in future scenarios. All non-winning scores are updated and used in the next turn.
# We stop when there are no scores that need to be remembered for the next round.

# Unfortunately, it is not quite that simple, in order to figure the score for a turn, I need to know the
# current location as well as the current score.  It seems that the score and the location are tied together,
# for example player 1 starting at square 1 would have a score of 7 by moving from 1 to 4 then 8 (3+4) or by
# moving from 1 to 5 then 8 (4+3).  Since it seems that score and location will move together, it will not
# create a lot of different permutations, and it will save me the trouble of figuring out how to derive
# location from score and number of turns

import collections  # for defaultdict


def part1(lines):
    player1, player2 = parse(lines)
    score1, score2, rolls = play_to(1000, player1, player2)
    # print(score1, score2, rolls)
    low_score = min(score1, score2)
    return low_score * rolls


def part2(lines):
    player1, player2 = parse(lines)
    p1wins, p2wins = multiverse_play(21, player1, player2)
    # print(p1wins, p2wins)
    most_wins = max(p1wins, p2wins)
    return most_wins


def parse(lines):
    player1 = int(lines[0].replace("Player 1 starting position: ", ""))
    player2 = int(lines[1].replace("Player 2 starting position: ", ""))
    return player1, player2


BOARD_SIZE = 10


def play_to(goal, player1, player2):
    # locations/tiles are numbered 1 to 10, but I am using 0-9 internally to make modulo easier
    player1 -= 1
    player2 -= 1
    score1, score2 = (0, 0)
    dice = 0
    # print("player1: ", player1, dice, 0, score1)
    # print("player2: ", player2, dice, 0, score2)
    total_rolls = 0
    while True:
        dice, rolls = roll3times(dice)
        total_rolls += 3
        player1 = (player1 + rolls) % BOARD_SIZE
        score1 += player1 + 1
        if score1 >= 1000:
            return score1, score2, total_rolls
        # print("player1: ", player1, dice, rolls, score1)
        dice, rolls = roll3times(dice)
        total_rolls += 3
        player2 = (player2 + rolls) % BOARD_SIZE
        score2 += player2 + 1
        # print("player2: ", player2, dice, rolls, score2)
        if score2 >= 1000:
            return score1, score2, total_rolls

    return score1, score2


def roll3times(dice):
    total = 0
    for _ in range(3):
        dice += 1
        dice % 100
        total += dice
    return dice, total


def multiverse_play(goal, p1, p2):
    # total number of universes so far in which each player has won
    player1_wins = 0
    player2_wins = 0

    # In probs the key is the total of the rolls of a 3 sided die;
    # the value is the probability (number of times out of 27 that the total will occur)
    probs = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    # In scores the key is ((loc1, loc2), (score1, score2)) and the value is the
    # The number of universes that have this score.
    # start with 1 universe with the score 0 to 0
    scores = {((p1, p2), (0, 0)): 1}
    # we alternate players each time through the loop.
    player1_turn = True
    while scores:
        new_scores = collections.defaultdict(int)
        for k, v in scores.items():
            ((l1, l2), (s1, s2)) = k
            for r, n in probs.items():
                if player1_turn:
                    loc = (l1 + r) % BOARD_SIZE  # loc will be 0..9 (0 == tile 10)
                    score = s1 + (10 if loc == 0 else loc)
                    if score >= goal:
                        player1_wins += v * n
                    else:
                        new_scores[((loc, l2), (score, s2))] += v * n
                else:
                    loc = (l2 + r) % BOARD_SIZE  # loc will be 0..9 (0 == tile 10)
                    score = s2 + (10 if loc == 0 else loc)
                    if score >= goal:
                        player2_wins += v * n
                    else:
                        new_scores[((l1, loc), (s1, score))] += v * n
        scores = new_scores
        player1_turn = not player1_turn
    return player1_wins, player2_wins


if __name__ == "__main__":
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
