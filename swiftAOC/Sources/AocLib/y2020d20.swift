struct Problem202020: Problem {
  var name: String { "2020-20" }
  func solveWith(data: [String]) -> Solution { Solution202020(data: data) }
}

struct Solution202020: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    guard let puzzle = ImagePuzzle(data) else { return -1 }
    //print(puzzle)
    puzzle.sort()
    return puzzle.cornerProduct ?? -1
  }

  var answer2: Int {
    return -1
  }

}

class ImagePuzzle: CustomStringConvertible {
  let size: Int
  let pieces: [PieceId: Piece]
  var unplaced: Set<PieceId>
  var unplacedEdges = Set<PieceId>()
  var unplacedCorners = Set<PieceId>()
  var unplacedMiddles = Set<PieceId>()
    var board: [Coord2:(PieceId,Orientation)]
  let edges: [Int:Set<PieceId>]

  init?(_ data: [String]){
    var id: Int? = nil
    var lines = [String]()
    var pieces = [PieceId: Piece]()
    for line in data {
      if line.starts(with: "Tile ") {
        id = Int(line.filter{$0.isNumber})
      } else if line.isEmpty {
        if let realId = id, lines.count > 0 {
          if let piece = Piece(id: realId, image: lines) {
            pieces[piece.id] = piece
          }
        }
        lines.removeAll()
        id = nil
      } else {
        lines.append(line)
      }
    }
    // We might not have a blank line at the end, so create a piece with any unprocessed lines
    if let realId = id, lines.count > 0 {
      if let piece = Piece(id: realId, image: lines) {
        pieces[piece.id] = piece
      }
    }
    // Set size
    let size = Int(Double(pieces.count).squareRoot())
    // Sanity check, there are a square number of pieces
    if pieces.count != size * size { return nil }
    // Sanity check, verify all pieces are the same size
    guard pieces.count > 0, let pieceSize = pieces.values.first?.size else { return nil }
    if pieces.values.filter({ $0.size == pieceSize }).count != pieces.count { return nil }
    self.pieces = pieces
    self.size = size
    self.unplaced = Set(pieces.keys)
    self.board = [Coord2:(PieceId,Orientation)]()

    // Optimization:
    var edges = [Int:Set<PieceId>]()
    for (pieceId, piece) in pieces {
      for edge in piece.edges {
        if edges[edge] == nil { edges[edge] = Set<PieceId>() }
        edges[edge]!.insert(pieceId)
      }
    }
    self.edges = edges
    //print(edges.count)
    //print(edges)
    // for (edge, group) in edges {
    //   print("\(edge) x \(group.count)")
    // }
  }

  func sort() {
    // sorts unplaced into unplacedEdges, unplacedCorners, unplacedMiddle
    var edges = [Int:Set<PieceId>]()
    for (pieceId, piece) in pieces {
      for edgePair in piece.edgePairs {
        let edge = edgePair.x
        let egde = edgePair.y
        if edges[edge] == nil && edges[egde] == nil { edges[edge] = Set<PieceId>() }
        if edges[egde] != nil { edges[egde]!.insert(pieceId) }
        else {edges[edge]!.insert(pieceId)}
      }
    }
    let singleUseEdges = edges.filter { $1.count == 1 }
    var unusedEdges = [Int:Int]()
    for v in singleUseEdges.values {
      let id = v.first!
      let c = unusedEdges[id]
      if c == nil { unusedEdges[id] = 1 }
      else { unusedEdges[id] = c! + 1 }
    }
    for id in unplaced {
      if unusedEdges[id] == nil {
        unplacedMiddles.insert(id)
      } else if unusedEdges[id] == 1 {
        unplacedEdges.insert(id)
      } else if unusedEdges[id] == 2 {
        unplacedCorners.insert(id)
      } else {
        print("piece \(id) is confused")
      }
    }
    //print("Corners: \(unplacedCorners)")
    //print("Edges: \(unplacedEdges)")
    //print("Middles: \(unplacedMiddles)")
  }

  func solve() -> Bool {
    if unplaced.count == 0 { return true }
    guard let position = firstFree else { return true }
    let searchTiles:Set<PieceId> = {
      if position.x == 0 && position.y == 0 {
        return unplaced // at top left, try all pieces
      } else if position.x == 0 {
        guard let topEdge = top(position) else { return Set<PieceId>() }
        // print("top:\(topEdge)")
        return (edges[topEdge] ?? Set<PieceId>()).intersection(unplaced)
      } else if position.y == 0 {
        guard let leftEdge = left(position) else { return Set<PieceId>() }
        // print("left:\(leftEdge)")
        return (edges[leftEdge] ?? Set<PieceId>()).intersection(unplaced)
      }
      guard let topEdge = top(position), let leftEdge = left(position) else { return Set<PieceId>() }
      guard let e1 = edges[topEdge], let e2 = edges[leftEdge] else { return Set<PieceId>() }
      // print("top:\(topEdge) & left:\(leftEdge)")
      return e1.intersection(e2).intersection(unplaced)
    }()
    //print("\(board[position]) at:\(position): searching \(searchTiles)")
    for tileId in searchTiles {
      for orient in Orientation.allCases {
        if fits(piece: (tileId,orient), at:position) {
          board[position] = (tileId,orient)
          unplaced.remove(tileId)
          if solve() {
            return true
          } else {
            unplaced.insert(tileId)
            board[position] = nil
          }
        }
      }
    }
    return false
  }

  func top(_ position:Coord2) -> Int? {
    guard let above = abovePiece(at: position) else { return nil }
    guard let other = pieces[above.0] else { return nil }
    let orientation = above.1
    return other.bottom(with: orientation)
  }

  func left(_ position:Coord2) -> Int? {
    guard let left = leftPiece(at: position) else { return nil }
    guard let other = pieces[left.0] else { return nil }
    let orientation = left.1
    return other.right(with: orientation)
  }

  var firstFree: Coord2? {
    for y in 0..<size {
      for x in 0..<size {
        let c = Coord2(x:x, y:y)
        if board[c] == nil { return c }
      }
    }
    return nil
  }

  func fits(piece: (PieceId,Orientation), at position: Coord2) -> Bool {
    guard let myPiece = pieces[piece.0] else { return false }
    let myOrientation = piece.1
    if let left = left(position) {  // else this is a left edge
      if left != myPiece.left(with:myOrientation) {
        return false
      }
    }
    if let above = top(position) { // else this is a top edge
      if above != myPiece.top(with:myOrientation) {
        return false
      }
    }
    // because I'm proceeding left to right, top to bottom, there will never be a piece to the right or below
    return true
  }

  func leftPiece(at position: Coord2) -> (PieceId, Orientation)? {
    guard position.x > 0 else { return nil }
    return board[Coord2(x:position.x-1, y: position.y)]
  }

  func abovePiece(at position: Coord2) -> (PieceId, Orientation)? {
    guard position.y > 0 else { return nil }
    return board[Coord2(x:position.x, y: position.y-1)]
  }

  var cornerProduct: Int? {
    guard unplacedCorners.count == 4 else { return nil }
    return unplacedCorners.reduce(1, *)
  }

  var description: String {
    var lines = ["\(size)x\(size) Puzzle"]
    if board.count > 0 {
      lines.append("Board:")
      for y in 0..<size {
        for x in 0..<size {
          if let (piece,orientation) = board[Coord2(x:x, y:y)] {
            lines.append("Tile \(piece) at (\(x),\(y)) and \(orientation)")
          }
        }
      }
    }
    if pieces.count > 0 {
      lines.append("Tiles:")
      for (id, piece) in pieces {
        lines.append("Tile \(id) = \(piece)")
      }
    }
    return lines.joined(separator: "\n")
  }

}

typealias PieceId = Int
struct Piece: CustomStringConvertible {
  let id: PieceId
  let size: Int // determined by input to accept similar puzzles
  let image: [String]
  // The sides are a size (10) bit number
  // i.e.:     .#.#..##..
  //        => 0101001100 = 332
  // reverse = 0011001010 = 202

  let top: Int     // right to left
  let bottom: Int  // right to left
  let left: Int    // top to bottom
  let right: Int   // top to bottom

  let pot: Int     // top left to right
  let mottob: Int  // bottom left to right
  let tfel: Int    // left bottom to top
  let thgir: Int   // right bottom to top

  init?(id: Int, image: [String]) {
    self.id = id
    self.image = image
    guard image.count > 0, image.count == image[0].count else { return nil }
    self.size = image.count
    guard let t = Int(String(image[0].map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    guard let b = Int(String(image[size-1].map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    var leftChars = [Character]()
    var rightChars = [Character]()
    for line in image {
      guard line.count == size, let first = line.first, let last = line.last else { return nil }
      leftChars.append(first)
      rightChars.append(last)
    }
    guard let l = Int(String(leftChars.map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    guard let r = Int(String(rightChars.map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    top = t
    bottom = b
    left = l
    right = r
    pot = Piece.reverse(t, size: size)
    mottob = Piece.reverse(b, size: size)
    tfel = Piece.reverse(l, size: size)
    thgir = Piece.reverse(r, size: size)
  }

  var edges: [Int] {
    [top, pot, bottom, mottob, left, tfel, right, thgir]
  }
  var edgePairs: [Coord2] {
    [Coord2(x:top, y:pot), Coord2(x:bottom, y:mottob), Coord2(x:left, y:tfel), Coord2(x:right, y:thgir)]
  }

// Rotation is clockwise;
// fh = flip about horizontal axix (top -> bottom);
// fv = flip about vertical (left <-> right)
  func top(with orientation: Orientation) -> Int {
    switch orientation {
    case .rot0: return top
    case .rot90: return tfel
    case .rot180: return mottob
    case .rot270: return right
    case .fhRot0: return bottom
    case .fhRot90: return left
    case .fhRot180: return pot
    case .fhRot270: return thgir
    case .fvRot0: return pot
    case .fvRot90: return thgir
    case .fvRot180: return bottom
    case .fvRot270: return left
    }
  }

  func bottom(with orientation: Orientation) -> Int {
    switch orientation {
    case .rot0: return bottom
    case .rot90: return thgir
    case .rot180: return pot
    case .rot270: return left
    case .fhRot0: return top
    case .fhRot90: return right
    case .fhRot180: return mottob
    case .fhRot270: return tfel
    case .fvRot0: return mottob
    case .fvRot90: return tfel
    case .fvRot180: return top
    case .fvRot270: return right
    }
  }

  func left(with orientation: Orientation) -> Int {
    switch orientation {
    case .rot0: return left
    case .rot90: return bottom
    case .rot180: return thgir
    case .rot270: return pot
    case .fhRot0: return tfel
    case .fhRot90: return top
    case .fhRot180: return right
    case .fhRot270: return mottob
    case .fvRot0: return right
    case .fvRot90: return mottob
    case .fvRot180: return tfel
    case .fvRot270: return top
    }
  }

  func right(with orientation: Orientation) -> Int {
    switch orientation {
    case .rot0: return right
    case .rot90: return top
    case .rot180: return tfel
    case .rot270: return mottob
    case .fhRot0: return thgir
    case .fhRot90: return bottom
    case .fhRot180: return left
    case .fhRot270: return pot
    case .fvRot0: return left
    case .fvRot90: return pot
    case .fvRot180: return thgir
    case .fvRot270: return bottom
    }
  }

  static func reverse(_ x: Int, size: Int) -> Int {
    //size: 5, value: 2:  00010 -> "10" -> (reverse) -> "01" -> "01" + "000"
    let bin = String(x, radix: 2)
    let zeros = String(Array<Character>(repeating: "0", count: size - bin.count))
    return Int((bin.reversed() + zeros), radix: 2)!
  }

  var description: String {
    return "Id: \(id), Size: \(size), Top: \(top)(\(pot)), Bottom: \(bottom)(\(mottob))" +
    ", Left: \(left)(\(tfel)), Right: \(right)(\(thgir))"
  }
 }

// Rotation is clockwise
enum Orientation: CaseIterable {
  case rot0
  case rot90
  case rot180
  case rot270
  case fhRot0
  case fhRot90
  case fhRot180
  case fhRot270
  case fvRot0
  case fvRot90
  case fvRot180
  case fvRot270
}
struct Coord2: Hashable {
    let x: Int
    let y: Int
}
