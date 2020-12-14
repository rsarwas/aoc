struct Problem202013: Problem {
  var name: String { "2020-13" }
  func solveWith(data: [String]) -> Solution { Solution202013(data: data) }
}

struct Solution202013: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    guard data.count == 2 else { return -3 }
    guard let etd = Int(data[0]) else { return -2 }
    let ids = data[1].split(separator: ",")
    let buses = ids.compactMap { Bus(id: String($0)) }
    var minWaitTime = Int.max
    var solution = -1
    for bus in buses {
      let delay = bus.timeToDeparture(etd: etd)
      if delay < minWaitTime { minWaitTime = delay; solution = bus.id * delay }
    }
    return solution
  }

  var answer2: Int {
    guard let buses = data.buildBuses else { return -1 }
    //print(buses)
    // buses is [(arrivalDelay, loopTime)] both are Ints
    // a happyBus has startTime + arrivalDelay a multiple of loopTime
    // initialize startTime to make the slowest bus happy
    let (delayOfMax, maxLoop) = buses.reduce((0,0)) { $0.1 < $1.1 ? $1 : $0 }
    var startTime = maxLoop - delayOfMax
    //print(startTime)
    var increment = maxLoop
    //print(increment)
    var countOfHappyBuses = 1
    while countOfHappyBuses < buses.count {
      startTime += increment
      let loopTimes = happyLoopTimes(buses, at: startTime)
      if countOfHappyBuses < loopTimes.count {
        countOfHappyBuses = loopTimes.count
        //optimize by increasing the increment (should find a solution but may not be minimal)
        increment = loopTimes.reduce(1) { lcm($0, $1) }
        //print("t:\(startTime); c: \(countOfHappyBuses); inc:\(increment)")
      }
    }
    return startTime
  }

  func happyLoopTimes(_ buses: [(Int,Int)], at startTime: Int) -> [Int] {
    return buses.filter { (startTime + $0.0) % $0.1 == 0 }.map { $0.1 }
  }

  /*
  Returns the Greatest Common Divisor of two numbers.
  */
  func gcd(_ x: Int, _ y: Int) -> Int {
      var a = 0
      var b = max(x, y)
      var r = min(x, y)

      while r != 0 {
          a = b
          b = r
          r = a % b
      }
      return b
  }

  /*
  Returns the least common multiple of two numbers.
  */
  func lcm(_ x: Int, _ y: Int) -> Int {
      return x / gcd(x, y) * y
  }

}

struct Bus {
  let id: Int

  init?(id: String) {
    guard let nid = Int(id) else { return nil }
    self.id = nid
  }

  func timeToDeparture(etd: Int) -> Int {
    return id - (etd % id)
  }

}

extension Array where Element == String {
  var buildBuses: [(Int,Int)]? {
    // where bus := (Int,Int) == (arrivalDelay, loopTime)
    guard self.count == 2 else { return nil }
    let ids = self[1].split(separator: ",").map { String($0) }
    let buses = ids.enumerated().compactMap { (i,s) in
      guard let n = Int(s) else { return nil }
      return (i,n)
    } as [(Int,Int)]
    return buses
  }
}