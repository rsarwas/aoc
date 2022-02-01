# Data Model:
# ===========
# data is a list of decimal digits

def part1(data):
    # brute force matrix multiplication for 100 cycles
    numbers = parse(data)
    results = fft(numbers, 100)
    return "".join([str(n) for n in results[:8]])

def part2(lines):
    return -1

def parse(data):
    return [int(c) for c in data]

def fft(numbers, cycles):
    matrix = make_matrix(len(numbers))
    for _ in range(cycles):
        numbers = multiply(matrix, numbers)
    return numbers

def multiply(matrix, vector):
    results = []
    n = len(vector)
    for i in range(n):
        row = matrix[i]
        results.append(abs(cross_multiply(row, vector))%10)
    return results

def cross_multiply(l1, l2):
    return sum([a*b for (a,b) in zip(l1,l2)])

def make_matrix(n):
    matrix = []
    for i in range(n):
        matrix.append(make_row(i,n))
    return matrix

def make_row(i,n):
    i += 1
    base = [0]*i + [1]*i + [0]*i + [-1]*i
    m = 1 + n // (i * 4)
    row = []
    for _ in range(m):
        row += base
    return row[1:n+1]

if __name__ == '__main__':
    # data = "12345678"
    # data = "80871224585914546619083218645595" # => 24176176
    # data = "19617804207202209144916044189917" # => 73745418
    # data = "69317163492948606335995924319873" # => 52432133
    data = open("input.txt").read() # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
