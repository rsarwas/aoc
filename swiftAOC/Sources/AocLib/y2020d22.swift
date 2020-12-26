struct Problem202022: Problem {
  var name: String { "2020-22" }
  func solveWith(data: [String]) -> Solution { Solution202022(data: data) }
}

struct Solution202022: Solution {
  let data: [String]

  var part1: String {
    return "\(answer())"
  }

  var part2: String {
    return "\(answer(recursive: true))"
  }

  func answer(recursive: Bool = false) -> Int {
    let combat = Combat(cards:data)
    combat.play(recursive: recursive)
    guard let winner = combat.winner else { return -1 }
    let answer = winner.reversed().enumerated().map{ (i,n) in (i+1)*n }.reduce(0, +)
    return answer
  }

}

class Combat {
  var p1: [Int]
  var p2: [Int]

  init(cards: [String]) {
    // Test case
    // p1 = [9, 2, 6, 3, 1]
    // p2 = [5, 8, 4, 7, 10]
    var buildingPlayer1 = true
    var p1 = [Int]()
    var p2 = [Int]()
    for card in cards {
      if card == "" { buildingPlayer1 = false; continue }
      if card.starts(with: "Player") { continue }
      guard let cardValue = Int(card) else { continue }
      if buildingPlayer1 {
        p1.append(cardValue)
      } else {
        p2.append(cardValue)
      }
    }
    self.p1 = p1
    self.p2 = p2
  }

  func play(recursive: Bool = false) {
    while p1.count > 0 && p2.count > 0 {
      //print(p1,p2)
      let c1 = p1.first!
      let c2 = p2.first!
      p1 = Array(p1.dropFirst())
      p2 = Array(p2.dropFirst())
      if recursive && c1 <= p1.count && c2 <= p2.count {
        //print("start recurse")
        let rCombat = RecursiveCombat(p1:Array(p1.prefix(c1)), p2:Array(p2.prefix(c2)))
        rCombat.play()
        //print("finish recurse")
        if rCombat.isP1theWinner {
          p1.append(contentsOf: [c1,c2])
        } else {
          p2.append(contentsOf: [c2,c1])
        }
      } else {
        if c1 < c2 {
          p2.append(contentsOf: [c2,c1])
        } else {
          p1.append(contentsOf: [c1,c2])
        }
      }
    }
  }

  var winner: [Int]? {
    if p1.count == 0 { return p2 }
    if p2.count == 0 { return p1 }
    return nil
  }

}

class RecursiveCombat {
  var p1: [Int]
  var p2: [Int]
  var previousStates = Set<String>()

  init(p1: [Int], p2: [Int]) {
    self.p1 = p1
    self.p2 = p2
  }

  func play() {
    while p1.count > 0 && p2.count > 0 {
      //print(p1,p2)
      let state = self.state
      if previousStates.contains(state) {
        //print("Stuck; p1 wins")
        return
      } else {
        previousStates.insert(state)
      }
      let c1 = p1.first!
      let c2 = p2.first!
      p1 = Array(p1.dropFirst())
      p2 = Array(p2.dropFirst())
      if c1 < p1.count && c2 < p2.count {
        //print("start recurse")
        let rCombat = RecursiveCombat(p1:Array(p1.prefix(c1)), p2:Array(p2.prefix(c2)))
        rCombat.play()
        //print("finish recurse")
        if rCombat.isP1theWinner {
          p1.append(contentsOf: [c1,c2])
        } else {
          p2.append(contentsOf: [c2,c1])
        }
      } else {
        if c1 < c2 {
          p2.append(contentsOf: [c2,c1])
        } else {
          p1.append(contentsOf: [c1,c2])
        }
      }
    }
  }

  var isP1theWinner: Bool {
    if p1.count == 0 { return false }
    return true
  }

  var state: String {
    let p1s = p1.map { String($0) }.joined(separator: ",")
    let p2s = p2.map { String($0) }.joined(separator: ",")
    return p1s + ":" + p2s
  }

}
