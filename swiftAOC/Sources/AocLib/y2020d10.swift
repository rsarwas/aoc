struct Problem202010: Problem {
  var name: String { "2020-10" }
  func solveWith(data: [String]) -> Solution { Solution202010(data: data) }
}

struct Solution202010: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let adapters = data.compactMap { Int($0) }.sorted()
    var count1 = adapters[0] == 1 ? 1 : 0
    var count3 = adapters[0] == 3 ? 1 : 0
    var a = adapters.first!
    for b in adapters.dropFirst() {
      if b - a == 1 { count1 += 1 }
      if b - a == 3 { count3 += 1 }
      a = b
    }
    count3 += 1  // last adapter to the device
    return count1 * count3
  }

  var answer2: Int {
    let adapters = data.compactMap { Int($0) }.sorted()
    let adapters2 = [0] + adapters + [adapters.last! + 3]
    //print(adapters2)
    return countPermutations(adapters2)
  }

  func countPermutationsRecursive(_ list: [Int]) -> Int {
    if list.count == 0 { return 0 }
    if list.count == 1 { return 1 }
    var total = 0
    if list.count > 1 && list[1] - list[0] < 4 {
      total += countPermutations(Array(list.dropFirst(1)))
    }
    if list.count > 2 && list[2] - list[0] < 4 {
      total += countPermutations(Array(list.dropFirst(2)))
    }
    if list.count > 3 && list[3] - list[0] < 4 {
      total += countPermutations(Array(list.dropFirst(3)))
    }
    return total
  }

  func countPermutations(_ list: [Int]) -> Int {
    // The recursive solution recalulates each leaf of the tree independently
    // This is super duper inefficent when there are trillions of leafs, and
    // We know what the answer is.  If we know the answer to the leaf, we know
    // answer to the parent of the leaf, and so on.
    if list.count == 0 { return 0 }
    if list.count == 1 { return 1 }
    var cnts = [Int](repeating: 0, count: list.count)
    cnts[list.count - 1] = 1
    // examine the list from the end to the beginning
    // for each item in list, cnt is the total of the
    // cnt of each item ahead of it that it can reach
    var i = list.count - 2
    while 0 <= i {
      var j = i + 1
      while j < list.count && list[j] - list[i] <= 3 {
        cnts[i] += cnts[j]
        j += 1
      }
      i -= 1
    }
    return cnts[0]
  }

}
