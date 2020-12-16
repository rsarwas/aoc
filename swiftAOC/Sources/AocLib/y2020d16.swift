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
    guard let puzzle = Puzzle(input: data) else { return -1}
    return puzzle.scanningErrorRate
  }

  var answer2: Int {
    return -1
  }

}

struct Puzzle {

  let tickets: [Ticket]
  let myTicketNumber = 0
  let ranges: [String: (ClosedRange<Int>,ClosedRange<Int>)]

  init?(input: [String]) {
    ranges = [
      "class": (1...3, 5...7),
      "row": (6...11, 33...44),
      "seat": (13...40, 45...50)
    ]
    tickets = [
      [7,1,14],
      [7,3,47],
      [40,4,50],
      [55,2,20],
      [38,6,12]
    ]
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
    print(field)
    return false
  }

}

typealias Ticket = [Int]

extension Ticket {
}
