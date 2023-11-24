"""
Advent of Code 2019 day 24
See https://adventofcode.com/2019/day/24 for the problem description
"""

import sys


class Life:
    BUG = "#"
    EMPTY = "."

    def __init__(self, rows, columns):
        self.__r = rows
        self.__c = columns
        self.__state = 0

    def set_as_int(self, val):
        self.__state = val

    def get_as_int(self):
        return self.__state

    def set_with_text(self, lines):
        self.__state = 0
        for row, line in enumerate(lines):
            for col, cell in enumerate(line):
                if cell == Life.BUG:
                    index = row * self.__c + col
                    self.__state |= 1 << index

    def get_as_text(self):
        lines = []
        for row in range(self.__r):
            line = ""
            for col in range(self.__c):
                line += Life.EMPTY if self.__is_empty(row, col) else Life.BUG
            lines.append(line)
        return lines

    def update(self):
        new_state = 0
        for row in range(self.__r):
            for col in range(self.__c):
                if self.__bug_at(row, col):
                    index = row * self.__c + col
                    new_state |= 1 << index
        self.__state = new_state

    def __is_empty(self, row, col):
        """
        Tiles on the edges of the grid have fewer than four adjacent tiles;
        the missing tiles count as empty space.
        """
        if row < 0 or col < 0 or row >= self.__r or col >= self.__c:
            return True
        index = row * self.__c + col
        val = 1 << index
        return self.__state & val != val

    def __count_adjacent_bugs(self, row, col):
        count = 4
        if self.__is_empty(row - 1, col):
            count -= 1
        if self.__is_empty(row + 1, col):
            count -= 1
        if self.__is_empty(row, col - 1):
            count -= 1
        if self.__is_empty(row, col + 1):
            count -= 1
        return count

    def __bug_at(self, row, col):
        """
        * A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        * An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        """
        empty = self.__is_empty(row, col)
        bug_count = self.__count_adjacent_bugs(row, col)
        if empty:
            return bug_count == 1 or bug_count == 2
        else:
            return bug_count == 1


def test():
    board = sys.stdin.readlines()
    life = Life(5, 5)
    life.set_with_text(board)
    for line in life.get_as_text():
        print(line)
    for _ in [1, 2, 3, 4]:
        life.update()
        print()
        for line in life.get_as_text():
            print(line)


def main():
    """Solve the puzzle"""
    board = sys.stdin.readlines()
    life = Life(5, 5)
    life.set_with_text(board)
    biodiversity_index = life.get_as_int()
    layouts = set([])
    while biodiversity_index not in layouts:
        layouts.add(biodiversity_index)
        life.update()
        biodiversity_index = life.get_as_int()
    print("Part 1: {0}".format(biodiversity_index))


if __name__ == "__main__":
    main()
