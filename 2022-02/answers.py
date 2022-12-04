# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

# POINTS: 1 for Rock, 2 for Paper, and 3 for Scissors
# POINTS: 6 for Win, 3 for Draw, and 0 for Loss

# Column 1 = opponents play; A for Rock, B for Paper, and C for Scissors
# column 2 = my response; X for Rock, Y for Paper, and Z for Scissors

SCORE1 = {
    "A X": 4, # Rock Rock = Draw(3) + Rock(1)
    "A Y": 8, # Rock Paper = Win(6) + Paper(2)
    "A Z": 3, # Rock Scissors = Loss(0) + Scissors(3)
    "B X": 1, # Paper Rock = Loss(0) + Rock(1)
    "B Y": 5, # Paper Paper = Draw(3) + Paper(2)
    "B Z": 9, # Paper Scissors = Win(6) + Scissors(3)
    "C X": 7, # Scissors Rock = Win(6) + Rock(1)
    "C Y": 2, # Scissors Paper = Loss(0) + Paper(2)
    "C Z": 6  # Scissors Scissors = Draw(3) + Scissors(3)
}

# Column 1 = opponents play; A for Rock, B for Paper, and C for Scissors
# column 2 = outcome: X need to lose, Y need to tie, and Z need to win

SCORE2 = {
    "A X": 3, # Rock Loss = Loss(0) + Scissors(3)
    "A Y": 4, # Rock Draw = Draw(3) + Rock(1)
    "A Z": 8, # Rock Win = Win(6) + Paper(2)
    "B X": 1, # Paper Loss = Loss(0) + Rock(1)
    "B Y": 5, # Paper Draw = Draw(3) + Paper(2)
    "B Z": 9, # Paper Win = Win(6) + Scissors(3)
    "C X": 2, # Scissors Loss = Loss(0) + Paper(2)
    "C Y": 6, # Scissors Draw = Draw(3) + Scissors(3)
    "C Z": 7  # Scissors Win = Win(6) + Rock(1)
}

def part1(lines):
    total = 0
    for line in lines:
        line = line.strip()
        total += SCORE1[line]
    return total


def part2(lines):
    total = 0
    for line in lines:
        line = line.strip()
        total += SCORE2[line]
    return total


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
