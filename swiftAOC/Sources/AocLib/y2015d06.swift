struct Problem201506: Problem {
  var name: String { "2015-06" }
  func solveWith(data: [String]) -> Solution { Solution201506(data: data) }
}

struct Solution201506: Solution {
  let data: [String]

  var part1: String {
    let instructions = data.compactMap { $0.asLightingInstruction }
    var grid = LightingGrid()
    for instruction in instructions {
      grid.update(instruction)
    }  
    let answer = grid.countLights
    return "\(answer)"
  }

  var part2: String {
    let instructions = data.compactMap { $0.asLightingInstruction }
    var grid = LightingGrid()
    for instruction in instructions {
      grid.updateV2(instruction)
    }  
    let answer = grid.countLights
    return "\(answer)"
  }

}

enum LightState {
  case On
  case Off
  case Toggle
}

struct LightInstruction {
  let state: LightState
  let lowerLeft: Coord2
  let upperRight: Coord2
}

struct LightingGrid {
  // Start with all the lights off (0)
  var lights = Array(repeating: Array(repeating: 0, count: 1000), count: 1000)

  // NOTE: I'm not sure of the best way to update large arrays.
  // However, updating the 1000x1000 matrix is slow with a debug build, but very fast with a release build
  mutating func update(_ instruction: LightInstruction) {
    let ll = instruction.lowerLeft
    let ur = instruction.upperRight
    let left = min(ll.x, ur.x)
    let right = max(ll.x, ur.x)
    let top = min(ll.y, ur.y)
    let bottom = max(ll.y, ur.y)
    for rowIndex in top...bottom {
      for columnIndex in left...right {
        switch instruction.state {
        case .On:
          lights[rowIndex][columnIndex] = 1
        case .Off:
          lights[rowIndex][columnIndex] = 0
        case .Toggle:
          lights[rowIndex][columnIndex] = (lights[rowIndex][columnIndex] + 1) % 2
        }
      }
    }
  }

  mutating func updateV2(_ instruction: LightInstruction) {
    let ll = instruction.lowerLeft
    let ur = instruction.upperRight
    let left = min(ll.x, ur.x)
    let right = max(ll.x, ur.x)
    let top = min(ll.y, ur.y)
    let bottom = max(ll.y, ur.y)
    for rowIndex in top...bottom {
      for columnIndex in left...right {
        switch instruction.state {
        case .On:
          lights[rowIndex][columnIndex] += 1
        case .Off:
          if lights[rowIndex][columnIndex] > 0 {
            lights[rowIndex][columnIndex] -= 1
          }
        case .Toggle:
          lights[rowIndex][columnIndex] += 2
        }
      }
    }
  }

  var countLights: Int {
    // values are 0 or 1, so we can add up all the values to get
    // the number that are on (1)
    return lights.reduce(0) { $0 + $1.reduce(0, +) }
  }
}

extension String {

  var asLightingInstruction: LightInstruction? {
    var command: LightState
    var prefixLength: Int
    if self.hasPrefix("turn on ") {
        command = .On
        prefixLength = 8
    }
    else if self.hasPrefix("turn off ") {
        command = .Off
        prefixLength = 9
    }
    else if self.hasPrefix("toggle ") {
        command = .Toggle
        prefixLength = 7
    }
    else {
      return nil
    }
    let coords = self[index(startIndex, offsetBy:prefixLength)..<endIndex]
    let ends = coords.split(separator: " through ")
    guard ends.count == 2 else { return nil }

    let c1 = ends[0].split(separator: ",").compactMap { Int($0) }
    let c2 = ends[1].split(separator: ",").compactMap { Int($0) }
    guard c1.count == 2 && c2.count == 2 else { return nil }
    let instruction = LightInstruction(state: command, lowerLeft: Coord2(x:c1[0], y:c1[1]), upperRight: Coord2(x:c2[0], y:c2[1]))
    return instruction
  }
  
}