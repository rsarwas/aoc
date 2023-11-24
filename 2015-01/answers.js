function what_floor(text) {
  var floor = 0
  for (var i = 0; i < text.length; i++) {
    var char = text.charAt(i)
    if (char == '(') {
      floor++
    }
    if (char == ')') {
      floor--
    }
  }
  return floor
}

function when_basement(text) {
  var floor = 0
  for (var i = 0; i < text.length; i++) {
    var char = text.charAt(i)
    if (char == '(') {
      floor++
    }
    if (char == ')') {
      floor--
    }
    if (floor == -1) {
      return i + 1
    }
  }
  return -1
}

var stdin = 0
var fs = require('fs') // Node only; browser has no filesystem
var input = fs.readFileSync(stdin, 'utf-8')
console.log('Part 1: ' + what_floor(input))
console.log('Part 2: ' + when_basement(input))
