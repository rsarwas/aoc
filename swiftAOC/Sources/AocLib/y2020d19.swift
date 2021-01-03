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
    let dataParts = data.split(separator: "")
    let parser = Parser(ruleText:dataParts[0])
    // for testing:
    // for message in dataParts[1] {
    //   print("message:\"\(message)\"")
    //   print("isValid: \(parser.isValid2(message: message))")
    // }
    // return -1
    return dataParts[1].filter({parser.isValid2(message: $0)}).count
  }

}

import Foundation // for String.splitOnOccurence
class Parser {

  var rules: [RuleId:Rule]
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

  func isValid2(message: String) -> Bool {
    // In the original problem 0 -> 8 11; 8 -> 42; 11 -> 42 31
    // or put another way: 0 ->  42 42 31
    // No other rules call 8, 11, 31 or 42 (in test or real input)
    // With the new recursive rule change 8 -> 42 | 42 8 (i.e. one or more 42s)
    // and 11 -> 42 31 | 42 11 31 (i.e  a sequence of n 42 followed by n 31)
    // Therefore rule 0 is now a sequence of n 42 followed by m 31
    // where 2 < n and 0 < m < n
    // The original solver does not work because it will only try the second branch
    // if the first one fails.  Consider 8: 42 | 42 8.  Since the second starts the same
    // as the first one it will never get called unless the first one failed, in which case
    // it will fail as well, but what we want to check the second option as well as
    // the first option. That is we need to be greedy on rule 42.
    // We could try repeating rule 42 until it fails, and then try rule 31 up to
    // n-1 times where n is the number of times we successfully matched rule 42.
    // However this fails because 42 42 42 ? may fail at ? while 42 42 31 is valid
    // Changing the rules to 8 -> 42 8 | 42 and 11 -> 31 11 | 11 will allow
    // nx 42 followed by mx 31; but m will not be bound to n-1, and it will
    // greedily consume the 42, when maybe it should stop ealier to look for 31.

    guard let rule42 = rules[42] else { return false }
    guard let rule31 = rules[31] else { return false }
    guard !message.isEmpty else { return false }
    self.message = message.reversed()
    if !isMessageValid(rule: rule42) { return false }
    var n = 1
    while true {
      let oldMessage = self.message
      let failMode = found(count1: n, rule1: rule42, count2: n, rule2: rule31)
      if failMode == .notn42 { return false }
      // if failMode == .no31 { print("fail: no 31s; keep trying")}
      if failMode == .ok {
        if self.message.isEmpty { return true }
      }
      n += 1
      self.message = oldMessage
    }
  }
  enum FailModes {
    case notn42
    case no31
    case ok
  }

  private func found(count1: Int, rule1: Rule, count2: Int, rule2: Rule) -> FailModes {
    for _ in 1...count1 {
      if !isMessageValid(rule: rule1) { return .notn42 }
    }
    for i in 1...count2 {
      if !isMessageValid(rule: rule2) {
        if i == 1 { return .no31 }
      }
    }
    return .ok
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
