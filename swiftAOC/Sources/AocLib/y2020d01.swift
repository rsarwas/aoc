struct Problem202001: Problem {
  var name: String { "2020-01" }
  func solveWith(data: [String]) -> Solution { Solution202001(data: data) }
}

struct Solution202001: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let nums = data.map { Int($0) ?? 0 }
    for num1 in nums {
      for num2 in nums {
        if num1 + num2 == 2020 { return num1 * num2 }
      }
    }
    return 0
  }

  var answer2: Int {
    let nums = data.map { Int($0) ?? 0 }
    for num1 in nums {
      for num2 in nums {
        let num = num1 + num2
        if num >= 2020 { continue }
        for num3 in nums {
          if num + num3 == 2020 { return num1 * num2 * num3 }
        }
      }
    }
    return 0
  }

}
