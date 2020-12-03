import Foundation

struct Problem202002: Problem {
  var name: String { "2020-02" }
  func solveWith(data: [String]) -> Solution { Solution202002(data: data) }
}

struct Solution202002: Solution {
  let data: [String]

  var part1: String {
    return "\(passwordCountPassingTest1)"
  }

  var part2: String {
    return "\(passwordCountPassingTest2)"
  }

  var passwordCountPassingTest1: Int {
    return data.compactMap { $0.asPasswordChecker }
      .filter { $0.passingTest1 }
      .count
  }

  var passwordCountPassingTest2: Int {
    return data.compactMap { $0.asPasswordChecker }
      .filter { $0.passingTest2 }
      .count
  }

}

extension String {
  var asPasswordChecker: PasswordChecker? {
    let parts = self.split(separator: " ")
    guard parts.count == 3 else { return nil }
    let rangeParts = parts[0].split(separator: "-")
    guard rangeParts.count == 2 else { return nil }
    guard let int1 = Int(rangeParts[0]), let int2 = Int(rangeParts[1]) else { return nil }
    guard let char1 = parts[1].first else { return nil }
    let password = String(parts[2])
    return PasswordChecker(int1: int1, int2: int2, char1: char1, password: password)
  }
}

struct PasswordChecker {
  let int1: Int
  let int2: Int
  let char1: Character
  let password: String

  var passingTest1: Bool {
    let count = password.filter { $0 == char1 }.count
    return int1 <= count && count <= int2
  }

  var passingTest2: Bool {
    let count = password.enumerated().filter { (n, c) in
      c == char1 && (n + 1 == int1 || n + 1 == int2)
    }.count
    return count == 1
  }

}
