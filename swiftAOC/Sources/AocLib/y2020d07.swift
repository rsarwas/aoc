import Foundation  // for componentsSeparatedByString()

struct Problem202007: Problem {
  var name: String { "2020-07" }
  func solveWith(data: [String]) -> Solution { Solution202007(data: data) }
}

struct Solution202007: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let rules = data.compactMap { $0.asRule }
    let ruleset = rules.asRuleSet
    guard var containers = ruleset["shiny gold"] else { return 0 }
    var colors = Set<String>()
    while containers.count > 0 {
      let containerCopy = containers.map { $0 }
      containers.removeAll()
      for color in containerCopy {
        colors.insert(color)
        if let newContainers = ruleset[color] {
          containers.formUnion(newContainers)
        }
      }
    }
    return colors.count
  }

  var answer2: Int {
    let rules = data.compactMap { $0.asRule }
    let ruleSet = rules.asRuleSet2
    // for rule in rules {
    //   print("color: \(rule.color) = \(rule.countBags(rules: ruleSet))")
    // }
    guard let rule = ruleSet["shiny gold"] else { return 0 }
    return rule.countBags(rules: ruleSet) - 1  // uncount the shiny gold bag
  }
}

struct Rule {
  let color: String
  let bags: [Bags]

  func countBags(rules: [String: Rule]) -> Int {
    var count = 1  // this bag
    for bag in bags {
      if let rule = rules[bag.color] {
        count += bag.quantity * rule.countBags(rules: rules)
      } else {
        print("color: \(color) not found")
      }
    }
    return count
  }
}

struct Bags {
  let quantity: Int
  let color: String
}

extension String {
  var asRule: Rule? {
    var bags = [Bags]()
    let parts = self.components(separatedBy: " bags contain ")
    guard parts.count == 2 else { return nil }
    let color = parts[0]
    if parts[1] == "no other bags." {
      return Rule(color: color, bags: bags)
    } else {
      let parts = parts[1].components(separatedBy: ", ")
      for part in parts {
        let cleanPart = part.replacingOccurrences(of: "bags", with: "")
          .replacingOccurrences(of: "bag", with: "").replacingOccurrences(of: ".", with: "")
        let pieces = cleanPart.split(separator: " ")
        guard pieces.count > 1, let count = Int(pieces[0]) else { continue }
        let color = pieces.dropFirst().joined(separator: " ")
        bags.append(Bags(quantity: count, color: color))
      }
    }
    //print("color: \(color); bags: \(bags)")
    return Rule(color: color, bags: bags)
  }
}

extension Array where Element == Rule {
  //ruleset is key is a bag color the value is all the bag colors that may directly contain it.
  var asRuleSet: [String: Set<String>] {
    var results = [String: Set<String>]()
    for rule in self {
      for bag in rule.bags {
        if results[bag.color] == nil {
          results[bag.color] = Set<String>()
        }
        results[bag.color]!.insert(rule.color)
      }
    }
    return results
  }

  var asRuleSet2: [String: Rule] {
    var ruleSet = [String: Rule]()
    for rule in self {
      ruleSet[rule.color] = rule
    }
    return ruleSet
  }
}
