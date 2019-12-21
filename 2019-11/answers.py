import sys
from computer import Computer

class Robot:

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    BLACK = 0
    WHITE = 1

    TURN_CCW = 0
    TURN_CW = 1

    def __init__(self, intcode):
        self.__code = list(intcode) # make a private copy
        self.__painted_panels = {}
        self.__current_location = (0,0)  # (X,Y), X grows to the right, Y grows down
        self.__heading = self.UP

    def estimate(self):
        self.__run(self.BLACK)
        return len(self.__painted_panels)
    
    def paint(self):
        self.__run(self.WHITE)
        return self.__painted_panels
    
    def __run(self, start_panel_color):
        c = Computer(self.__code)
        c.push_input(start_panel_color)
        c.start()
        done = False
        while not done:
            move_cmd = c.pop_output()
            paint_cmd = c.pop_output()
            if move_cmd is None or paint_cmd is None:
                done = True
            else:
                self.__painted_panels[self.__current_location] = paint_cmd
                self.__move(move_cmd)
                this_panel_color = self.BLACK # default
                if self.__current_location in self.__painted_panels:
                    this_panel_color = self.__painted_panels[self.__current_location]
                c.push_input(this_panel_color)
                status = c.resume()
                done = status == Computer.done

    def __move(self, cmd):
        # The headings are integral (0..4) increasing clockwise
        # Turn
        if cmd == self.TURN_CW:
            self.__heading = (self.__heading + 1) % 4
        elif cmd == self.TURN_CCW:
            # +3 is the same as -1, but the math is easier
            self.__heading = (self.__heading + 3) % 4
        else:
            print("Unexpected value of move command", cmd)
            raise NotImplementedError
        # Move
        if self.__heading == self.UP:
            self.__current_location = (self.__current_location[0], self.__current_location[1] - 1)
        elif self.__heading == self.RIGHT:
            self.__current_location = (self.__current_location[0] + 1, self.__current_location[1])
        elif self.__heading == self.LEFT:
            self.__current_location = (self.__current_location[0] - 1, self.__current_location[1])
        elif self.__heading == self.DOWN:
            self.__current_location = (self.__current_location[0], self.__current_location[1] + 1)
        else:
            print("Unexpected heading", )
            raise NotImplementedError

def get_estimate(code):
    r = Robot(code)
    return r.estimate()
    
def registration(code):
    r = Robot(code)
    panels = r.paint()
    return format(panels)

def format(panels):
    # build a matrix of text '#' for white, and ' ' for black
    # find range of panel locations (number of rows/lines and columns/characters)
    minx, miny, maxx, maxy = 0,0,0,0
    for key in panels:
        minx = min(key[0], minx)
        miny = min(key[1], miny)
        maxx = max(key[0], maxx)
        maxy = max(key[1], maxy)
    nchar = 1 + maxx - minx
    nlines = 1 + maxy - miny
    print ('lines x chars', nlines, nchar)
    # set it all to black
    list_matrix = [list(' '*nchar) for _ in range(nlines)]
    # paint the white panels
    for key in panels:
        if panels[key] == Robot.WHITE:
            list_matrix[key[1]-miny][key[0]-minx] = '#'
    char_matrix = [''.join(l) for l in list_matrix]
    return char_matrix
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = get_estimate(program)
    print("Part 1: {0}".format(answer))
    answer = registration(program)
    print("Part 2:")
    for line in answer:
        print(line)
