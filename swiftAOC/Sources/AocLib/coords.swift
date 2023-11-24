struct Coord2: Hashable {
  let x: Int
  let y: Int
}

struct Coord3: Hashable {
  let x: Int
  let y: Int
  let z: Int
}

struct Coord4: Hashable {
  let x: Int
  let y: Int
  let z: Int
  let t: Int
}

struct HexCoord: Hashable {
  let x: Int
  let y: Int

  /*
   X Coordinates are staggered for Hexagons; Increase to the East:
2  0 1 2 3 4
1   0 1 2 3 4
0    0 1 2 3 4
Y Coordinates Increase to the North
*/
  static let moves = [
    "se": (0, -1),
    "sw": (-1, -1),
    "e": (1, 0),
    "w": (-1, 0),
    "ne": (1, 1),
    "nw": (0, 1),
  ]

}

extension HexCoord {

  func move(dir: String) -> HexCoord? {
    guard let (dx, dy) = HexCoord.moves[dir] else { return nil }
    return HexCoord(x: self.x + dx, y: self.y + dy)
  }

  var neighbors: Set<HexCoord> {
    return Set([
      self.move(dir: "se")!,
      self.move(dir: "sw")!,
      self.move(dir: "e")!,
      self.move(dir: "w")!,
      self.move(dir: "ne")!,
      self.move(dir: "nw")!,
    ])
  }
}

extension String {
  var asHexCoord: HexCoord? {
    var coord = HexCoord(x: 0, y: 0)
    var prefix: Character? = nil
    for char in self {
      switch (prefix, char) {
      case (nil, "e"):
        coord = coord.move(dir: "e")!
        break
      case (nil, "w"):
        coord = coord.move(dir: "w")!
        break
      case (nil, "s"):
        prefix = "s"
        break
      case (nil, "n"):
        prefix = "n"
        break
      case ("s", "e"):
        prefix = nil
        coord = coord.move(dir: "se")!
        break
      case ("s", "w"):
        prefix = nil
        coord = coord.move(dir: "sw")!
        break
      case ("n", "e"):
        prefix = nil
        coord = coord.move(dir: "ne")!
        break
      case ("n", "w"):
        prefix = nil
        coord = coord.move(dir: "nw")!
        break
      default: return nil
      }
    }
    return coord
  }
}
