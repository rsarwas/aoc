struct Problem202304: Problem {
  var name: String { "2023-04" }
  func solveWith(data: [String]) -> Solution { Solution202304(data: data) }
}

struct Solution202304: Solution {
  let data: [String]

  var part1: String {
    let wins = data.compactMap { $0.asWins }
    let points = wins.map {
      if $0 <= 0 {
        return 0
      } else {
        return 1 << ($0 - 1)
      }
    }
    let answer = points.reduce(0, +)
    return "\(answer)"
  }

  var part2: String {
    let wins = data.compactMap { $0.asWins }
    var cards = Array(repeating: 1, count: data.count)
    for (id, win) in wins.enumerated() {
      if win == 0 { continue }
      for offset in 1...win {
        if id + offset < cards.count {
          cards[id + offset] += cards[id]
        }
      }
    }
    let answer = cards.reduce(0, +)
    return "\(answer)"
  }

}

extension String {
  var asWins: Int? {
    let parts = self.split(separator: ": ")
    guard parts.count == 2 else { return nil }
    let sub_parts = parts[1].split(separator: " | ")
    guard sub_parts.count == 2 else { return nil }
    let winning_numbers = sub_parts[0].split(separator: " ", omittingEmptySubsequences: true)
    let numbers_held = sub_parts[1].split(separator: " ", omittingEmptySubsequences: true)
    let heldNumbersThatAreWinning = numbers_held.filter(winning_numbers.contains)
    return heldNumbersThatAreWinning.count
  }
}
