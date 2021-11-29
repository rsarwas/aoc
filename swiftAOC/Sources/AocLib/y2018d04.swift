struct Problem201804: Problem {
  var name: String { "2018-04" }
  func solveWith(data: [String]) -> Solution { Solution201804(data: data) }
}

struct Solution201804: Solution {
  let data: [String]

  var part1: String {
    let guardLog = data.compactMap { $0.asLogRecord }
    guard let sleepiestGuard = guardLog.guards.sleepiest else { return "-1" }
    guard let sleepiestMinute = sleepiestGuard.maxSleepMinute else { return "-2" }
    return "\(sleepiestGuard.id * sleepiestMinute)"
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
    guard self.count > 0 else { return guards }
    // print("Total Log records = \(self.count)")
    // for (i, log) in self.enumerated() {
    //     print ("Log \(i): guard \(log.guardId), Action \(log.action)")
    // }
    // we need the logs sorted by guard and then timestamp to create a complete guard
    // However only the start log has a guard id, so we cannot sort by guard and timestamp
    let logs = self.sorted { $0.timestamp < $1.timestamp }
    // print("paritially sorted log records = \(logs.count)")
    // for (i, log) in logs.enumerated() {
    //     print ("Log \(i): guard \(log.guardId), Action \(log.action)")
    // }
    guard logs.count > 0, logs[0].action == LogRecord.Action.start else { return guards }
    guard var currentId = logs[0].guardId else { return guards }
    let logs2:[LogRecord] = logs.map { log in 
        if log.guardId != nil {
            currentId = log.guardId!
            return log
        } else {
            return LogRecord(timestamp: log.timestamp, guardId: currentId, action: log.action)
        }
    }.sorted {
        guard let g1 = $0.guardId, let g2 = $1.guardId else { return $0.timestamp < $1.timestamp }
        if g1 == g2 {
            return $0.timestamp < $1.timestamp
        } else {
            return g1 < g2 
        }
    }
    // print("Fully sorted log records = \(logs.count)")
    // for (i, log) in logs2.enumerated() {
    //     print ("Log \(i): guard \(log.guardId), Action \(log.action), Time: \(log.timestamp)")
    // }
    var startIndex = 0
    var guardId = logs2[0].guardId
    for i in 1..<logs.count {
        if guardId != logs2[i].guardId {
            //print("Build Guard with indices (\(startIndex),\(i-1)) from Logs[\(logs.count)]")
            if let sentry = Guard.build(logs: logs2[startIndex..<i]) {
                guards.append(sentry)
            }
            guardId = logs2[i].guardId
            startIndex = i
        }
        if i == logs2.count - 1 {
            // Close out the last sentry
            //print("Build last guard with indices (\(startIndex),\(i)) from Logs[\(logs.count)]")
            if let sentry = Guard.build(logs: logs2[startIndex...i]) {
                guards.append(sentry)
            }
            guardId = logs2[i].guardId
            startIndex = i
        }
    }
    return guards
  }

}

extension Array where Element == Guard {

  var sleepiest: Guard? {
    guard self.count > 0 else { return nil }
    var winner: Guard? 
    var maxNaptime = 0
    for sentry in self {
        let naptime = sentry.naps.reduce(0) {$0 + $1.duration}
        //print("Guard \(sentry.id) has \(sentry.naps.count) naps for \(naptime) minutes")
        if naptime > maxNaptime { 
            maxNaptime = naptime
            winner = sentry
        }

    }
    return winner
  }

}

extension Guard {
  var maxSleepMinute: Int? {

      var minuteCounts = Array(repeating: 0, count: 60)
      for nap in naps {
          for i in (nap.start.minute..<nap.end.minute) {
              minuteCounts[i] += 1
          }
      }
      //print("Minute counts: \(minuteCounts)")
      var sleepiestMinute = -1
      var sleepiestCount = 0
      for minute in 0..<60 {
          if minuteCounts[minute] > sleepiestCount {
              sleepiestMinute = minute
              sleepiestCount = minuteCounts[minute]
          }
      }
    return sleepiestMinute
  }

  static func build(logs: ArraySlice<LogRecord>) -> Guard? {
      guard logs.count > 0 else { return nil }
      var maybeId: Int?
      var maybeStart: TimeStamp?
      var naps = [Nap]()
      for log in logs {
          if log.action == LogRecord.Action.start {
               maybeId = log.guardId
               if maybeStart != nil {
                   print("Warning The guard was still asleep at the end of his previous shift")
               }
          }
          if log.action == LogRecord.Action.sleep {
               maybeStart = log.timestamp
          }
          if log.action == LogRecord.Action.wake {
            guard let start = maybeStart else { continue }
            let end = log.timestamp
            naps.append(Nap(start: start, end: end))
            maybeStart = nil
          }
      }
      guard let id = maybeId else { return nil }
      return Guard(id: id, naps: naps)
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