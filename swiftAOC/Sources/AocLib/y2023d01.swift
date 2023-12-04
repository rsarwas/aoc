struct Problem202301: Problem {
  var name: String { "2023-01" }
  func solveWith(data: [String]) -> Solution { Solution202301(data: data) }
}

struct Solution202301: Solution {
  let data: [String]

  var part1: String {
    let answer = data.map(asCalibrationValue).reduce(0, +)
    return "\(answer)"
  }

  var part2: String {
    let answer = data.map(asCalibrationValue2).reduce(0, +)
    return "\(answer)"

  }

  func asCalibrationValue(s: String) -> Int {
    let (x, y) = firstAndLastDigits(of: s, withText: false)
    return x * 10 + y
  }
  func asCalibrationValue2(s: String) -> Int {
    let (x, y) = firstAndLastDigits(of: s, withText: true)
    return x * 10 + y
  }

  func firstAndLastDigits(of s: String, withText: Bool) -> (Int, Int) {
    var firstIndex = s.endIndex
    var firstDigit: Int?
    var lastIndex = s.startIndex
    var lastDigit: Int?
    for digit in 0...9 {
      let digitChar = Character(String(digit))
      if let first = s.firstIndex(of: digitChar), first < firstIndex {
        firstIndex = first
        firstDigit = digit
      }
      // use >= since last may be the startIndex and lastIndex starts as startIndex
      if let last = s.lastIndex(of: digitChar), last >= lastIndex {
        lastIndex = last
        lastDigit = digit
      }
    }
    if withText {
      for (value, text) in [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
      ].enumerated() {
        if let range = s.range(of: text) {
          if range.lowerBound < firstIndex {
            firstIndex = range.lowerBound
            firstDigit = value
          }
        }
        if let range = s.range(of: text, options: .backwards) {
          if range.lowerBound >= lastIndex {
            lastIndex = range.lowerBound
            lastDigit = value
          }
        }
      }
    }
    return (firstDigit ?? 0, lastDigit ?? 0)
  }
}
