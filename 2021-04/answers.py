
# Data Model:
# ===========
# numbers is a list of integers; the numbers drawn in order playing bingo
# boards is a list of boards
# A board is a 5x5 matrix (list of lists) where
# each element is a tuple (number, marked: Bool)
# all elements start with marked = false, and are switched to True
# when the number is called

def part1(lines):
    numbers, boards = parse(lines)
    # find the score of the first board to win
    score = play_bingo(numbers, boards)
    return score

def part2(lines):
    numbers, boards = parse(lines)
    # find the score of the last board to win
    score = lose_bingo(numbers, boards)
    return score

def parse(lines):
    boards = []
    numbers = [int(num) for num in lines[0].split(",")]
    board_line = 0
    board = []
    for line in lines[2:]:
        if len(line) < 10: continue
        board_line += 1
        row = [(int(n), False) for n in line.strip().replace("  "," ").split(" ")]
        board.append(row)
        if board_line == 5:
            boards.append(board)
            board_line = 0
            board = []
    return numbers, boards

def lose_bingo(numbers, boards):
    # Keep a set of indexes for the boards that are still in play (have not won)
    remaining_boards = set(range(0,len(boards)))
    for i, num in enumerate(numbers):
        for bi, board in enumerate(boards):
            if bi not in remaining_boards: continue
            if check(board, num):
                # skip winning check for first 4 numbers (not possible to win with < 5)
                if i > 4 and is_winning(board):
                    remaining_boards.remove(bi)
                    if len(remaining_boards) == 0:
                        return num * score(boards[bi])
    return 0

def play_bingo(numbers, boards):
    for i, num in enumerate(numbers):
        for board in boards:
            if check(board, num):
                # skip winning check for first 4 numbers (not possible to win with < 5)
                if i > 4 and is_winning(board):
                    return num * score(board)
    return 0

def check(board, num):
    for row in range(0,5):
        for col in range(0,5):
            cell = board[row][col]
            if cell[0] == num:
                board[row][col] = (num, True)
                return True
    return False

def is_winning(board):
    for row in range(0,5):
        winning = board[row][0][1] and board[row][1][1] and board[row][2][1] and board[row][3][1] and board[row][4][1]
        if winning: return True
    for col in range(0,5):
        winning = board[0][col][1] and board[1][col][1] and board[2][col][1] and board[3][col][1] and board[4][col][1]
        if winning: return True

def score(board):
    # sum of all unmarked numbers
    score = 0
    for row in range(0,5):
        for col in range(0,5):
            cell = board[row][col]
            if not cell[1]: score += cell[0]
    return score

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
