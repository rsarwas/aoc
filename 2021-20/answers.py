# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# The image structure (dictionary) has a key called "background"
# which says if the infinite space around the image data is ON or OFF
# In the sample, The 0 bit of the enhancement algorithm was OFF, so
# the infinite area all OFF => 0 > OFF.  In the real puzzle data,
# 0 => goes to ON, so all un mapped pixels are ON, fortunately, the
# 512 bit (111_111_111 or all ON) is OFF, so the infinite boundary
# will flip ON/OFF on each iteration.
# 

ON = "#"
OFF = "."

def part1(lines):
    algorithm, image = parse(lines)
    for _ in range(2):
        image = enhance(image, algorithm)
    return brightness(image)

def part2(lines):
    algorithm, image = parse(lines)
    for _ in range(50):
        image = enhance(image, algorithm)
    return brightness(image)

def parse(lines):
    algorithm = lines[0].strip()
    # skip a blank line
    data = [line.strip() for line in lines[2:]]
    image = make_image(data)
    return algorithm, image

def make_image(data):
    image = {
        "data": data,
        "width": len(data[0]),
        "height": len(data),
        "background": OFF
    }
    return image

def enhance(image, algorithm):
    # The new image will be 2 pixels taller and wider.
    # i.e. the pixel at -1,-1, will sample (0,0)
    data = []
    for row_index in range(-1,image["height"]+1):
        row = []
        for col_index in (range(-1,image["width"]+1)):
            pixel_code = sample(image, row_index, col_index)
            pixel = algorithm[pixel_code]
            row.append(pixel)
        data.append(row)
    new_image = make_image(data)
    # toggle the background (see comments at the top of the file)
    if algorithm[0] == ON and algorithm[-1] == OFF:
        new_image["background"] = OFF if image["background"] == ON else ON
    return new_image

# (row, column) offsets, top left to bottom right; across then down
# row numbers increase downward; column numbers increase to the right
ADJACENT = [(-1,-1), (-1, 0), (-1, 1),
            ( 0,-1), ( 0, 0), ( 0, 1),
            ( 1,-1), ( 1, 0), ( 1, 1)]

def sample(image, row_index, col_index):
    bits = [] # ON or OFF
    data = image["data"]
    w, h = image["width"], image["height"]
    background = image["background"]
    for (dr,dc) in ADJACENT:
        r,c = row_index + dr, col_index + dc
        if r < 0 or c < 0 or r >= h or c >= w:
            bits.append(background)
        else:
            bits.append(data[r][c])
    b_bits = ["0" if bit is OFF else "1" for bit in bits]
    num = int("".join(b_bits), base=2)
    # print(row_index, col_index, bits, b_bits, num)
    return num

def brightness(image):
    total = 0
    for row in image["data"]:
        for pixel in row:
            if pixel == ON:
                total += 1
    return total

def print_image(image):
    for row in image["data"]:
        if isinstance(row, list):
            print("".join(row))
        else:
            print(row)

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
