struct Problem202016: Problem {
  var name: String { "2020-16" }
  func solveWith(data: [String]) -> Solution { Solution202016(data: data) }
}

struct Solution202016: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    guard let puzzle = Puzzle(input: data) else { return -1 }
    print(puzzle.validTickets)
    return puzzle.scanningErrorRate
  }

  var answer2: Int {
    //guard let puzzle = Puzzle(input: data) else { return -1 }
    return -1
  }

}

struct Puzzle {

  typealias Ticket = [Int]
  typealias TRange = (ClosedRange<Int>,ClosedRange<Int>)

  let tickets: [Ticket]
  let myTicketNumber = 0
  let ranges: [String: TRange]
  // The names in ranges in the order found on the tickets
  var fieldOrder = [String]()

  // init?(input: [String]) {
  //   ranges = [
  //     "class": (1...3, 5...7),
  //     "row": (6...11, 33...44),
  //     "seat": (13...40, 45...50)
  //   ]
  //   tickets = [
  //     [7,1,14],
  //     [7,3,47],
  //     [40,4,50],
  //     [55,2,20],
  //     [38,6,12]
  //   ]
  // }

  init?(input: [String]) {
    var myRanges = [String: TRange]()
    var myTickets = [Ticket]()
    var inRules = true
    for line in input {
      if line == "" || line.starts(with: "your") || line.starts(with: "nearby") {
        inRules = false
        continue
      }
      if inRules {
        if let (name, ranges) = line.asTRule {
          myRanges[name] = ranges
        }
      } else {
        myTickets.append(line.asTicket)
      }
    }
    ranges = myRanges
    tickets = myTickets
  }


  var scanningErrorRate: Int {
    return invalidOtherFields.reduce(0, +)
  }

  var invalidOtherFields: [Int] {
    let invalids = otherTickets.map { invalidFields($0) }
    return invalids.reduce([], +) //Flatten [[Int]] -> [Int]
  }

  var myTicket: [Int] {
    return tickets[myTicketNumber]
  }

  var otherTickets: Array<[Int]>.SubSequence {
    tickets.dropFirst()
  }

  func invalidFields(_ ticket: Ticket) -> [Int] {
    return ticket.filter { !valid(field: $0) }
  }

  func valid(field: Int) -> Bool {
    for (range1, range2) in ranges.values {
      if range1.contains(field) || range2.contains(field) { return true }
    }
    return false
  }

  var validTickets: [Ticket] {
    return tickets.filter { invalidFields($0).count == 0 }
  }

}

extension String {
  var asTicket: Puzzle.Ticket {
    return self.split(separator: ",").compactMap { Int($0) }
  }

  var asTRule: (String, Puzzle.TRange)? {
    let parts1 = self.split(separator: ":")
    guard parts1.count == 2 else { return nil }
    let name = String(parts1[0])
    let parts2 = parts1[1].filter { $0 != " " && $0 != "r" }.split(separator: "o")
    guard parts2.count == 2 else { return nil }
    let parts3 = parts2[0].split(separator: "-")
    let parts4 = parts2[1].split(separator: "-")
    guard parts3.count == 2, parts4.count == 2 else { return nil }
    guard let int1 = Int(parts3[0]), let int2 = Int(parts3[1]),
    let int3 = Int(parts4[0]), let int4 = Int(parts4[1]) else { return nil}
    return (name,(int1...int2, int3...int4))
  }

}