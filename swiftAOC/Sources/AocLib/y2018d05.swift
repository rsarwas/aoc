struct Problem201805: Problem {
  var name: String { "2018-05" }
  func solveWith(data: [String]) -> Solution { Solution201805(data: data) }
}

struct Solution201805: Solution {
  let data: [String]

  var part1: String {
    guard data.count == 1 else { return "-1" }
    let polymer = data[0].asPolymer
    //print("Polymer = \(polymer)")
    let simplePolymer = polymer.simplify()
    //print("Simple Polymer = \(simplePolymer)")
    return "\(simplePolymer.count)"
  }

  var part2: String {
    let answer = "Not Implemented"
    return "\(answer)"
  }

}

typealias Polymer = [UInt8]

extension String {

  var asPolymer: Polymer {
    return Array(self.utf8)
    //return [65, 66, 67, 99, 98, 68]
  }

}

extension Array where Element == UInt8 {
  func simplify() -> Polymer {
    let delta: UInt8 = "a".utf8.first! - "A".utf8.first!
    func match(_ a: UInt8, _ b: UInt8) -> Bool {
      // fortunately Z + delta is still a UInt8, so we do not need to worry about overflow
      if a > b {
        return b + delta == a
      } else {
        return a + delta == b
      }
    }
    var d = self  // copy and mutate
    var s = 0
    var e = 1
    while e < d.count {
      if match(d[s], d[e]) {
        //print("Match \(s) = \(d[s]); \(e) = \(d[e])")
        // clear/move aka copy and clear
        d[s] = 0
        d[e] = 0
        if e + 1 < d.count {
          d[s] = d[e + 1]
          d[e + 1] = 0
          e += 2
        } else {
          e += 1
        }
        // If s is beyond the first character,
        // since d[s] is new, check if we created a match at s and s-1
        // No need to loop since we can only match backwards once.
        // (The next iteration of the main loop may move s backwards some more)
        if s > 0 {
          if match(d[s], d[s - 1]) {
            //print("Match back at \(s-1) = \(d[s-1]); \(s) = \(d[s])")
            d[s] = 0
            d[s - 1] = 0
            if s > 1 {
              s -= 2
            } else {
              // we just cleared the start of the string;
              // so move d[e] to d[s=0] before the next loop
              s -= 1
              if e < count {
                d[s] = d[e]
                e += 1
              }
            }
          }
        }
      } else {
        s += 1
        if e > s {
          d[s] = d[e]
          d[e] = 0
        }
        e += 1
      }
      //print("s = \(s); e = \(e); d = \(d)")
    }
    //print("s = \(s); e = \(e); d = \(d)")
    return Array(d[0...s])
  }

}
