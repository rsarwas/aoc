struct Problem202020: Problem {
  var name: String { "2020-20" }
  func solveWith(data: [String]) -> Solution { Solution202020(data: data) }
}

struct Solution202020: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    //let adapters = data.compactMap { Int($0) }.sorted()
    return -1
  }

  var answer2: Int {
    return -1
  }

}
