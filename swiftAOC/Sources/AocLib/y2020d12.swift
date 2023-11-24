import Darwin  // for atan2, sqrt, sin, cos

struct Problem202012: Problem {
  var name: String { "2020-12" }
  func solveWith(data: [String]) -> Solution { Solution202012(data: data) }
}

struct Solution202012: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let ship = Ship(instructions: data.compactMap { Move($0) })
    ship.move()
    return ship.manhattanDistance
  }

  var answer2: Int {
    let ship = Ship(instructions: data.compactMap { Move($0) })
    ship.move2()
    return ship.manhattanDistance
  }

}

class Ship {
  let instructions: [Move]
  let start: (Int, Int)
  var facing: Direction
  var location: (Int, Int)
  var waypoint: (Int, Int)

  init(instructions: [Move]) {
    self.instructions = instructions
    facing = .east
    start = (0, 0)
    location = (0, 0)
    waypoint = (10, 1)
  }

  func update(_ location: (Int, Int), _ direction: Direction, _ distance: Int) -> (Int, Int) {
    var newLocation = location
    switch direction {
    case .north:
      newLocation.1 = location.1 + distance
      break
    case .south:
      newLocation.1 = location.1 - distance
      break
    case .east:
      newLocation.0 = location.0 + distance
      break
    case .west:
      newLocation.0 = location.0 - distance
      break
    }
    return newLocation
  }

  func update2(_ location: (Int, Int), _ distance: Int) -> (Int, Int) {
    // move twords waypoint distance times
    let x = location.0 + (waypoint.0 * distance)
    let y = location.1 + (waypoint.1 * distance)
    return (x, y)
  }

  func move() {
    for move in instructions {
      switch move {
      case .cardinal(let direction, let distance):
        location = update(location, direction, distance)
        break
      case .right, .left:
        facing = facing.rotate(by: move)
        break
      case .forward(let distance):
        location = update(location, facing, distance)
        break
      }
    }
  }

  func move2() {
    for move in instructions {
      switch move {
      case .cardinal(let direction, let distance):
        waypoint = update(waypoint, direction, distance)
        break
      case .right, .left:
        rotateWaypoint(by: move)
        break
      case .forward(let distance):
        location = update2(location, distance)
        break
      }
    }
  }

  func rotateWaypoint(by move: Move) {
    let x = Double(waypoint.0)
    let y = Double(waypoint.1)
    let hyp = sqrt(x * x + y * y)
    var angle = atan2(y, x)
    switch move {
    case .right(let rotation):
      angle = angle - (Double(rotation.rawValue) * Double.pi / 180)
    case .left(let rotation):
      angle = angle + (Double(rotation.rawValue) * Double.pi / 180)
    default:
      break
    }
    waypoint.0 = Int((hyp * cos(angle)).rounded())
    waypoint.1 = Int((hyp * sin(angle)).rounded())
  }

  var manhattanDistance: Int {
    return abs(location.0 - start.0) + abs(location.1 - start.1)
  }
}

enum Direction: Int {
  case north = 0
  case east = 90
  case south = 180
  case west = 270
}

extension Direction {
  func rotate(by move: Move) -> Direction {
    var angle: Int
    switch move {
    case .right(let rotation):
      angle = self.rawValue + rotation.rawValue
    case .left(let rotation):
      angle = self.rawValue - rotation.rawValue
    default:
      return self
    }
    var facing: Direction?
    if angle < 0 {
      facing = Direction(rawValue: angle + 360)
    } else if 360 <= angle {
      facing = Direction(rawValue: angle - 360)
    } else {
      facing = Direction(rawValue: angle)
    }
    if facing == nil {
      print("WARNING: Invalid rotation, \(self), \(move), \(angle)")
    }
    return facing ?? self
  }
}

enum Angle: Int {
  case a90 = 90
  case a180 = 180
  case a270 = 270
}

enum Move {
  case forward(Int)
  case left(Angle)
  case right(Angle)
  case cardinal(Direction, Int)
}

extension Move {
  init?(_ instruction: String) {
    guard let code = instruction.first else { return nil }
    guard let distance = Int(instruction.dropFirst()) else { return nil }
    switch code {
    case "F":
      self = .forward(distance)
      break
    case "L":
      guard let angle = Angle(rawValue: distance) else { return nil }
      self = .left(angle)
      break
    case "R":
      guard let angle = Angle(rawValue: distance) else { return nil }
      self = .right(angle)
      break
    case "N":
      self = .cardinal(.north, distance)
      break
    case "S":
      self = .cardinal(.south, distance)
      break
    case "E":
      self = .cardinal(.east, distance)
      break
    case "W":
      self = .cardinal(.west, distance)
      break
    default: return nil
    }
  }
}
