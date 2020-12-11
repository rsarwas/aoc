struct Problem202011: Problem {
  var name: String { "2020-11" }
  func solveWith(data: [String]) -> Solution { Solution202011(data: data) }
}

struct Solution202011: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer1)"
  }

  var answer1: Int {
    let grid = data.map { l in l.compactMap { c in Cell(rawValue:c) } }
    let life = Life(grid)
    life.run()
    return life.occupied
  }

  var answer2: Int {
    return -1
  }

}

enum Cell: Character {
  case floor = "."
  case seat = "L"
  case occupied = "#"
}

class Life {
  var grid: [[Cell]]
  let w: Int
  let h: Int

  init(_ grid: [[Cell]]) {
    self.grid = grid
    w = grid[0].count
    h = grid.count
  }

  func run() -> Void {
    var didChange = false
    repeat {
      didChange = update()
    } while didChange
  }

  func update() -> Bool {
    var didChange = false
    let row = Array<Cell>(repeating: .floor, count: w)
    var newGrid = Array<Array<Cell>>(repeating: row, count: h)
    for y in 0..<h {
      for x in 0..<w {
        let cell = newCell(x, y)
        newGrid[y][x] = cell
        if cell != grid[y][x] {
          didChange = true
        }
      }
    }
    grid = newGrid
    return didChange
  }

  func newCell(_ x: Int, _ y: Int) -> Cell {
    switch grid[y][x]  {
    case .floor: return .floor
    case .seat: return sparse(x, y, n: 0) ? .occupied : .seat
    //case .occupied: return crowded(x, y, n: 4) ? .seat : .occupied  // Part1
    case .occupied: return crowded(x, y, n: 5) ? .seat : .occupied  // Part2
    }
  }

  func sparse(_ x: Int, _ y: Int, n: Int) -> Bool {
    // return true if n or less of the occupied seats around x,y
    // assumes grid[y][x] is a seat (unoccupied)
    //return adjacentSeats(x,y).filter { $0 == .occupied }.count <= n // Part1
    return visibleSeats(x,y).filter { $0 == .occupied }.count <= n  // Part2
  }

  func crowded(_ x: Int, _ y: Int, n: Int) -> Bool {
    // return true if 4 or more seats around x,y are occupied
    // assumes grid[y][x] is occupied
    //return adjacentSeats(x,y).filter { $0 == .occupied }.count >= n // Part1
    return visibleSeats(x,y).filter { $0 == .occupied }.count >= n  // Part2
  }

  func adjacentSeats(_ x: Int, _ y: Int) -> [Cell] {
    var cells = [Cell]()
    let x1 = max(x-1,0)
    let x2 = min(x+1,w-1)
    let y1 = max(y-1,0)
    let y2 = min(y+1,h-1)
    for yy in y1...y2 {
      for xx in x1...x2 {
        if yy == y && xx == x { continue } //skip the current cell
        let cell = grid[yy][xx]
         if cell != .floor { cells.append(cell) }
      }
    }
    return cells
  }

  func visibleSeats(_ x: Int, _ y: Int) -> [Cell] {
    var cells = [Cell]()
    // right
    for i in x+1..<w { if grid[y][i] != .floor { cells.append(grid[y][i]); break } }
    // lower right
    var inc = 1
    while x+inc < w && y+inc < h {
      if grid[y+inc][x+inc] != .floor { cells.append(grid[y+inc][x+inc]); break }
      inc += 1
    }
    // down
    for i in y+1..<h { if grid[i][x] != .floor { cells.append(grid[i][x]); break } }
    // lower left
    inc = 1
    while 0 <= x-inc && y+inc < h {
      if grid[y+inc][x-inc] != .floor { cells.append(grid[y+inc][x-inc]); break }
      inc += 1
    }
    // left
    inc = 1
    while 0 <= x-inc {
      if grid[y][x-inc] != .floor { cells.append(grid[y][x-inc]); break }
      inc += 1
    }
    // upper left
    inc = 1
    while 0 <= x-inc && 0 <= y-inc {
      if grid[y-inc][x-inc] != .floor { cells.append(grid[y-inc][x-inc]); break }
      inc += 1
    }
    // upper
    inc = 1
    while 0 <= y-inc {
      if grid[y-inc][x] != .floor { cells.append(grid[y-inc][x]); break }
      inc += 1
    }
    // upper right
    inc = 1
    while x+inc < w && 0 <= y-inc {
      if grid[y-inc][x+inc] != .floor { cells.append(grid[y-inc][x+inc]); break }
      inc += 1
    }
    return cells
  }

  var occupied: Int {
    return grid.reduce(0) {a,b in a + b.reduce(0) {c,d in c + (d == .occupied ? 1 : 0) } }
  }
}