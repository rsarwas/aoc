struct Problem202015: Problem {
  var name: String { "2020-15" }
  func solveWith(data: [String]) -> Solution { Solution202015(data: data) }
}

struct Solution202015: Solution {
  let data: [String]

  var part1: String {
    return "\(answer(limit: 2020))"
  }

  var part2: String {
    return "\(answer(limit: 30_000_000))"
  }

  func answer(limit: Int) -> Int {
    let numbers = data[0].split(separator: ",").compactMap { Int($0) }
    // key is the number spoken the tuple is (most recent turn spoken, previous turn or 0)
    var lastTwoTurns = [Int: (Int, Int)]()
    var lastNumber = -1
    var turn = 0
    for number in numbers {
      turn += 1
      lastTwoTurns[number] = (turn, 0)
      lastNumber = number
    }
    while turn < limit {
      turn += 1
      let spoken = lastTwoTurns[lastNumber]!
      let number = spoken.1 == 0 ? 0 : spoken.0 - spoken.1
      if let previous = lastTwoTurns[number] {
        lastTwoTurns[number] = (turn, previous.0)
      } else {
        lastTwoTurns[number] = (turn, 0)
      }
      lastNumber = number
    }
    return (lastNumber)
  }

}
