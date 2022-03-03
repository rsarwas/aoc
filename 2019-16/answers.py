# Data Model:
# ===========
# data is a list of decimal digits

def part1(data):
    # brute force matrix multiplication for 100 cycles
    numbers = parse(data)
    results = fft(numbers, 100)
    return "".join([str(n) for n in results[:8]])

def part2(data):
    # brute force will not work.
    # However, due to the nature of the matrix of 0,1,0,-1,...
    # the bottom left quarter is all ones on the diagonal and above
    # and all zeros below, for example in an 8x8
    # 1  0 -1  0  1  0 -1  0
    # 0  1  1  0  0 -1 -1  0
    # 0  0  1  1  1  0  0  0
    # 0  0  0  1  1  1  1  0
    # 0  0  0  0  1  1  1  1
    # 0  0  0  0  0  1  1  1
    # 0  0  0  0  0  0  1  1
    # 0  0  0  0  0  0  0  1
    # therefore the second half of the number is easier to calculate
    # The last number is always the same after each cycle.
    # the len-n number is the sum of the last n digits (mod 10) 
    # the second half of the number can be calculated from back to front
    # 
    numbers = parse(data)
    offset = int(data[:7])
    sub_length = len(data)
    length = 10000 * sub_length
    # make sure the offset is in the second half
    if offset < length / 2:
        return -1    
    # build the ending list of numbers to "fft"
    sub_offset = offset % sub_length
    end_length = length - offset
    sub_count = end_length // sub_length
    # print(len(data), length, offset, sub_offset, sub_length, sub_count)
    end_data = numbers[sub_offset:]
    for _ in range(sub_count):
        end_data += numbers

    # Do the "fast"  fft on the end data
    for _ in range(100):
        end_data = fast_fft(end_data)
    return "".join([str(n) for n in end_data[:8]])

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

def fast_fft(data):
    n = len(data)
    for i in range(n-1,0,-1):
        data[i-1] = (data[i-1] + data[i]) % 10
    return data

if __name__ == '__main__':
    # simple test
    # data = "12345678"

    # test for part 1
    # data = "80871224585914546619083218645595" # => 24176176
    # data = "19617804207202209144916044189917" # => 73745418
    # data = "69317163492948606335995924319873" # => 52432133

    # test for part 2
    # data = "03036732577212944063491565474664" # => 84462026
    # data = "02935109699940807407585447034323" # => 78725270
    # data = "03081770884921959731165446850517" # => 53553731

    data = open("input.txt").read() # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
