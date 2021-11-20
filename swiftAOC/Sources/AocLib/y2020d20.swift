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
    guard puzzle.solve() else { return -2 }
    return puzzle.cornerProduct ?? -1
  }

  var answer2: Int {
    guard let puzzle = ImagePuzzle(data) else { return -1 }
    puzzle.sort()
    //testRotatingFlipping(puzzle)
    guard puzzle.solve() else { return -2 }
    guard let image = puzzle.asImage else { return -3 }
    //print(image.asString)
    //print(SeaMonster().image.asString)
    return roughness(image)
  }

  func testRotatingFlipping(_ puzzle: ImagePuzzle) {
    // print out a single piece at all orientations
    // visually check that it is correctly transformed
    let p1 = puzzle.pieces[puzzle.unplacedMiddles.first!]!
    for o in Orientation.allCases {
      let image = p1.asImage(with: o)
      print(o)
      print(image.asString)
    }
  }

  func roughness(_ image: Image) -> Int {
    // The count of all the waves in the image.
    // A wave is a cell that is true ('#' in the source) after the monsters (cells
    // which are true because they are part of a monster not a wave) are removed.
    // Image may need to be rotated/flipped to see the monsters.
    // Assume only the correct orientation will yield a non zero monster count
    let monster = SeaMonster()
    let monsterImage = monster.asImage
    for o in Orientation.allCases {
      // it would be faster to transform the smaller monster image, but my inplace transformation requires a square image
      var transformedImage = image
      transformedImage.reorientate(to:o)
      let monsters = countSeaMonsters(image: transformedImage, monster: monsterImage)
      //print("Orientation: \(o) has \(monsters) monsters")
      if monsters > 0 {
        return image.onCount - (monsters * monster.asImage.onCount)
      }
    }
    return image.onCount
  }

  func countSeaMonsters(image: Image, monster: Image) -> Int {
    var count = 0
    for row in 0..<(image.height - monster.height) {
      for col in 0..<(image.width - monster.width) {
        if isSubImage(main: image, small: monster, row: row, col: col) {
          count += 1
        }
      }
    }
    return count
  }

  func isSubImage(main: Image, small: Image, row: Int, col: Int) -> Bool {
    for srow in 0..<small.height {
      for scol in 0..<small.width {
        if small[srow][scol] && !main[row + srow][col + scol] { return false }
      }
    }
    return true
  }

}

class ImagePuzzle: CustomStringConvertible {
  let size: Int
  let pieces: [PieceId: Piece]
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
          if let piece = Piece(id: realId, data: lines) {
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
      if let piece = Piece(id: realId, data: lines) {
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
    //self.unplaced = Set(pieces.keys)
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
    // for edge in edges.keys.sorted() {
    //   print("\(edge): \(edges[edge]!)")
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
    for id in Set(pieces.keys) {
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
    // print("Corners: \(unplacedCorners)")
    // print("Edges: \(unplacedEdges)")
    // print("Middles: \(unplacedMiddles)")
  }

  func solve() -> Bool {
    // We search left to right inside top to bottom
    // the top left piece is first, the bottom right piece is last
    if unplacedCorners.count == 0 { return true }
    guard let position = firstFree else { return true }
    let searchTiles:Set<PieceId> = {
      var candidates: Set<PieceId>? = nil
      // limit the search to tiles that match the upper and or left neighbor
      if position.x == 0 && position.y == 0 {
        // no neighbors, we could search all tiles, but we only need to search the corners
        return unplacedCorners
      }
      if position.x == 0 {
        // left edge has no left neighbor but must have an upper neighbor (it's not 0,0)
        guard let topEdge = top(position) else { print("error no upper"); return Set<PieceId>() }
        //print("top:\(topEdge)")
        candidates = edges[topEdge]
      } else if position.y == 0 {
        // upper edge has no upper neighbor but must have an left neighbor (it's not 0,0)
        guard let leftEdge = left(position) else { print("error no left"); return Set<PieceId>() }
        //print("left:\(leftEdge)")
        candidates = edges[leftEdge]
      } else {
        // must have upper neighbor and left neighbor (it's not at y=0 or x=0)
        guard let topEdge = top(position), let leftEdge = left(position) else { print("error no left"); return Set<PieceId>() }
        guard let e1 = edges[topEdge], let e2 = edges[leftEdge] else { print("error no upper"); return Set<PieceId>() }
        //print("top:\(topEdge) & left:\(leftEdge)")
        candidates = e1.intersection(e2)
      }
      switch pieceType(position) {
      case .corner: return (candidates ?? Set<PieceId>()).intersection(unplacedCorners)
      case .edge: return (candidates ?? Set<PieceId>()).intersection(unplacedEdges)
      case .middle: return (candidates ?? Set<PieceId>()).intersection(unplacedMiddles)
      }
    }()
    //print("At:\(position): searching \(searchTiles)")
    for tileId in searchTiles {
      for orient in Orientation.allCases {
        if fits(piece: (tileId,orient), at:position) {
          board[position] = (tileId,orient)
          //print("placing \((tileId,orient)) at \(position)")
          switch pieceType(position) {
          case .corner: unplacedCorners.remove(tileId); break
          case .edge: unplacedEdges.remove(tileId); break
          case .middle: unplacedMiddles.remove(tileId); break
          }
          if solve() {
            return true
          } else {
            //print("removing \(tileId) from \(position)")
            switch pieceType(position) {
            case .corner: unplacedCorners.insert(tileId); break
            case .edge: unplacedEdges.insert(tileId); break
            case .middle: unplacedMiddles.insert(tileId); break
            }
            board[position] = nil
          }
        }
      }
    }
    //print("solve failed")
    return false
  }

  func pieceType(_ position:Coord2) -> PieceType {
      if position.x == 0 && position.y == 0 ||
         position.x == 0 && position.y == size - 1 ||
         position.x == size - 1 && position.y == 0 ||
         position.x == size - 1 && position.y == size - 1 {
        return .corner
      }
      if position.y == 0 || position.y == size - 1 || position.x == 0 || position.x == size - 1 {
        return .edge
      }
      return .middle
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
    if unplacedCorners.count == 4 {
      return unplacedCorners.reduce(1, *)
    }
    guard let corners = solvedCorners, corners.count == 4 else { return nil }
    return corners.reduce(1, *)
  }

  var solvedCorners: Set<PieceId>? {
    guard let c1 = board[Coord2(x:0,      y:0)   ]?.0 else { return nil }
    guard let c2 = board[Coord2(x:0,      y:size-1)]?.0 else { return nil }
    guard let c3 = board[Coord2(x:size-1, y:0)   ]?.0 else { return nil }
    guard let c4 = board[Coord2(x:size-1, y:size-1)]?.0 else { return nil }
    return Set([c1, c2, c3, c4])
  }

  var asImage: Image? {
    let puzzleSize = size
    let tileSize = pieces.values.first!.size - 2 // remove the edges
    let imageSize = puzzleSize * tileSize
    var image = Array(repeating: Array(repeating: false, count: imageSize), count: imageSize)
    for i in 0..<puzzleSize {
      for j in 0..<puzzleSize {
        let (pieceId, orientation) = board[Coord2(x:j, y:i)]!
        let tile = pieces[pieceId]!.asImage(with: orientation)
        for u in 0..<tileSize {
          for v in 0..<tileSize {
            image[i*tileSize + u][j*tileSize + v] = tile[u][v]
          }
        }
      }
    }
    return image
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

enum PieceType {
  case corner
  case edge
  case middle
}

typealias PieceId = Int

struct Piece: CustomStringConvertible {
  let id: PieceId
  let size: Int // determined by input to accept similar puzzles
  let imageData: [String]
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

  init?(id: Int, data: [String]) {
    self.id = id
    self.imageData = data
    guard data.count > 0, data.count == data[0].count else { return nil }
    self.size = data.count
    guard let t = Int(String(data[0].map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    guard let b = Int(String(data[size-1].map { $0 == "#" ? "1" : "0" }), radix: 2) else { return nil }
    var leftChars = [Character]()
    var rightChars = [Character]()
    for line in data {
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
    }
  }

  static func reverse(_ x: Int, size: Int) -> Int {
    //size: 5, value: 2:  00010 -> "10" -> (reverse) -> "01" -> "01" + "000"
    let bin = String(x, radix: 2)
    let zeros = String(Array<Character>(repeating: "0", count: size - bin.count))
    return Int((bin.reversed() + zeros), radix: 2)!
  }

  var asImage: Image {
    self.imageData.dropFirst().dropLast().map { row in
      row.dropFirst().dropLast().map { $0 == "#" }
    }
  }

  func asImage(with orientation: Orientation) -> Image {
    var image = self.asImage
    image.reorientate(to: orientation)
    return image
  }

  var description: String {
    return "Id: \(id), Size: \(size), Top: \(top)(\(pot)), Bottom: \(bottom)(\(mottob))" +
    ", Left: \(left)(\(tfel)), Right: \(right)(\(thgir))"
  }
 }

typealias Image = [[Bool]]
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
  // note: fv + rot 180 is the same as fh rot 0, so we can ignore it
}
struct Coord2: Hashable {
    let x: Int
    let y: Int
}

extension Array where Element == Array<Bool> {

  mutating func transpose() {
    // fatal error if matrix is not square
    for i in 0..<self.count {
      for j in (i+1)..<self[i].count {
        let temp = self[i][j]
        self[i][j] = self[j][i]
        self[j][i] = temp
      }
    }
  }

  mutating func flipH() {
    // flip over the horizontal (X) axis
    self.reverse()
  }

  mutating func flipV() {
    // flip over the vertical (Y) axis
    //self.forEach{ $0.reverse() } // $0 is immutable
    //self = self.map { $0.reversed() } // ok but make new array
    for i in 0..<self.count { self[i].reverse() }
  }

  mutating func reorientate(to orientation: Orientation) {
    switch orientation {
    case .rot0: break //identity
    case .rot90: self.transpose(); self.flipV(); break
    case .rot180: self.flipV(); self.flipH(); break
    case .rot270: self.transpose(); self.flipH(); break
    case .fhRot0: self.flipH(); break
    case .fhRot90: self.transpose(); break
    case .fhRot180: self.flipV(); break
    case .fhRot270: self.transpose(); self.flipV(); self.flipH(); break
    }
  }

  var onCount: Int {
    //Returns the number of cells in image that are on (true)
    self.map { row in row.map { $0 ? 1 : 0 }.reduce(0, +) }.reduce(0, +)
  }

  var height: Int {
    self.count
  }
  
  var width: Int {
    guard self.count > 0 else { return 0 }
    return self[0].count
  }

}

extension Array where Element == Array<Bool> {
  // Array already conforms to CustomStringConvertible, so this is a lame work around
  var asString: String {
    let stringRows = self.map { row in
      String(row.map { $0 ? "#" : "." })
    }
    return stringRows.joined(separator: "\n")
  }
}

struct SeaMonster {
  let definition = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
  ]
  let width: Int
  let height: Int
  init() {
    height = definition.count
    width = definition[0].count
  }

  var asImage: Image {
    return definition.map { row in
      row.map { $0 == "#" }
    }
  }

  func asImage(with orientation: Orientation) -> Image {
    var image = self.asImage
    image.reorientate(to: orientation)
    return image
  }

}
