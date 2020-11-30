struct Problem201503: Problem {
    var name: String { "2015-03" }
    func solveWith(data: [String]) -> Solution { Solution201503(data: data) }
}

struct Solution201503: Solution {
    let data: [String]

    var part1: String {
        return "\(houseCount)"
    }

    var part2: String {
        return "\(houseCountWithRoboSanta)"
    }

    var houseCount: Int {
        var visitedHouses = Set<Location>()
        var currentLocation = Location(x:0, y:0)
        visitedHouses.insert(currentLocation)
        for char in data[0] {
            let direction = MoveDirection(rawValue: char)
            currentLocation = currentLocation.moveTo(direction: direction)
            visitedHouses.insert(currentLocation)
        }
        return visitedHouses.count
    }
    var houseCountWithRoboSanta: Int {
        var visitedHouses = Set<Location>()
        var santaLocation = Location(x:0, y:0)
        var roboLocation = Location(x:0, y:0)
        visitedHouses.insert(santaLocation)
        visitedHouses.insert(roboLocation)
        var moveRobo = false
        for char in data[0] {
            let direction = MoveDirection(rawValue: char)
            if moveRobo {
                roboLocation = roboLocation.moveTo(direction: direction)
                visitedHouses.insert(roboLocation)
            } else {
                santaLocation = santaLocation.moveTo(direction: direction)
                visitedHouses.insert(santaLocation)
            }
            moveRobo.toggle()
        }
        return visitedHouses.count
    }
    struct Location: Hashable {
        let x: Int
        let y: Int

        func moveTo(direction: MoveDirection?) -> Location {
            switch direction {
            case .north: return Location(x: self.x + 1, y: self.y)
            case .east: return Location(x: self.x, y: self.y + 1)
            case .south: return Location(x: self.x - 1, y: self.y)
            case .west: return Location(x: self.x, y: self.y - 1)
            default: return self
            }
        }
    }
}

enum MoveDirection: Character {
    case north = "^"
    case east = ">"
    case south = "v"
    case west = "<"
}
