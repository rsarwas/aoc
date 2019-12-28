import sys
from computer import Computer
class Droid:

    # Computer Input; Move instructions - all one space
    # Only four movement commands are understood: north (1), south (2), west (3), and east (4)
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    # Computer Output
    # The repair droid can reply with any of the following status codes:
    #   0: The repair droid hit a wall. Its position has not changed.
    #   1: The repair droid has moved one step in the requested direction.
    #   2: The repair droid has moved one step in the requested direction;
    #      its new position is the location of the oxygen system.
    WALL = 0
    OPEN = 1
    SENSOR = 2

    CHARS = ['#', '.', 'o']

    def __init__(self, intcode):
        self.__code = list(intcode) # make a private copy
        self.__computer = Computer(self.__code)
        self.__start = (0, 0)  # (x,y); x grows to the East (right); y grows South (down)
        self.__map = {self.__start: Droid.OPEN}   # dict key: x,y tuples; value: Computer output
        self.__path = []  # list of x,y tuples;
        self.__current_location = self.__start
        self.__sensor = None
        self.__stop_at_sensor = False
        self.__stop = False

    def explore_all(self):
        """ Recursively explores all squares """
        self.__computer.start()  # It will pause immediately waiting for input
        self.__move()

    def find_sensor(self):
        """ Returns location and path to oxygen sensor """
        self.__stop_at_sensor = True
        self.__computer.start()  # It will pause immediately waiting for input
        self.__move()
        return self.__sensor, self.__path

    def open_tiles(self):
        """ Return a list of open tiles found so far """
        for coord in self.__map:
            if self.__map[coord] == Droid.OPEN:
                yield coord

    def print_map(self):
        """ Prints an ASCII map of the area explord so far """
        for line in self.__format_map():
            print(line)

    def __move(self):
        if self.__sensor is not None and self.__stop_at_sensor:
            self.__stop = True
            return
        moves = self.__get_moves()
        for direction, target in moves:
            if target in self.__map:
                # skip already explored tiles
                continue
            self.__computer.push_input(direction)
            status = self.__computer.resume()
            if status == Computer.DONE:
                # This should never happen
                print('Oh No!  The computer halted')
                self.__stop = True
                return
            response = self.__computer.pop_output()
            self.__map[target] = response
            if response == Droid.SENSOR:
                self.__sensor = target
            if response == Droid.OPEN or response == Droid.SENSOR:
                self.__path.append(self.__current_location)
                self.__current_location = target
                self.__move()
                # When we return from a nested move, we may be done.
                # if so, skip other directions.
                if self.__stop:
                    return
        # There are no more directions to go at this location
        if len(self.__path) == 0:
            # This is either a very small maze,
            # or we have have backtracked to the start and explored all options.
            return
        else:
            # backup and continue
            self.__backup()
            return

    def __get_moves(self):
        # WARNING: if there are multiple paths to the target, the order of
        #          the moves will make a difference.
        #          I tested a few, and always got the same results, so I think I'm OK.
        x, y = self.__current_location
        moves = [
            (Droid.SOUTH, (x, y+1)),
            (Droid.NORTH, (x, y-1)),
            (Droid.WEST, (x-1, y)),
            (Droid.EAST, (x+1, y)),
        ]
        return moves

    def __backup(self):
        # Adjust path and other internal state, and __MOVE__ the droid!!
        c_x, c_y = self.__current_location
        previous = self.__path.pop()
        p_x, p_y = previous
        direction = Droid.NORTH # Assume, then correct
        if c_x > p_x:
            direction = Droid.WEST
        if c_x < p_x:
            direction = Droid.EAST
        if c_y < p_y:
            direction = Droid.SOUTH
        self.__computer.push_input(direction)
        self.__computer.resume()
        self.__computer.pop_output()
        self.__current_location = previous

    def __format_map(self):
        minx, miny, maxx, maxy = self.__get_extents()
        ncols, nlines = 1+ maxx - minx, 1 + maxy - miny
        list_matrix = [list(' '*ncols) for _ in range(nlines)]
        for x, y in self.__map:
            row = y - miny
            col = x - minx
            list_matrix[row][col] = Droid.CHARS[self.__map[(x, y)]]
        # Start Location
        row = 0 - miny
        col = 0 - minx
        list_matrix[row][col] = 'X'
        # Droid Location
        row = self.__current_location[1] - miny
        col = self.__current_location[0] - minx
        list_matrix[row][col] = 'D'
        char_matrix = [''.join(l) for l in list_matrix]
        return char_matrix

    def __get_extents(self):
        minx, miny, maxx, maxy = 0, 0, 0, 0
        for x, y in self.__map:
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)
        return minx, miny, maxx, maxy

def show_map(intcode):
    droid = Droid(intcode)
    droid.explore_all()
    droid.print_map()

def distance_to_sensor(intcode):
    droid = Droid(intcode)
    _, path = droid.find_sensor()
    return len(path)

def time_to_fill(intcode):
    """
    Brute force solution
    Oxygen fills oxygen location in 1 minute
    if there are no more open squares, return minute count
    otherwise fill all open spaces adjacent to oxygen locations, increment time count and repeat
    """
    def adjacent(tile1, tile2):
        x1, y1 = tile1
        x2, y2 = tile2
        return (x1 == x2 and abs(y2 - y1) == 1) or (y1 == y2 and abs(x2 - x1) == 1)

    def find_open_adjacent_to_filled(open_tiles, filled_tiles):
        for tile1 in open_tiles:
            for tile2 in filled_tiles:
                if adjacent(tile1, tile2):
                    yield tile1

    droid = Droid(intcode)
    droid.explore_all()
    location, _ = droid.find_sensor()
    open_tiles = list(droid.open_tiles())
    # Test data
    # location = (1,2)
    # open_tiles = [(0,0), (1,0), (0,1), (2,1), (3,1), (0,2), (2,2)]
    filled_tiles = [location]
    # Initially (time = 0), the only location which contains oxygen is the location
    # of the repaired oxygen system
    time = 0
    while len(open_tiles) > 0:
        time += 1
        for tile in list(find_open_adjacent_to_filled(open_tiles, filled_tiles)):
            open_tiles.remove(tile)
            filled_tiles.append(tile)
    return time

def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    # show_map(program)
    answer = distance_to_sensor(program)
    print("Part 1: {0}".format(answer))
    answer = time_to_fill(program)
    print("Part 2: {0}".format(answer))

if __name__ == '__main__':
    main()
