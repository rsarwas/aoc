struct Problem201501: Problem {
    var name: String { "2015-01" }
    func solveWith(data: [String]) -> Solution { Solution201501(data: data) }
}

struct Solution201501: Solution {
    let data: [String]

    var part1: String {
        return "\(finalFloor)"
    }

    var part2: String {
        return movesToBasement == nil ? "Never" : "\(movesToBasement!)"
    }

    var finalFloor: Int {
        var floor = 0
        for char in data[0] {
            if char == "(" { floor += 1}
            if char == ")" { floor -= 1}
       }
       return floor
    }

    var movesToBasement: Int? {
        var floor = 0
        var moves = 0
        for char in data[0] {
            if char == "(" { floor += 1; moves += 1}
            if char == ")" { floor -= 1; moves += 1}
            if floor < 0 { return moves }
        }
        return nil
    }

}