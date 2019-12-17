import sys

def verify(data, ncols, nrows):
    npix = ncols * nrows
    nlayers = len(data)//npix
    min0 = npix
    result = 0
    for i in range(nlayers):
        n0,n1,n2 = pixel_values(data[npix*i:npix*(i+1)])
        if n0 < min0:
            min0 = n0
            result = n1*n2
    return result

def pixel_values(data):
    n0,n1,n2 = 0,0,0
    for i in data:
        if i == 0:
            n0 += 1
        if i == 1:
            n1 += 1
        if i == 2:
            n2 += 1
    return n0,n1,n2

def decode(data, ncols, nrows):
    npix = ncols * nrows
    nlayers = len(data)//npix
    image = [2]*npix
    for i in range(nlayers):
        layer = data[npix*i:npix*(i+1)]
        for index,pixel in enumerate(layer):
            if pixel != 2 and image[index] == 2:
                image[index] = pixel
    return image

if __name__ == '__main__':
    pixels = [int(x) for x in sys.stdin.read().strip()]
    part1 = verify(pixels, 25, 6)
    print("Part 1: {0}".format(part1))
    print("part2")
    image = decode(pixels, 25, 6)
    for i in range(6):
        for j in range(25):
            print(' ' if image[25*i+j] == 0 else 'X', end = '')
        print()
