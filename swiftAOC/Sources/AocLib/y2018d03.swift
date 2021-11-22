struct Problem201803: Problem {
  var name: String { "2018-03" }
  func solveWith(data: [String]) -> Solution { Solution201803(data: data) }
}

struct Solution201803: Solution {
  let data: [String]

  var part1: String {
    let claims = data.compactMap { $0.asClaim }
    return "\(claims.overlaps.count)"
  }

  var part2: String {
    let claims = data.compactMap { $0.asClaim }
    guard let answer = claims.cleanClaim else { return "-1" }
    return "\(answer)"
  }

}

struct Claim {
  let id: Int
  let leftMargin: Int
  let topMargin: Int
  let width: Int
  let height: Int
}

extension String {
  var asClaim: Claim? {
    // after removing spaces, each line is #id@l,t:wxh
    // where id,l,t,w,h are 1 to 4 digit ints)
    // then just split on "@", ":", ",", and "x" to get the parts
    let line = self.replacingOccurrences(of: " ", with: "")
      .replacingOccurrences(of: "#", with: "")
    let idAndRest = line.split(separator: "@")
    guard idAndRest.count == 2 else { return nil }
    guard let id = Int(idAndRest[0]) else { return nil }
    let marginAndSize = idAndRest[1].split(separator: ":")
    guard marginAndSize.count == 2 else { return nil }
    let margin = marginAndSize[0].split(separator: ",")
    let size = marginAndSize[1].split(separator: "x")
    guard margin.count == 2 else { return nil }
    guard let l = Int(margin[0]), let t = Int(margin[1]) else { return nil }
    guard size.count == 2 else { return nil }
    guard let w = Int(size[0]), let h = Int(size[1]) else { return nil }
    let claim = Claim(id: id, leftMargin: l, topMargin: t, width: w, height: h)
    return claim
  }
}

extension Array where Element == Claim {

  var overlaps: Set<Coord2> {
    var swatches = Set<Coord2>()
    var overlaps = Set<Coord2>()
    for claim in self {
      for x in 0..<claim.width {
        for y in 0..<claim.height {
          let c = Coord2(x: x + claim.leftMargin, y: y + claim.topMargin)
          if swatches.contains(c) {
            overlaps.insert(c)
          } else {
            swatches.insert(c)
          }
        }
      }
    }
    return overlaps
  }

  var cleanClaim: Int? {
    let savedOverlaps = self.overlaps
    claimSearch: for claim in self {
      for x in 0..<claim.width {
        for y in 0..<claim.height {
          let c = Coord2(x: x + claim.leftMargin, y: y + claim.topMargin)
          if savedOverlaps.contains(c) { continue claimSearch }
        }
      }
      return claim.id
    }
    return nil
  }

}
