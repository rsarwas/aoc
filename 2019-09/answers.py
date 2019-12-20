import sys
from computer import Computer

def test(code):
    c = Computer(code)
    c.start()
    out = c.pop_output()
    diagnostic_code = out
    while out is not None:
        diagnostic_code = out
        print(diagnostic_code)
        out = c.pop_output()
    return diagnostic_code
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    boost_keycode = test(program)
    print("Part 1: {0}".format(boost_keycode))
