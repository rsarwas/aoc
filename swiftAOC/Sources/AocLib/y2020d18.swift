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
    let expressions = data.map { Expression(def: $0) }
    let results = expressions.compactMap { $0.value }
    return results.reduce(0, +)
  }

  var answer2: Int {
    let expressions = data.map { Expression2(def: $0) }
    let results = expressions.compactMap { $0.value }
    return results.reduce(0, +)
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
          case .left, .add, .multiply:
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
        guard case let .number(num) = stack.popLast(), case .left = stack.popLast() else {
          return false
        }
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
            guard case .add = stack.popLast(), case let .number(num) = stack.popLast() else {
              return false
            }
            return self.push(.number(value + num))
          case .multiply:
            // error if top not num, .multiply;  pop num do add push result
            guard case .multiply = stack.popLast(), case let .number(num) = stack.popLast() else {
              return false
            }
            return self.push(.number(value * num))
          default: return false
          }
        }
        break
      }
      return true
    }

  }
}

struct Expression2 {

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
    guard evaluator.reduceStack() else { return nil }
    return evaluator.value
  }

  class Evaluator {

    var stack = [Exp]()

    var value: Int? {
      guard !stack.isEmpty, case let .number(value) = stack[0] else { return nil }
      return value
    }

    func reduceStack() -> Bool {
      // called after all data is pushed into the evaluator, since there is no more data
      // coming, I can do any remaining multiplications until there is only a single element
      // on the stack. Any thing but multiplecations and numbers on the stack is an error
      if stack.isEmpty { return false }
      while stack.count > 1 {
        guard case let .number(n1) = stack.popLast(),
          case .multiply = stack.popLast(),
          case let .number(n2) = stack.popLast()
        else { return false }
        stack.append(.number(n1 * n2))
      }
      return stack.count == 1
    }

    func reduceParen() -> Bool {
      // called when a right paren is push and the top of the stack has .multiply, .number
      // I do all the multiplications until I find the left paren.  which is poped and
      // the result of the multiplication is pushed onto the stack
      // Any thing but multiplecations, numbers before the left paren on the stack is an error
      // as is finding the end of the stack before the left paren
      if stack.isEmpty { return false }
      while !stack.isEmpty {
        guard case let .number(n1) = stack.popLast(),
          case .multiply = stack.popLast(),
          case let .number(n2) = stack.popLast()
        else { return false }
        switch stack.last {
        case .left:
          let _ = stack.popLast()
          return self.push(.number(n1 * n2))
        case .multiply:
          stack.append(.number(n1 * n2))
          break
        default:
          return false
        }
      }
      // If I get here I never found the left paren
      return false
    }

    func push(_ exp: Exp) -> Bool {
      switch exp {
      case .left:
        if stack.isEmpty {
          stack.append(exp)
        } else {
          switch stack.last! {
          case .left, .add, .multiply:
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
        // option 1: only adds were pushed since "("; this reduces to just "(" & number on top of stack
        //   pop twice and push number
        // option 2: adds have been evaluated, but there is a sequence of multiplies since "("
        //   recduce the multiplies on the stack until we get to the "("
        guard case let .number(num) = stack.popLast(), let top = stack.last else { return false }
        switch top {
        case .left:
          let _ = stack.popLast()  //remove left paren
          return self.push(.number(num))
        case .multiply:
          stack.append(.number(num))
          return reduceParen()
        default:
          return false
        }
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
            guard case .add = stack.popLast(), case let .number(num) = stack.popLast() else {
              return false
            }
            return self.push(.number(value + num))
          case .multiply:
            // error if top not num, .multiply;  push new number (do multiply later)
            let _ = stack.popLast()  // .multiply
            guard case .number = stack.last else { return false }
            stack.append(.multiply)
            stack.append(exp)
            break
          default: return false
          }
        }
        break
      }
      return true
    }

  }
}

enum Exp {
  case number(Int)
  case add
  case multiply
  case left
  case right
}
