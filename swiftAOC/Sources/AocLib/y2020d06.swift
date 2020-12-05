struct Problem202006: Problem {
  var name: String { "2020-06" }
  func solveWith(data: [String]) -> Solution { Solution202006(data: data) }
}

struct Solution202006: Solution {
  let data: [String]

  var part1: String {
    return "\(answer)"
  }

  var part2: String {
    return "\(answer)"
  }

  var answer: String { return "Not Implemented" }
}
