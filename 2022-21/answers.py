# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    result = solve(data, "root", 1, None)
    return result


def part2(lines):
    data = parse(lines)
    # explore(data)
    # return interpolate(data, 300, 400) # test
    return interpolate(data, 3e12, 4e12) # problem


def parse(lines):
    data = {}
    for line in lines:
        monkey = {}
        line = line.strip()
        name, job = line.split(": ")
        try:
            name1, op, name2 = job.split(" ")
            job = (op, name1, name2)
        except ValueError:
            op = "yell"
            val = int(job)
            job = (op, val)
        data[name] = job
    return data


def solve(data, monkey, version, value):
    if monkey == "humn" and version == 2:
        return value
    job = data[monkey]
    if job[0] == 'yell':
        return job[1]
    else:
        op, monkey1, monkey2 = job
        if op == "*":
            return solve(data,monkey1, version, value) * solve(data,monkey2, version, value)
        if op == "/":
            return solve(data,monkey1, version, value) / solve(data,monkey2, version, value)
        if op == "+":
            return solve(data,monkey1, version, value) + solve(data,monkey2, version, value)
        if op == "-":
            return solve(data,monkey1, version, value) - solve(data,monkey2, version, value)
    print("PANIC. unexpected job")
    return -1


def explore(data):
    _, monkey1, monkey2 = data["root"]
    # for val in [100, 200, 300, 400]:  # test puzzle
    for val in [1e12, 2e12, 3e12, 4e12, 5e12]:
        left = solve(data, monkey1, 2, val)
        right = solve(data, monkey2, 2, val)
        if left == right:
            print("the winner is", val)
        else:
            verdict = "too small" if left < right else "too big" 
            print("val", val, "is", verdict, "left", left, "right", right)


def interpolate(data, lower, upper):
    _, monkey1, monkey2 = data["root"]
    val = (lower + upper) // 2
    left = solve(data, monkey1, 2, val)
    right = solve(data, monkey2, 2, val)
    safety = 0
    while left != right and safety < 50:
        # print(upper, lower, left - right)
        if left < right:
            # lower = val # test left grows with larger inputs
            upper = val # puzzle: left shrinks with larger inpu
        else:
            # upper = val # test left grows with larger inputs
            lower = val # puzzle: left shrinks with larger inputs
        val = (lower + upper) // 2
        left = solve(data, monkey1, 2, val)
        right = solve(data, monkey2, 2, val)
        safety += 1
    return val


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
