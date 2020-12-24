struct Problem202024: Problem {
  var name: String { "2020-24" }
  func solveWith(data: [String]) -> Solution { Solution202024(data: data) }
}

struct Solution202024: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    return blackTiles.count
  }

  var answer2: Int {
    let conway = HexConway(alive: blackTiles)
    conway.flip(100)
    return conway.score
  }

  var blackTiles: Set<HexCoord> {
    // A tile is identified by it's HexCoordinates
    let tiles = data.compactMap { $0.asHexCoord }
    var blackTiles = Set<HexCoord>()
    for tile in tiles {
      if blackTiles.contains(tile) {
        blackTiles.remove(tile)
      } else {
        blackTiles.insert(tile)
      }
    }
    return blackTiles
  }

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
    "se": (0,-1),
    "sw": (-1,-1),
    "e": (1,0),
    "w": (-1,0),
    "ne": (1,1),
    "nw": (0,1)
  ]

}

extension  HexCoord {

  func move(dir: String) -> HexCoord? {
    guard let (dx,dy) = HexCoord.moves[dir] else { return nil }
    return HexCoord(x: self.x + dx, y: self.y + dy)
  }

  var neighbors: Set<HexCoord> {
    return Set([
      self.move(dir:"se")!,
      self.move(dir:"sw")!,
      self.move(dir:"e")!,
      self.move(dir:"w")!,
      self.move(dir:"ne")!,
      self.move(dir:"nw")!
    ])
  }
}
extension String {
  var asHexCoord : HexCoord? {
    var coord = HexCoord(x:0,y:0)
    var prefix : Character? = nil
    for char in self {
      switch (prefix, char) {
      case (nil, "e"): coord = coord.move(dir: "e")!; break
      case (nil, "w"): coord = coord.move(dir: "w")!; break
      case (nil, "s"): prefix = "s"; break
      case (nil, "n"): prefix = "n"; break
      case ("s", "e"): prefix = nil; coord = coord.move(dir: "se")!; break
      case ("s", "w"): prefix = nil; coord = coord.move(dir: "sw")!; break
      case ("n", "e"): prefix = nil; coord = coord.move(dir: "ne")!; break
      case ("n", "w"): prefix = nil; coord = coord.move(dir: "nw")!; break
      default: return nil
      }
    }
    return coord
  }
}

class HexConway {
  private var alive: Set<HexCoord>

  init (alive: Set<HexCoord>) {
    self.alive = alive
  }

/* Rules:
    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
*/

  func flip(_ n: Int) {
    for _ in 0..<n {
      flip()
    }
  }

  func flip() {
    var newAlive = Set<HexCoord>()
    for black in alive {
      let neighbors = black.neighbors
      let blackNeighborCount = neighbors.map { alive.contains($0) ? 1 : 0 }.reduce(0,+)
      if blackNeighborCount == 1 || blackNeighborCount == 2 {
        newAlive.insert(black)
      }
      // I only need to consider white tiles adjacent to a black tile (not all, infinite, white tiles)
      let whiteNeighbors = neighbors.filter { !alive.contains($0) }
      for white in whiteNeighbors {
        let blackNeighborCount = white.neighbors.map { alive.contains($0) ? 1 : 0 }.reduce(0,+)
        if blackNeighborCount == 2 {
          newAlive.insert(white)
        }
      }
    }
    alive = newAlive
    //print(alive.count)
  }

  var score: Int { alive.count }

}
