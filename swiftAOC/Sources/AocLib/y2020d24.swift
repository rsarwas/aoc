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
