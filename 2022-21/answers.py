# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    result = solve(data, "root")
    return result


def part2(lines):
    return -1


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


def solve(data, monkey):
    job = data[monkey]
    if job[0] == 'yell':
        return job[1]
    else:
        op, monkey1, monkey2 = job
        if op == "*":
            return solve(data,monkey1) * solve(data,monkey2)
        if op == "/":
            return solve(data,monkey1) / solve(data,monkey2)
        if op == "+":
            return solve(data,monkey1) + solve(data,monkey2)
        if op == "-":
            return solve(data,monkey1) - solve(data,monkey2)
    print("PANIC. unexpected job")
    return -1


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
