struct Problem202003: Problem {
  var name: String { "2020-03" }
  func solveWith(data: [String]) -> Solution { Solution202003(data: data) }
}

struct Solution202003: Solution {
  let data: [String]

  var part1: String {
    return "\(numberTreesAt3to1)"
  }

  var part2: String {
    return "\(numberTreesAtMultipleSlopes)"
  }

  var numberTreesAt3to1: Int {
    guard let treeGrid = data.asTreeGrid else { return -1 }
    let count = treeGrid.countTrees(start: Location(x:0, y:0), moveRight: 3, moveDown: 1)
    return count
  }

  var numberTreesAtMultipleSlopes: Int {
    guard let treeGrid = data.asTreeGrid else { return -1 }
    let slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    return slopes.map { (x,y) in
      treeGrid.countTrees(start: Location(x:0, y:0), moveRight: x, moveDown: y)
    }.reduce(1) { $0*$1 }
  }


}

extension Array where Element == String {
  var asTreeGrid: TreeGrid? {
    var trees = Set<Location>()
    let height = self.count
    guard height > 0, self[1].count > 0 else { return nil }
    let width = self[1].count
    for (y, line) in self.enumerated() {
      for (x, char) in line.enumerated() {
        if char == "#" { trees.insert(Location(x:x, y:y)) }
      }
    }
    return TreeGrid(width: width, height: height, trees: trees)
  }
}

struct Location: Hashable {
  let x: Int
  let y: Int
}
struct TreeGrid {
  let width: Int
  let height: Int
  let trees: Set<Location>

  func countTrees(start: Location, moveRight: Int, moveDown: Int) -> Int {
    var x = start.x
    var y = start.y
    var count = 0
    while x < width && y < height {
      let location = Location(x:x, y:y)
      if trees.contains(location) { count += 1 }
      x += moveRight
      y += moveDown
    }
    if y < height {
      count += countTrees(start: Location(x:x - width, y:y), moveRight: moveRight, moveDown: moveDown)
    }
    return count
  }

}