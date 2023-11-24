import sys


def surface_area(h, w, l):
    return 2 * h * w + 2 * h * l + 2 * w * l


def smallest_side_area(h, w, l):
    return min(h * w, h * l, w * l)


def smallest_side_perimeter(h, w, l):
    return min(2 * h + 2 * w, 2 * h + 2 * l, 2 * w + 2 * l)


def volume(h, w, l):
    return h * w * l


def ribbon(h, w, l):
    return volume(h, w, l) + smallest_side_perimeter(h, w, l)


def paper(h, w, l):
    return surface_area(h, w, l) + smallest_side_area(h, w, l)


def totalizer(packages, material):
    total = 0
    for present in packages.split("\n"):
        if "x" in present:
            dims = [int(dim) for dim in present.split("x")]
            total += material(*dims)
    return total


if __name__ == "__main__":
    input = sys.stdin.read()
    print("Part 1: {0}".format(totalizer(input, paper)))
    print("Part 2: {0}".format(totalizer(input, ribbon)))
