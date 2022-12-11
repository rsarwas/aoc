# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

def tf0(old):
    return old * 19
def tf1(old):
    return old + 6
def tf2(old):
    return old * old
def tf3(old):
    return old + 3
    
def f0(old):
    return old * 11
def f1(old):
    return old + 4
def f2(old):
    return old * old
def f3(old):
    return old + 2
def f4(old):
    return old + 3
def f5(old):
    return old + 1
def f6(old):
    return old + 5
def f7(old):
    return old * 19
    
TEST = [
{'items':[79, 98],
'op':tf0,
'divisor':23,
'throw':(2,3),
'inspections':0},

{'items':[54, 65, 75, 74],
'op':tf1,
'divisor':19,
'throw':(2,0),
'inspections':0},

{'items':[79, 60, 97],
'op':tf2,
'divisor':13,
'throw':(1,3),
'inspections':0},

{'items':[74],
'op':tf3,
'divisor':17,
'throw':(0,1),
'inspections':0},
]

DATA = [
{'items':[63, 84, 80, 83, 84, 53, 88, 72],
'op':f0,
'divisor':13,
'throw':(4,7),
'inspections':0},

{'items':[67, 56, 92, 88, 84],
'op':f1,
'divisor':11,
'throw':(5,3),
'inspections':0},

{'items':[52],
'op':f2,
'divisor':2,
'throw':(3,1),
'inspections':0},

{'items':[59, 53, 60, 92, 69, 72],
'op':f3,
'divisor':5,
'throw':(5,6),
'inspections':0},

{'items':[61, 52, 55, 61],
'op':f4,
'divisor':7,
'throw':(7,2),
'inspections':0},

{'items':[79, 53],
'op':f5,
'divisor':3,
'throw':(0,6),
'inspections':0},

{'items':[59, 86, 67, 95, 92, 77, 91],
'op':f6,
'divisor':19,
'throw':(4,0),
'inspections':0},

{'items':[58, 83, 89],
'op':f7,
'divisor':17,
'throw':(2,1),
'inspections':0},
]

def part1(lines):
    # monkeys = parse(lines)
    # monkeys = TEST
    monkeys = DATA
    for _ in range(20):
        update(monkeys)
        # print(monkeys)
    inspections = [monkey['inspections'] for monkey in monkeys]
    inspections.sort()
    result = inspections[-1] * inspections[-2]
    return result


def part2(lines):
    data = parse(lines)
    #result = solve(data)
    #return result


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        item = line.split()
        data.append(item)
    return data


def update(monkeys):
    for monkey in monkeys:
        while monkey['items']:
            item = monkey['items'][0]
            monkey['items'] = monkey['items'][1:]
            monkey['inspections'] += 1
            item = monkey['op'](item)
            item //=  3
            if item % monkey['divisor'] == 0:
                receiver = monkey['throw'][0]
            else:
                receiver = monkey['throw'][1]
            monkeys[receiver]['items'].append(item)


if __name__ == '__main__':
    lines = open("test.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
