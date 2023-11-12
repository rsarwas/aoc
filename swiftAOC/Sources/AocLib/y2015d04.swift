import CryptoKit // Requires MacOS 15+

struct Problem201504: Problem {
  var name: String { "2015-04" }
  func solveWith(data: [String]) -> Solution { Solution201504(data: data) }
}

struct Solution201504: Solution {
  let data: [String]

  var part1: String {
    var index = 0
    let key = data[0]
    while (true) {
        let index_str = "\(index)"
        let test = key + index_str
        // Insecure in CryptoKit
        let hash = Insecure.MD5.hash(data: test.data(using: .utf8)!)
        //print("\(index) -> \(test) -> \(hash)")
        if hash.description.prefix(17) == "MD5 digest: 00000" {
            return index_str
        }
        index = index + 1
        // if index % 5000 == 0 {
        //   print(".", terminator: "")
        // }
        // if (index > 254575) {
        //   print("\(index-1) -> \(test) -> \(hash)")
        //   fatalError("I went past the solution")
        // }
    }
  }

  var part2: String {
    var index = 254575 // start at solution to part 1
    let key = data[0]
    while (true) {
        let index_str = "\(index)"
        let test = key + index_str
        // Insecure in CryptoKit
        let hash = Insecure.MD5.hash(data: test.data(using: .utf8)!)
        if hash.description.prefix(18) == "MD5 digest: 000000" {
            return index_str
        }
        index = index + 1
    }
  }

}
