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
    case start, sleep, wake
  }
  let timestamp: TimeStamp
  let guardId: Int?
  let action: Action
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

// Swift's Date requires Foundation and does wierd things with the timezone
// We do not really need it anyway, besides this is more portable 
struct TimeStamp {
  let year: Int
  let month: Int
  let day: Int
  let hour: Int
  let minute: Int
}

extension String {
  var asLogRecord: LogRecord? {
    // Examples:
    //  "[1518-11-03 00:05] Guard #10 begins shift"
    //  "[1518-11-03 00:24] falls asleep"
    //  "[1518-11-03 00:29] wakes up"

    let dateAndRest = self.replacingOccurrences(of: "[", with: "").split(separator: "]")
    guard dateAndRest.count == 2 else { return nil }
    guard let timestamp = String(dateAndRest[0]).asTimeStamp else { return nil }
    let rest = dateAndRest[1]
    if rest.hasPrefix(" wakes up") {
      return LogRecord(timestamp: timestamp, guardId: nil, action: LogRecord.Action.wake)
    }
    if rest.hasPrefix(" falls asleep") {
      return LogRecord(timestamp: timestamp, guardId: nil, action: LogRecord.Action.sleep)
    }
    if rest.hasPrefix(" Guard #") {
      let idString = rest.replacingOccurrences(of: " Guard #", with: "")
        .replacingOccurrences(of: " begins shift", with: "")
      guard let id = Int(idString) else { return nil }
      return LogRecord(timestamp: timestamp, guardId: id, action: LogRecord.Action.start)
    }
    return nil
  }

  var asTimeStamp: TimeStamp? {
    let dateAndTime = self.split(separator: " ")
    guard dateAndTime.count == 2 else { return nil }
    let dateParts = dateAndTime[0].split(separator: "-")
    guard dateParts.count == 3 else { return nil }
    guard let year = Int(dateParts[0]) else { return nil }
    guard let month = Int(dateParts[1]) else { return nil }
    guard let day = Int(dateParts[2]) else { return nil }
    let timeParts = dateAndTime[1].split(separator: ":")
    guard timeParts.count == 2 else { return nil }
    guard let hour = Int(timeParts[0]) else { return nil }
    guard let minute = Int(timeParts[1]) else { return nil }
    return TimeStamp(year: year, month: month, day: day, hour: hour, minute: minute)
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


extension TimeStamp: Comparable {

    static func < (lhs: TimeStamp, rhs: TimeStamp) -> Bool {
        if lhs.year != rhs.year {
            return lhs.year < rhs.year
        } else if lhs.month != rhs.month {
            return lhs.month < rhs.month
        } else if lhs.day != rhs.day {
            return lhs.day < rhs.day
        } else if lhs.hour != rhs.hour {
            return lhs.hour < rhs.hour
        } else {
            return lhs.minute < rhs.minute
        }
    }

    static func == (lhs: TimeStamp, rhs: TimeStamp) -> Bool {
        return lhs.year == rhs.year && lhs.month == rhs.month
            && lhs.day == rhs.day && lhs.hour == rhs.hour
            && lhs.minute == rhs.minute
    }

}