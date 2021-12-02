struct Problem202101: Problem {
  var name: String { "2021-01" }
  func solveWith(data: [String]) -> Solution { Solution202101(data: data) }
}

struct Solution202101: Solution {
  let data: [String]

  var part1: String {
    let (answer, _) = data.compactMap { Int($0) }.reduce((0,Int.max)) { (acc, depth) in 
      let (incCount, lastDepth) = acc
      if depth > lastDepth { return (incCount + 1, depth) }
      return (incCount, depth)
    }
    return "\(answer)"
  }

  var part2: String {
    let depths = data.compactMap { Int($0) }
    var increases = 0
    var lastDepth = Int.max
    for (d1, (d2, d3)) in zip(depths, zip(depths[1...], depths[2...])) {
      let depth = d1 + d2 + d3
      if depth > lastDepth { increases += 1 }
      lastDepth = depth
    }
    return "\(increases)"
  }

}
