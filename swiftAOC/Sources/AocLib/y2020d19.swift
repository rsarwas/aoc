struct Problem202019: Problem {
  var name: String { "2020-19" }
  func solveWith(data: [String]) -> Solution { Solution202019(data: data) }
}

struct Solution202019: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let dataParts = data.split(separator: "")
    let parser = Parser(ruleText:dataParts[0])
    // for message in dataParts[1] {
    //   print("message:\"\(message)\"")
    //   print("isValid: \(parser.isValid(message: message, ruleId: 0))")
    // }
    return dataParts[1].filter({parser.isValid(message: $0, ruleId: 0)}).count
  }

  var answer2: Int {
    return -1
  }

}

import Foundation // for String.splitOnOccurence
class Parser {

  let rules: [RuleId:Rule]
  var message: [Character]

  init(ruleText: Array<String>.SubSequence) {
    var rules = [RuleId:Rule]()
    for rule in ruleText {
      let parts = rule.components(separatedBy:": ")
      guard parts.count == 2 else { continue }
      guard let id = Int(parts[0]) else { continue }
      guard let newRule = Rule(parts[1]) else { continue }
      rules[id] = newRule
    }
    self.rules = rules
    // print(rules)
    self.message = [Character]()
  }

  func isValid(message: String, ruleId: RuleId) -> Bool {
    guard let rule = rules[ruleId] else { return false }
    guard !message.isEmpty else {return false }
    self.message = message.reversed()
    return isMessageValid(rule: rule) && self.message.isEmpty
  }

  private func isMessageValid(rule: Rule) -> Bool {
    //print(message, rule)
    guard !message.isEmpty else { return false }
    switch rule {
    case .id(let id):
      guard let newRule = rules[id] else { return false }
      return isMessageValid(rule: newRule)
    case .term(let char):
      if message.last == char {
        _ = message.popLast()
        return true
      } else {
        return false
      }
    case .seq(let rules):
      let savedMessage = message
      if rules.allSatisfy({isMessageValid(rule:$0)}) {
        return true
      } else {
        message = savedMessage
        return false
      }
    case .or(let r1, let r2):
      let savedMessage = message
      if isMessageValid(rule: r1) { return true }
      message = savedMessage
      if isMessageValid(rule: r2) { return true }
      message = savedMessage
      return false
    }
  }

  typealias RuleId = Int

  indirect enum Rule {
    case id(RuleId)
    case term(Character)
    case seq([Rule])
    case or(Rule, Rule)

    init?(_ rule: String) {
      if rule == "\"a\"" {
        self = .term("a")
      }
      else if rule == "\"b\"" {
        self = .term("b")
      }
      else if rule.contains("|") {
        let parts = rule.components(separatedBy:" | ")
        guard parts.count == 2 else { return nil }
        guard let r1 = Rule(parts[0]) else { return nil }
        guard let r2 = Rule(parts[1]) else { return nil }
        self = .or(r1, r2)
      } else {
        let ids = rule.split(separator:" ").compactMap { Int($0) }
        guard ids.count > 0 else { return nil }
        if ids.count == 0 {
          self = .id(ids[0])
        } else {
          self = .seq(ids.map { .id($0) })
        }
      }
    }
  }

}
