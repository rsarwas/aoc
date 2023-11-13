struct Problem201505: Problem {
  var name: String { "2015-05" }
  func solveWith(data: [String]) -> Solution { Solution201505(data: data) }
}

struct Solution201505: Solution {
  let data: [String]

  var part1: String {
    return "\(data.filter(nice).count)"
  }

  var part2: String {
    return "\(data.filter(nice2).count)"
  }

  func nice(_ s: String) -> Bool {
    return s.hasAtLeast3Vowels && s.hasAtLeast1LetterTwiceInARow && !s.containsSpecial
  }

  func nice2(_ s: String) -> Bool {
    return s.hasNonOverlappingPair && s.hasRepeaterWithGap
  }

}

extension String {
  var hasAtLeast3Vowels: Bool {
    let vowels: [Character] = ["a", "e", "i", "o", "u"]
    var vowelCount = 0
    for char in self {
      if vowels.contains(char) {
        vowelCount += 1
        if vowelCount == 3 {
          return true
        }
      }
    }
    return false
  }

  var hasAtLeast1LetterTwiceInARow: Bool {
    for (i, char) in self.enumerated() {
      if i + 1 < self.count {
        if self[index(startIndex, offsetBy: i + 1)] == char {
          return true
        }
      }
    }
    return false
  }

  var containsSpecial: Bool {
    for special in ["ab", "cd", "pq", "xy"] {
      if self.contains(special) {
        return true
      }
    }
    return false
  }

  var hasNonOverlappingPair: Bool {
    // To avoid the complexity of String's Index system, we use the utf8 property (UTF8View, or array of int8)
    // this works because our string is guaranteed to be a simple ASCII string
    let buffer = [UInt8](self.utf8)
    for index in 0..<buffer.count - 2 {
      let pair = buffer[index...index + 1]
      for index2 in index + 2..<buffer.count - 1 {
        let otherPair = buffer[index2...index2 + 1]
        if pair == otherPair {
          return true
        }
      }
    }
    return false
  }

  var hasRepeaterWithGap: Bool {
    for (i, char) in self.dropLast(2).enumerated() {
      let charAfterGap = self[index(startIndex, offsetBy: i + 2)]
      if char == charAfterGap {
        return true
      }
    }
    return false
  }

}
