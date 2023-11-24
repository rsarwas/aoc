function surface_area(h, w, l) {
  return 2 * h * w + 2 * h * l + 2 * w * l
}

function smallest_side_area(h, w, l) {
  return Math.min(h * w, h * l, w * l)
}

function smallest_side_perimeter(h, w, l) {
  return Math.min(2 * h + 2 * w, 2 * h + 2 * l, 2 * w + 2 * l)
}

function volume(h, w, l) {
  return h * w * l
}

function ribbon(h, w, l) {
  return volume(h, w, l) + smallest_side_perimeter(h, w, l)
}

function paper(h, w, l) {
  return surface_area(h, w, l) + smallest_side_area(h, w, l)
}

function totalizer(packages, material) {
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

var stdin = 0
var fs = require('fs') // Node only browser has no filesystem
var input = fs.readFileSync(stdin, 'utf-8')
console.log('Part 1: ' + totalizer(input, paper))
console.log('Part 2: ' + totalizer(input, ribbon))
