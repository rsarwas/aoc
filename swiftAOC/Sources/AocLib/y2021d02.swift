struct Problem202102: Problem {
  var name: String { "2021-02" }
  func solveWith(data: [String]) -> Solution { Solution202102(data: data) }
}

struct Solution202102: Solution {
  let data: [String]

  var part1: String {
    let commands = data.compactMap { $0.asCommand }
    let initialLocation: SubLocation = (distance: 0, depth: 0)
    let location: SubLocation = commands.reduce(initialLocation) { (currentLocation, command) in
      return newLocation(location: currentLocation, command: command)
    }
    let answer = location.distance * location.depth
    return "\(answer)"
  }

  var part2: String {
    let commands = data.compactMap { $0.asCommand }
    let initialLocation: SubLocation2 = (distance: 0, depth: 0, aim: 0)
    let location: SubLocation2 = commands.reduce(initialLocation) { (currentLocation, command) in
      return newLocation2(location: currentLocation, command: command)
    }
    let answer = location.distance * location.depth
    return "\(answer)"
  }

  func newLocation(location: SubLocation, command: SubCommand) -> SubLocation {
    switch command {
    case .Forward(let distance):
      return (distance: location.distance + distance, depth: location.depth)
    case .Up(let depth):
      return (distance: location.distance, depth: location.depth - depth)
    case .Down(let depth):
      return (distance: location.distance, depth: location.depth + depth)
    }
  }

  func newLocation2(location: SubLocation2, command: SubCommand) -> SubLocation2 {
    switch command {
    case .Forward(let x):
      return (
        distance: location.distance + x, depth: location.depth + (location.aim * x),
        aim: location.aim
      )
    case .Up(let aim):
      return (distance: location.distance, depth: location.depth, aim: location.aim - aim)
    case .Down(let aim):
      return (distance: location.distance, depth: location.depth, aim: location.aim + aim)
    }
  }

}

typealias SubLocation = (distance: Int, depth: Int)
typealias SubLocation2 = (distance: Int, depth: Int, aim: Int)

enum SubCommand {
  case Forward(Int)
  case Up(Int)
  case Down(Int)
}

extension String {
  var asCommand: SubCommand? {
    let commandParts = self.split(separator: " ")
    guard commandParts.count == 2 else { return nil }
    guard let distance = Int(commandParts[1]) else { return nil }
    switch commandParts[0] {
    case "forward":
      return .Forward(distance)
    case "up":
      return .Up(distance)
    case "down":
      return .Down(distance)
    default:
      return nil
    }
  }
}
