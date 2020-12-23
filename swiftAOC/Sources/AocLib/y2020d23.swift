struct Problem202023: Problem {
  var name: String { "2020-23" }
  func solveWith(data: [String]) -> Solution { Solution202023(data: data) }
}

struct Solution202023: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: String {
    var cups = data[0].compactMap { Int(String($0)) }
    //print(cups)
    for _ in 0..<100 {
      let n = destination(cups)
      cups = cups[4...n] + cups[1..<4] + cups[(n+1)...] + [cups[0]]
    }
    //rotate to 1 at front
    while cups[0] != 1 {
      let first = cups.first!
      cups = Array(cups.dropFirst())
      cups.append(first)
    }
    //print(cups)
    return cups.dropFirst().map { String($0) }.joined()
  }

  var answer2: Int {
    return -1
  }

  func destination(_ cups: [Int]) -> Int {
    // The current cup is always at the head of the list
    var newValue = cups[0] - 1
    let pickups = Set(cups[1..<4])
    if newValue < 1 { newValue = 9 }
    while pickups.contains(newValue) {
      newValue -= 1
      if newValue < 1 { newValue = 9 }
    }
    return cups.firstIndex(of: newValue)!
  }

}
