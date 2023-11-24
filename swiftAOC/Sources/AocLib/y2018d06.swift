struct Problem201806: Problem {
  var name: String { "2018-06" }
  func solveWith(data: [String]) -> Solution { Solution201806(data: data) }
}

struct Solution201806: Solution {
  let data: [String]

  var part1: String {
    // coords.name = x*1000 + y
    //coords.bounds -> grid
    //grid(populate: coords)
    // grid -> infiniteCoords
    // grid.sizes -> sizes[coord: size?]
    //
    // let coords = data.compactMap { $0.asCoord }
    // let grid = coords.minimumGrid
    // let answer = grid.largestArea
    let answer = "Not Implemented"
    return "\(answer)"
  }

  var part2: String {
    let answer = "Not Implemented"
    return "\(answer)"
  }

}
