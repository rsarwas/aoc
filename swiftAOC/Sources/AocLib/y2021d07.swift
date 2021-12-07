struct Problem202107: Problem {
  var name: String { "2021-07" }
  func solveWith(data: [String]) -> Solution { Solution202107(data: data) }
}

struct Solution202107: Solution {
  let data: [String]

  var part1: String {
    let numbers = data[0].asCrabLoctions
    let answer = solve(numbers, with:linear_costs)
    return "\(answer)"
  }

   var part2: String {
    let numbers = data[0].asCrabLoctions
    let answer = solve(numbers, with:triangle_costs)
    return "\(answer)"
  }

  // This is a unit lookup array 0 => 0, 1 => 1, 2 =>2, ... 
  // It is silly and inefficient, but it is required for symetry
  // with the part two solver.  And the cost in time an memeory is insignificant.
  var linear_costs: [Int] {
    var unit = [Int](repeating: 0, count: 2000)
    for i in 1..<2000 {
        unit[i] = i
    }
    return unit
  }
  
  var triangle_costs: [Int] {
    var tri = [Int](repeating: 1, count: 2000)
    for i in 2..<2000 {
        tri[i] = i + tri[i-1]
    }
    return tri
  }
  
  func fuel_cost(_ numbers:[Int], _ target: Int, _ cost: [Int]) -> Int {
      numbers.map { cost[abs($0-target)] }.reduce(0,+)
  }
 
  func solve(_ numbers: [Int], with costs: [Int]) -> Int {
    // Brute force is faster to write, and nearly as fast to run
    // See python solution for a more computationally efficient solution
    // check all possible solutions, and return the best
    var min_cost = Int.max
    let min = numbers.min()! // fail immediately if there is no min or max
    let max = numbers.max()!
    for target in min...max {
        let new_cost = fuel_cost(numbers, target, costs)
        // print("target = \(target), cost = \(new_cost)")
        if new_cost < min_cost {
            min_cost = new_cost
        }
    }
    return min_cost
  }
}

extension String {
    var asCrabLoctions: [Int] {
        self.split(separator: ",").compactMap { Int($0)}
    }
}