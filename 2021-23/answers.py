# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

# Part1 was solved manually
# Input:

#############
#...........#
###D#D#B#A###
  #C#A#B#C#
  #########

# Problem: Move A's to first column, B to second, etc. with minimal cost.
# Cannot use the home columns (or the square above) as a temporary resting spot.
# It costs 1 unit to move A 1 square, B = 10, C = 100, D = 1000.

# Solution:
# Minimal moves are:  9+6 (or 7+8) for D = 15000
#                     6+7 (or 8+5) for C =  1300
#                     5+5          for B =   100
#                     6+8 (or 9+5) for A =    14  Total Minimal Score is 16414

# Move A, B and B out of the way

#############
#.B.B......A#
###D#D#.#.###
  #C#A#.#C#
  #########

# Move C and D home then move A out of the way

#############
#.B.B.....AA#
###D#.#.#.###
  #C#.#C#D#
  #########

# Move both B home, then D and then C

#############
#.........AA#
###.#B#C#D###
  #.#B#C#D#
  #########

# Move both A home

# One B had to move 3+3 extra moves and the other moved 1+1 extra move  +8*10 = +80
# One A moved 2+2 extra moves nd the other moved 5+5 extra moves  +14
# 16414 + 80 + 14 = 16508

# Part2 was solved manually
# Input:

#############
#...........#
###D#D#B#A###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#B#C#
  #########

# Solution:

# for reference, the temp squares and the letters are numbered as follows
#######################
#1 2 . 3 . 4 . 5 . 6 7#
####D-1#D-4#B-2#A-3####
   #D-2#C-2#B-3#A-4#
   #D-3#B-1#A-2#C-3#
   #C-1#A-1#B-4#C-4#
   #################
# the final are called f1 to f4, from top to bottom. For example C-4 is at D's f4 and D-4 is at B's f1
# Minimal moves are:  D4:9, D1:10, D2:10, D3:10 = 39 * 1000 = 39000
#                     C3:9, C4:9, C2:6, C1:9    = 33 *  100 =  3300
#                     B1:1, B2:6, B3:6, B4:7    = 20 *   10 =   200
#                     A1:10, A2:10, A3:9, A4:9  = 38 *    1 =    38  Total Minimal Score is 42538

# Solution:
#  A3 to 1 (9); A4 to 2 (9), C3 to 7 (500), C4 to 6 (500)             =  1_018
#  D4 to f4 (9k), D1 to f3 (10k), D2 to f2 (10k), D3 to f1 (10k)      = 39_000
#  C1 to 5 (900)                                                      =    900
#  A4@2 to f4 (5), A3@1 to f3 (5)                                     =     10
#  B2 to 1 (70), B3 to 2 (70), A2 to f2 (9), B4 to 4 (50)             =    199
#  C1@5 to f4 (500), C4@6 to f3 (600), C3@7 to f2 (600)               =  1_700
#  B4@4 to 5 (20), C2 to f1 (500)                                     =    520
#  B1 to 4 (40), A1 to f1 (7)                                         =     47
#  B3@2 to f4 (70), B2@1 to f3 (70), B1@4 to f2 (30), B4@5 to f1 (40) =    210
#                                                               Total = 43_604 (too low!!!)

# Solution:
#  A3 to 1 (9); A4 to 2 (9), C3 to 7 (500), C4 to 6 (500)               =  1_018
#  D4 to f4 (9k), D1 to f3 (10k), D2 to f2 (10k), D3 to f1 (10k)        = 39_000
#  C1 to 5 (900)                                                        =    900
#  A4@2 to f4 (5), A3@1 to f3 (5)                                       =     10
#  B2 to 1 (70), B3 to 2 (70), A2 to f2 (9), B4 to 3 (70)               =    219
#  C1@5 to f4 (500), C4@6 to f3 (600), C3@7 to f2 (600), C2 to f1 (500) =  2_200
#  B1 to 5 (60), A1 to 4 (5)                                            =     65
#  B4@3 to f4 (50), A1@4 (4)                                            =     54
#  B3@2 to f3 (60), B2@1 to f2 (60), B1@5 to f1 (40)                    =    160
#                                                                 Total = 43_626

def part1(lines):
    return 16508

def part2(lines):
    return -1

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
