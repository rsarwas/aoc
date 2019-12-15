def count_passwords():
    # count passwords in 359282 to 820401
    # RULE 1: no decreasing digits
    # RULE 2: at least one pair of adjacent digits match
    # simplify to 359,999 to 7999999
    # zero in 359282 to 359,998 - digits decreasing
    # zero in 800,000 to 820401 - digits decrease 8->0, 8->1, 8->2
    def minb(x):
        return 5 if x == 3 else x
    def minc(x,y):
        return 9 if x == 3 and y == 5 else y
    count = 0
    for a in range(3,(7+1)):
        for b in range(minb(a),10):
            for c in range(minc(a,b),10):
                for d in range(c,10):
                    for e in range(d,10):
                        # count options for last digit for this sequence of the first 5 digits
                        if a==b or b==c or c==d or d==e:
                            count += 10-e  # there is a pair so count all none decreasing options
                        else:
                            count += 1 # only 1; must match the last digit to have a pair
    return count

if __name__ == '__main__':
    part1 = count_passwords()
    print("Part 1: {0}".format(part1))
    part2 = "n/a"
    print("Part 2: {0}".format(part2))