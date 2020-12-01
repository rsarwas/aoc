import XCTest

@testable import AocLib

final class swiftAOCTests: XCTestCase {

  func test201501a() {
    let testCases = [
      ("(())", "0"), ("()()", "0"),
      ("(((", "3"), ("(()(()(", "3"), ("))(((((", "3"),
      ("())", "-1"), ("))(", "-1"),
      (")))", "-3"), (")())())", "-3"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201501(data: [input])
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test201501b() {
    let testCases = [
      (")", "1"),
      ("()())", "5"),
      ("(((", "Never"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201501(data: [input])
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test201502a() {
    let testCases = [
      ("2x3x4", "58"),
      ("1x1x10", "43"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201502(data: [input])
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test201502b() {
    let testCases = [
      ("2x3x4", "34"),
      ("1x1x10", "14"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201502(data: [input])
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test201503a() {
    let testCases = [
      (">", "2"),
      ("^>v<", "4"),
      ("^v^v^v^v^v", "2"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201503(data: [input])
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test201503b() {
    let testCases = [
      ("^v", "3"),
      ("^>v<", "3"),
      ("^v^v^v^v^v", "11"),
    ]
    for (input, answer) in testCases {
      let solution = Solution201503(data: [input])
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202001a() {
    let testCases = [
      (["1721","979","366","299","675","1456"], "514579"),
    ]
    for (input, answer) in testCases {
      let solution = Solution202001(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202001b() {
    let testCases = [
      (["1721","979","366","299","675","1456"], "241861950"),
    ]
    for (input, answer) in testCases {
      let solution = Solution202001(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  static var allTests = [
    // ("test201501a", test201501a),
    // ("test201501b", test201501b),
    // ("test201502a", test201502a),
    // ("test201502b", test201502b),
    ("test201503a", test201503a),
    ("test201503b", test201503b),
  ]
}
