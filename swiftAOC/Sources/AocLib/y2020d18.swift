struct Problem202018: Problem {
  var name: String { "2020-18" }
  func solveWith(data: [String]) -> Solution { Solution202018(data: data) }
}

struct Solution202018: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let expressions = data.map { Expression(def:$0) }
    let results = expressions.compactMap { $0.value }
    return results.reduce(0, +)
  }

  var answer2: Int {
    return -1
  }

}

struct Expression {

  let def: String

  var value: Int? {
    let evaluator = Evaluator()
    for char in def {
      switch char {
      case " ":
        break
      case "(":
        guard evaluator.push(.left) else { return nil }
        break
      case ")":
        guard evaluator.push(.right) else { return nil }
        break
      case "*":
        guard evaluator.push(.multiply) else { return nil }
        break
      case "+":
        guard evaluator.push(.add) else { return nil }
        break
      case "0"..."9":
        // assume a digit (0-9); i.e. no numbers > 9, no negative numbers
        // otherwise we would start a number builder that would end at next space
        guard let num = Int(String(char)) else { return nil }
        guard evaluator.push(.number(num)) else { return nil }
        break
      default:
        return nil
      }
    }
    return evaluator.value
  }

  class Evaluator {

    var stack = [Exp]()

    var value: Int? {
      guard !stack.isEmpty, case let .number(value) = stack[0] else { return nil }
      return value
    }

    func push(_ exp: Exp) -> Bool {
      switch exp {
      case .left:
        if stack.isEmpty {
          stack.append(exp)
        } else {
          switch stack.last! {
          case .left, .add, .multiply :
            stack.append(exp)
            break
          default:
            return false
          }
        }
        break
      case .add, .multiply:
        guard !stack.isEmpty else { return false }
        switch stack.last! {
        case .number(_):
          stack.append(exp)
          break
        default:
          return false
        }
        break
      case .right:
        // Error if the top of the stack does not contain (, number
        // pop twice and push number
        guard case let .number(num) = stack.popLast(), case .left = stack.popLast() else { return false }
        return self.push(.number(num))
      case .number(let value):
        if stack.isEmpty {
          stack.append(exp)
        } else {
          switch stack.last! {
          case .left:
            stack.append(exp)
            break
          case .add:
            // error if top not num, .add;  pop num do add push result
            guard case .add = stack.popLast(), case let .number(num) = stack.popLast() else { return false }
            return self.push(.number(value + num))
          case .multiply:
            // error if top not num, .multiply;  pop num do add push result
            guard case .multiply = stack.popLast(), case let .number(num) = stack.popLast() else { return false }
            return self.push(.number(value * num))
          default: return false
          }
        }
        break
      }
      return true
    }

  }

  enum Exp {
    case number(Int)
    case add
    case multiply
    case left
    case right
  }

}