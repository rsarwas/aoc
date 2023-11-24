struct Problem202017: Problem {
  var name: String { "2020-17" }
  func solveWith(data: [String]) -> Solution { Solution202017(data: data) }
}

struct Solution202017: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let conway = Conway(input: data)
    conway.run(n: 6)
    return conway.activeCubeCount
  }

  var answer2: Int {
    let conway = Conway2(input: data)
    conway.run(n: 6)
    return conway.activeCubeCount
  }

}

class Conway {

  var xs = 0..<0
  var ys = 0..<0
  var zs = 0..<0
  var activeCubes = Set<Coord3>()

  init(input: [String]) {
    var y = 0
    var x = 0
    var z = 0
    for line in input {
      z = 1
      x = 0
      for char in line {
        if char == "#" {
          activeCubes.insert(Coord3(x: x, y: y, z: 0))
        }
        x += 1
      }
      y += 1
    }
    xs = 0..<x
    ys = 0..<y
    zs = 0..<z
    //printSpace()
  }

  func run(n: Int) {
    for _ in 0..<n {
      var newActiveCubes = Set<Coord3>()
      for z in nextZs {
        for y in nextYs {
          for x in nextXs {
            if isActive(x: x, y: y, z: z) {
              newActiveCubes.insert(Coord3(x: x, y: y, z: z))
            }
          }
        }
      }
      // Assume cube grows on each round
      // could find xmin, xmax... on each round and set a tighter range
      xs = nextXs
      ys = nextYs
      zs = nextZs
      activeCubes = newActiveCubes
      //print("After Cycle \(i+1)")
      //printSpace()
    }
  }

  func isActive(x: Int, y: Int, z: Int) -> Bool {
    /*
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
    */
    let n = activeNeighbors(x: x, y: y, z: z)
    let active = activeCubes.contains(Coord3(x: x, y: y, z: z))
    if active {
      return n == 2 || n == 3
    } else {
      return n == 3
    }
  }

  func activeNeighbors(x: Int, y: Int, z: Int) -> Int {
    var active = 0
    for zz in z - 1...z + 1 {
      for yy in y - 1...y + 1 {
        for xx in x - 1...x + 1 {
          if xx == x && yy == y && zz == z { continue }
          if activeCubes.contains(Coord3(x: xx, y: yy, z: zz)) {
            active += 1
          }
        }
      }
    }
    return active
  }

  var nextXs: Range<Int> {
    return xs.lowerBound - 1..<(xs.upperBound + 1)
  }

  var nextYs: Range<Int> {
    return ys.lowerBound - 1..<(ys.upperBound + 1)
  }

  var nextZs: Range<Int> {
    return zs.lowerBound - 1..<(zs.upperBound + 1)
  }

  var activeCubeCount: Int {
    activeCubes.count
  }

  func printSpace() {
    var grid = [[[Character]]](
      repeating: [[Character]](
        repeating: [Character](repeating: ".", count: xs.count), count: ys.count), count: zs.count)
    for coord in activeCubes {
      grid[coord.z - xs.lowerBound][coord.y - xs.lowerBound][coord.x - xs.lowerBound] = "#"
    }
    for z in zs {
      print("Z=\(z)")
      for y in ys {
        print(String(grid[z - zs.lowerBound][y - ys.lowerBound]))
      }
    }
  }

}

class Conway2 {

  var xs = 0..<0
  var ys = 0..<0
  var zs = 0..<0
  var ws = 0..<0
  var activeCubes = Set<Coord4>()

  init(input: [String]) {
    var y = 0
    var x = 0
    var z = 0
    var w = 0
    for line in input {
      z = 1
      w = 1
      x = 0
      for char in line {
        if char == "#" {
          activeCubes.insert(Coord4(x: x, y: y, z: 0, t: 0))
        }
        x += 1
      }
      y += 1
    }
    xs = 0..<x
    ys = 0..<y
    zs = 0..<z
    ws = 0..<w
  }

  func run(n: Int) {
    for _ in 0..<n {
      var newActiveCubes = Set<Coord4>()
      for w in nextWs {
        for z in nextZs {
          for y in nextYs {
            for x in nextXs {
              if isActive(x: x, y: y, z: z, w: w) {
                newActiveCubes.insert(Coord4(x: x, y: y, z: z, t: w))
              }
            }
          }
        }
      }
      // Assume cube grows on each round
      // could find xmin, xmax... on each round and set a tighter range
      xs = nextXs
      ys = nextYs
      zs = nextZs
      ws = nextWs
      activeCubes = newActiveCubes
      //print("After Cycle \(i+1)")
      //printSpace()
    }
  }

  func isActive(x: Int, y: Int, z: Int, w: Int) -> Bool {
    /*
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
    */
    let n = activeNeighbors(x: x, y: y, z: z, w: w)
    let active = activeCubes.contains(Coord4(x: x, y: y, z: z, t: w))
    if active {
      return n == 2 || n == 3
    } else {
      return n == 3
    }
  }

  func activeNeighbors(x: Int, y: Int, z: Int, w: Int) -> Int {
    var active = 0
    for ww in w - 1...w + 1 {
      for zz in z - 1...z + 1 {
        for yy in y - 1...y + 1 {
          for xx in x - 1...x + 1 {
            if xx == x && yy == y && zz == z && ww == w { continue }
            if activeCubes.contains(Coord4(x: xx, y: yy, z: zz, t: ww)) {
              active += 1
            }
          }
        }
      }
    }
    return active
  }

  var nextXs: Range<Int> {
    return xs.lowerBound - 1..<xs.upperBound + 1
  }

  var nextYs: Range<Int> {
    return ys.lowerBound - 1..<ys.upperBound + 1
  }

  var nextZs: Range<Int> {
    return zs.lowerBound - 1..<zs.upperBound + 1
  }

  var nextWs: Range<Int> {
    return ws.lowerBound - 1..<ws.upperBound + 1
  }

  var activeCubeCount: Int {
    activeCubes.count
  }

}
