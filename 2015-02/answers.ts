function surface_area(h: number, w: number, l: number): number {
  return 2 * h * w + 2 * h * l + 2 * w * l
}

function smallest_side_area(h: number, w: number, l: number): number {
  return Math.min(h * w, h * l, w * l)
}

function smallest_side_perimeter(h: number, w: number, l: number): number {
  return Math.min(2 * h + 2 * w, 2 * h + 2 * l, 2 * w + 2 * l)
}

function volume(h: number, w: number, l: number): number {
  return h * w * l
}

function ribbon(h: number, w: number, l: number): number {
  return volume(h, w, l) + smallest_side_perimeter(h, w, l)
}

function paper(h: number, w: number, l: number): number {
  return surface_area(h, w, l) + smallest_side_area(h, w, l)
}

function totalizer(
  packages: string,
  material: (h: number, w: number, l: number) => number,
) {
  var total = 0
  packages.split('\n').forEach(function (present) {
    if (present.indexOf('x') !== -1) {
      var dims = present.split('x').map(function (dim) {
        return parseInt(dim, 10)
      })
      total += material(dims[0], dims[1], dims[2])
    }
  })
  return total
}

const stdin = 0
const fs = require('fs') // Node only; browser has no filesystem
const input = fs.readFileSync(stdin, 'utf-8')
console.log('Part 1: ' + totalizer(input, paper))
console.log('Part 2: ' + totalizer(input, ribbon))
