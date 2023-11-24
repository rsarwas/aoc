struct Problem202008: Problem {
  var name: String { "2020-08" }
  func solveWith(data: [String]) -> Solution { Solution202008(data: data) }
}

struct Solution202008: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let instructions = data.compactMap { Instruction($0) }
    let computer = Computer(code: instructions)
    let (status, result) = computer.run(enableLoopDetection: true)
    // print(status)
    return status == .loop ? result : -1
  }
  var answer2: Int {
    let instructions = data.compactMap { Instruction($0) }
    for (n, i) in instructions.enumerated() {
      var modifiedCode = instructions
      switch i {
      case .nop(let a):
        modifiedCode[n] = .jmp(a)
        break
      case .jmp(let a):
        modifiedCode[n] = .nop(a)
        break
      case .acc: break
      }
      let computer = Computer(code: modifiedCode)
      let (status, result) = computer.run(enableLoopDetection: true)
      if status == .success { return result }
      if status == .error { return result }
    }
    return -1
  }
}

struct Computer {
  let code: [Instruction]
  func run(enableLoopDetection: Bool = false) -> (Status, Int) {
    var visited = Set<Int>()
    var pc: Int = 0
    var acc: Int = 0
    while true {
      if pc < 0 || code.count < pc { return (.error, acc) }
      if pc == code.count { return (.success, acc) }
      if enableLoopDetection {
        if visited.contains(pc) { return (.loop, acc) }
        visited.insert(pc)
      }
      switch code[pc] {
      case .nop:
        pc += 1
        break
      case .acc(let n):
        acc += n
        pc += 1
        break
      case .jmp(let n):
        pc += n
        break
      }
      //print ("pc: \(pc), acc: \(acc)")
    }
  }
}

enum Status {
  case error
  case success
  case loop
}

enum Instruction {
  case nop(Int)
  case jmp(Int)
  case acc(Int)
}

extension Instruction {
  init?(_ text: String) {
    let parts = text.split(separator: " ")
    guard parts.count == 2 else { return nil }
    guard let num = Int(parts[1]) else { return nil }
    switch parts[0] {
    case "nop": self = .nop(num)
    case "acc": self = .acc(num)
    case "jmp": self = .jmp(num)
    default: return nil
    }
  }
}
