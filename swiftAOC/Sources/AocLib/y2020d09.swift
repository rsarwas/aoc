struct Problem202009: Problem {
  var name: String { "2020-09" }
  func solveWith(data: [String]) -> Solution { Solution202009(data: data, testing: false) }
}

struct Solution202009: Solution {
  let data: [String]
  let testing: Bool

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let preamble = testing ? 5 : 25
    let numbers = data.compactMap { Int($0) }
    for n in preamble..<numbers.count {
      var found = false
      preambleLoop: for i in n-preamble..<n-1 {
        for j in i+1..<n {
          if numbers[i] != numbers[j] && numbers[i] + numbers[j] == numbers[n] {
            found = true
            break preambleLoop
          }
        }
      }
      if !found {
        return numbers[n]
      }
    }
    return -1
  }

  var answer2: Int {
    let target = answer1
    let numbers = data.compactMap { Int($0) }
    for n1 in 1..<numbers.count-1 {
      var total = numbers[n1]
      var minimum = total
      var maximum = total
      for n2 in n1+1..<numbers.count {
        //print("\(n1), \(n2), \(numbers.count)")
        total += numbers[n2]
        if total > target { break }
        if numbers[n2] < minimum { minimum = numbers[n2] }
        if maximum < numbers[n2] { maximum = numbers[n2] }
        if total == target { return minimum + maximum}
      }
    }
    return -1
  }

}
