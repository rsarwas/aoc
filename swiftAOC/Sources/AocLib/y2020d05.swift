struct Problem202005: Problem {
  var name: String { "2020-05" }
  func solveWith(data: [String]) -> Solution { Solution202005(data: data) }
}

struct Solution202005: Solution {
  let data: [String]

  var part1: String {
    guard let answer = maximumSeatId else { return "Invalid Input" }
    return "\(answer)"
  }

  var part2: String {
    guard let answer = emptySeatId else { return "Invalid Input" }
    return "\(answer)"
  }

  var maximumSeatId: Int? {
    data.compactMap { $0.asBoardingPass.seatId }.max()
  }

  var emptySeatId: Int? {
    data.compactMap { $0.asBoardingPass.seatId }.missingInt
  }
}

extension String {
  var asBoardingPass: BoardingPass {
    BoardingPass(spec: self)
  }
}

struct BoardingPass {
  let spec: String

  var seatId: Int? {
    let bits = spec.map { $0 == "B" || $0 == "R" ? "1" : "0" }.reduce("") { $0 + $1 }
    return Int(bits, radix: 2)
  }
}

extension Array where Element == Int {
  var missingInt: Int? {
    let sortedInts = self.sorted()
    var lastSeat = 0
    for seat in sortedInts {
      if lastSeat == 0 {
        lastSeat = seat
        continue
      }
      if seat > lastSeat + 1 {
        return lastSeat + 1
      }
      lastSeat = seat
    }
    return nil
  }
}
