struct Problem201804: Problem {
  var name: String { "2018-04" }
  func solveWith(data: [String]) -> Solution { Solution201804(data: data) }
}

struct Solution201804: Solution {
  let data: [String]

  var part1: String {
    let guardLog = data.compactMap { $0.asLogRecord }
    guard let sleepestGuard = guardLog.guards.sleepest else { return "-1" }
    guard let sleepestMinute = sleepestGuard.maxSleepMinute else { return "-2" }
    return "\(sleepestGuard.id * sleepestMinute)"
  }

  var part2: String {
    let answer = "Not Implemented"
    return "\(answer)"
  }

}

struct LogRecord {
  enum Action {
    case sleep, wake
  }
  let timestamp: TimeStamp
  let guardId: Int?
  let action: Action?
}

struct Guard {
  let id: Int
  let naps: [Nap]
}

struct Nap {
  let start: TimeStamp
  let end: TimeStamp
  var duration: Int {
    // for this puzzle, all naps start and end in hour 00 of the same day
    return end.minute - start.minute
  }
}

struct TimeStamp {
  let year: Int
  let month: Int
  let day: Int
  let hour: Int
  let minute: Int
}

extension String {
  var asLogRecord: LogRecord? {
    let timestamp = TimeStamp(year: 1, month: 2, day: 3, hour: 4, minute: 5)
    let logRecord = LogRecord(timestamp: timestamp, guardId: 1, action: nil)
    return logRecord
  }
}

extension Array where Element == LogRecord {

  var guards: [Guard] {
    var guards = [Guard]()
    return guards
  }

}

extension Array where Element == Guard {

  var sleepest: Guard? {
    guard self.count > 0 else { return nil }
    return self[0]
  }

}

extension Guard {
  var maxSleepMinute: Int? {
    return nil
  }
}
