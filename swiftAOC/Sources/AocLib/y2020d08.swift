struct Problem202008: Problem {
  var name: String { "2020-08" }
  func solveWith(data: [String]) -> Solution { Solution202008(data: data) }
}

struct Solution202008: Solution {
  let data: [String]

  var part1: String {
    return "\(answer)"
  }

  var part2: String {
    return "\(answer)"
  }

  var answer: String { return "Not Implemented" }
}
