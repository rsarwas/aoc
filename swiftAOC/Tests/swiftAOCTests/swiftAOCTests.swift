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
      (["1721", "979", "366", "299", "675", "1456"], "514579")
    ]
    for (input, answer) in testCases {
      let solution = Solution202001(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202001b() {
    let testCases = [
      (["1721", "979", "366", "299", "675", "1456"], "241861950")
    ]
    for (input, answer) in testCases {
      let solution = Solution202001(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202002a() {
    let testCases = [
      (["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"], "2")
    ]
    for (input, answer) in testCases {
      let solution = Solution202002(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202002b() {
    let testCases = [
      (["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"], "1")
    ]
    for (input, answer) in testCases {
      let solution = Solution202002(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202003a() {
    let testCases = [
      (
        [
          "..##.......",
          "#...#...#..",
          ".#....#..#.",
          "..#.#...#.#",
          ".#...##..#.",
          "..#.##.....",
          ".#.#.#....#",
          ".#........#",
          "#.##...#...",
          "#...##....#",
          ".#..#...#.#",
        ], "7"
      )
    ]
    for (input, answer) in testCases {
      let solution = Solution202003(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202003b() {
    let testCases = [
      (
        [
          "..##.......",
          "#...#...#..",
          ".#....#..#.",
          "..#.#...#.#",
          ".#...##..#.",
          "..#.##.....",
          ".#.#.#....#",
          ".#........#",
          "#.##...#...",
          "#...##....#",
          ".#..#...#.#",
        ], "336"
      )
    ]
    for (input, answer) in testCases {
      let solution = Solution202003(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202004a() {
    let testCases = [
      (
        [
          "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
          "byr:1937 iyr:2017 cid:147 hgt:183cm",
          "",
          "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
          "hcl:#cfa07d byr:1929",
          "",
          "hcl:#ae17e1 iyr:2013",
          "eyr:2024",
          "ecl:brn pid:760753108 byr:1931",
          "hgt:179cm",
          "",
          "hcl:#cfa07d eyr:2025 pid:166559648",
          "iyr:2011 ecl:brn hgt:59in",
        ], "2"
      )
    ]
    for (input, answer) in testCases {
      let solution = Solution202004(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202004bInvalid() {
    let testCases = [
      (
        [
          "eyr:1972 cid:100",
          "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
          "",
          "iyr:2019",
          "hcl:#602927 eyr:1967 hgt:170cm",
          "ecl:grn pid:012533040 byr:1946",
          "",
          "hcl:dab227 iyr:2012",
          "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
          "",
          "hgt:59cm ecl:zzz",
          "eyr:2038 hcl:74454a iyr:2023",
          "pid:3556412378 byr:2007",
          "",
        ], "0"
      )
    ]
    for (input, answer) in testCases {
      let solution = Solution202004(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202004bValid() {
    let testCases = [
      (
        [
          "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
          "hcl:#623a2f",
          "",
          "eyr:2029 ecl:blu cid:129 byr:1989",
          "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
          "",
          "hcl:#888785",
          "hgt:164cm byr:2001 iyr:2015 cid:88",
          "pid:545766238 ecl:hzl",
          "eyr:2022",
          "",
          "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
          "",
        ], "4"
      )
    ]
    for (input, answer) in testCases {
      let solution = Solution202004(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202005a() {
    let testCases = [
      (["BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"], "820")
    ]
    for (input, answer) in testCases {
      let solution = Solution202005(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202006a() {
    let testCases = [
      (["abc", "", "a", "b", "c", "", "ab", "ac", "", "a", "a", "a", "a", "", "b", ""], "11")
    ]
    for (input, answer) in testCases {
      let solution = Solution202006(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202006b() {
    let testCases = [
      (["abc", "", "a", "b", "c", "", "ab", "ac", "", "a", "a", "a", "a", "", "b", ""], "6")
    ]
    for (input, answer) in testCases {
      let solution = Solution202006(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202007a() {
    let testCases = [
      (["light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags."
      ], "4")
    ]
    for (input, answer) in testCases {
      let solution = Solution202007(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202007b1() {
    let testCases = [
      (["light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags."
      ], "32")
    ]
    for (input, answer) in testCases {
      let solution = Solution202007(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202007b2() {
    let testCases = [
      (["shiny gold bags contain 2 dark red bags.",
        "dark red bags contain 2 dark orange bags.",
        "dark orange bags contain 2 dark yellow bags.",
        "dark yellow bags contain 2 dark green bags.",
        "dark green bags contain 2 dark blue bags.",
        "dark blue bags contain 2 dark violet bags.",
        "dark violet bags contain no other bags."
      ], "126")
    ]
    for (input, answer) in testCases {
      let solution = Solution202007(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

  func test202008a() {
    let testCases = [
      (["nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6"
      ], "5")
    ]
    for (input, answer) in testCases {
      let solution = Solution202008(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  func test202008b() {
    let testCases = [
      (["nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6"
      ], "8")
    ]
    for (input, answer) in testCases {
      let solution = Solution202008(data: input)
      XCTAssertEqual(solution.part2, answer)
    }
  }

}

