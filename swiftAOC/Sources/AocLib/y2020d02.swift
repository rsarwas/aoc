import Foundation
struct Problem202002: Problem {
  var name: String { "2020-02" }
  func solveWith(data: [String]) -> Solution { Solution202002(data: data) }
}

struct Solution202002: Solution {
  let data: [String]

  var part1: String {
    //let answer = "Not Implemented"
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    var validPasswordCount = 0
    for record in data {
      var parts = record.split(separator: ":")
      let policy = parts[0]
      let password = parts[1]
      parts = policy.split(separator: " ")
      let range = parts[0]
      let neededChar = parts[1].first
      parts = range.split(separator: "-")
      let minimum = Int(parts[0]) ?? 9999
      let maximum = Int(parts[1]) ?? -1
      let neededChars = password.filter { $0 == neededChar }
      password.unicodeScalars
      if neededChars.count >= minimum && neededChars.count <= maximum {
        validPasswordCount += 1
      }
    }
    return validPasswordCount
  }

  var answer2: Int {
    var validPasswordCount = 0
    for record in data {
      var parts = record.split(separator: ":")
      let policy = parts[0]
      let password = String(parts[1]).trimmingCharacters(in: .whitespacesAndNewlines)
      parts = policy.split(separator: " ")
      let range = parts[0]
      let neededChar = parts[1].first!
      parts = range.split(separator: "-")
      let minimum = -1 + (Int(parts[0]) ?? 9999)
      let maximum = -1 + (Int(parts[1]) ?? -1)
      let index1 = password.index(password.startIndex, offsetBy: minimum)
      let index2 = password.index(password.startIndex, offsetBy: maximum)
      //print("Policy \(policy): Search \(password) for \(neededChar), first: \(password[index1]), second: \(password[index2])")
      var found = 0
      if password[index1] == neededChar { found += 1 }
      if password[index2] == neededChar { found += 1 }
      if found == 1 {
        validPasswordCount += 1
      }
    }
    return validPasswordCount
  }

}
