struct Problem202006: Problem {
  var name: String { "2020-06" }
  func solveWith(data: [String]) -> Solution { Solution202006(data: data) }
}

struct Solution202006: Solution {
  let data: [String]

  var part1: String {
    return "\(answer)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer: Int {
    return data.asGroups.map { $0.countYes }.reduce(0) { $0 + $1 }
  }

  var answer2: Int {
    return data.asGroups.map { $0.countAllYes }.reduce(0) { $0 + $1 }
    }

}

extension Array where Element == String {
  var asGroups: [Group] {
    var groups = [Group]()
    var answers = [String]()
    for line in self {
      if line == "" {
        groups.append(Group(answers: answers))
        answers.removeAll()
        continue
      }
      answers.append(line)
    }
    if answers.count > 0 {
      // In case there is no blank line at the end of the file
      groups.append(Group(answers: answers))
    }
    return groups
  }
}

struct Group {
  let answers: [String]

  var countYes: Int {
    let empty = Set<Character>()
    return answers.map { Set($0) }.reduce(empty) { $0.union($1) }.count
  }

  var countAllYes: Int {
    let all = Set("abcdefghijklmnopqrstuvwxyz")
    return answers.map { Set($0) }.reduce(all) { $0.intersection($1) }.count
  }

}
