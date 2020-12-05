struct Problem202007: Problem {
  var name: String { "2020-07" }
  func solveWith(data: [String]) -> Solution { Solution202007(data: data) }
}

struct Solution202007: Solution {
  let data: [String]

  var part1: String {
    return "\(answer)"
  }

  var part2: String {
    return "\(answer)"
  }

  var answer: String { return "Not Implemented" }
}
