import sys


def fuel_mass(item):
   return item//3 - 2

def total_mass(item):
    mass = fuel_mass(item)
    if mass < 0:
        return 0
    else:
        return mass + total_mass(mass)

if __name__ == '__main__':
    total1 = 0
    total2 = 0
    for module in sys.stdin:
        total1 += fuel_mass(int(module))
        total2 += total_mass(int(module))
    print("Part 1: {0}".format(total1))
    print("Part 2: {0}".format(total2))
