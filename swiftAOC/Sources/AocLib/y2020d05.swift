struct Problem202005: Problem {
  var name: String { "2020-05" }
  func solveWith(data: [String]) -> Solution { Solution202005(data: data) }
}

struct Solution202005: Solution {
  let data: [String]

  var part1: String {
    return "\(answer)"
  }

  var part2: String {
    return "\(answer)"
  }

  var answer: String { return "Not Implemented" }
}
