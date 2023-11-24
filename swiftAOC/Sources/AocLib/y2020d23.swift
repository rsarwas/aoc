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
    let cups = data[0].compactMap { Int(String($0)) }
    let crabCup = CrabCup(max: 9, initial: cups)
    crabCup.run(100)
    return String(String(describing: crabCup).dropFirst())
  }

  var answer2: Int {
    let cups = data[0].compactMap { Int(String($0)) }
    let crabCup = CrabCup(max: 1_000_000, initial: cups)
    crabCup.run(10_000_000)
    let cup1 = crabCup.cup(1)
    return cup1 * crabCup.cup(cup1)
  }

}

class CrabCup: CustomStringConvertible {
  let max: Int
  var current: Int
  var next = [Int: Int]()

  init(max: Int, initial cups: [Int]) {
    self.max = max
    current = cups[0]
    var this = current
    for i in 1..<(cups.count) {
      next[this] = cups[i]
      this = cups[i]
    }
    if cups.count == max {
      next[cups.last!] = current
    } else {
      next[cups.last!] = cups.count + 1
      // intervening will default to the next number
      next[max] = current
    }
  }

  func run(_ n: Int) {
    for _ in 0..<n {
      let remove1 = cup(current)
      let remove2 = cup(remove1)
      let remove3 = cup(remove2)
      next[current] = cup(remove3)
      let destination = findDestination(not: Set([remove1, remove2, remove3]))
      next[remove3] = cup(destination)
      next[destination] = remove1
      current = cup(current)
      //print(self)
    }
  }

  func findDestination(not: Set<Int>) -> Int {
    var proposal = current - 1
    if proposal < 1 { proposal = max }
    while not.contains(proposal) {
      proposal -= 1
      if proposal < 1 { proposal = max }
    }
    return proposal
  }

  func cup(_ n: Int) -> Int {
    next[n] ?? n + 1
  }

  var description: String {
    var result = ["1"]
    var current = 1
    while result.count < max {
      result.append(String(cup(current)))
      current = cup(current)
    }
    //return result.joined(separator: ",") + " at " + String(self.current)
    return result.joined()
  }

}
