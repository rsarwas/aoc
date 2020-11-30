struct Problem201502: Problem {
    var name: String { "2015-02" }
    func solveWith(data: [String]) -> Solution { Solution201502(data: data) }
}

struct Solution201502: Solution {
    let data: [String]

    var part1: String {
        let presents = data.compactMap { $0.asPresent }
        let totalPaper = presents.reduce(0) {$0 + $1.paperRequired }
        return "\(totalPaper)"
    }

    var part2: String {
        let presents = data.compactMap { $0.asPresent }
        let totalRibbon = presents.reduce(0) { $0 + $1.ribbonRequired }
        return "\(totalRibbon)"
    }
}

struct Present {

    let cuboid: Cuboid

    var paperRequired: Int { cuboid.surfaceArea + cuboid.smallestSideArea }

    var ribbonRequired: Int { cuboid.volume + cuboid.smallestSidePerimeter }
}

struct Cuboid {
    let height: Int
    let length: Int
    let width: Int

    var areaA: Int { height * width }

    var areaB: Int { height * length }

    var areaC: Int { length * width }

    var perimeterA: Int { 2*height + 2*width }

    var perimeterB: Int { 2*height + 2*length }

    var perimeterC: Int { 2*length + 2*width }

    var volume: Int { height * width * length }

    var surfaceArea: Int { 2*areaA + 2*areaB + 2*areaC }

    var smallestSideArea: Int { min(areaA, areaB, areaC) }

    var smallestSidePerimeter: Int { min(perimeterA, perimeterB, perimeterC) }
}

extension String {
    /// returns a Optional Present from a string in the form of HxLxW
    /// where H, L, W are integers.
    /// If string is malformed, nil is returned
    /// If either of H, L, or W cannot be converted to an integer,
    /// that dimension will be set to 0
    var asPresent: Present? {
        guard self.contains("x") else { return nil }
        let dims = self.split(separator:"x").map{Int($0) ?? 0}
        guard dims.count == 3 else { return nil }
        let cuboid = Cuboid(height: dims[0], length: dims[1], width: dims[2])
        return Present(cuboid: cuboid)
    }
}
