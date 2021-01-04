import XCTest

@testable import AocLib

final class swiftAOCTests: XCTestCase {

  // func test201501a() {
  //   let testCases = [
  //     ("(())", "0"), ("()()", "0"),
  //     ("(((", "3"), ("(()(()(", "3"), ("))(((((", "3"),
  //     ("())", "-1"), ("))(", "-1"),
  //     (")))", "-3"), (")())())", "-3"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201501(data: [input])
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test201501b() {
  //   let testCases = [
  //     (")", "1"),
  //     ("()())", "5"),
  //     ("(((", "Never"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201501(data: [input])
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test201502a() {
  //   let testCases = [
  //     ("2x3x4", "58"),
  //     ("1x1x10", "43"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201502(data: [input])
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test201502b() {
  //   let testCases = [
  //     ("2x3x4", "34"),
  //     ("1x1x10", "14"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201502(data: [input])
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test201503a() {
  //   let testCases = [
  //     (">", "2"),
  //     ("^>v<", "4"),
  //     ("^v^v^v^v^v", "2"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201503(data: [input])
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test201503b() {
  //   let testCases = [
  //     ("^v", "3"),
  //     ("^>v<", "3"),
  //     ("^v^v^v^v^v", "11"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution201503(data: [input])
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202001a() {
  //   let testCases = [
  //     (["1721", "979", "366", "299", "675", "1456"], "514579")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202001(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202001b() {
  //   let testCases = [
  //     (["1721", "979", "366", "299", "675", "1456"], "241861950")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202001(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202002a() {
  //   let testCases = [
  //     (["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"], "2")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202002(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202002b() {
  //   let testCases = [
  //     (["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"], "1")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202002(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202003a() {
  //   let testCases = [
  //     (
  //       [
  //         "..##.......",
  //         "#...#...#..",
  //         ".#....#..#.",
  //         "..#.#...#.#",
  //         ".#...##..#.",
  //         "..#.##.....",
  //         ".#.#.#....#",
  //         ".#........#",
  //         "#.##...#...",
  //         "#...##....#",
  //         ".#..#...#.#",
  //       ], "7"
  //     )
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202003(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202003b() {
  //   let testCases = [
  //     (
  //       [
  //         "..##.......",
  //         "#...#...#..",
  //         ".#....#..#.",
  //         "..#.#...#.#",
  //         ".#...##..#.",
  //         "..#.##.....",
  //         ".#.#.#....#",
  //         ".#........#",
  //         "#.##...#...",
  //         "#...##....#",
  //         ".#..#...#.#",
  //       ], "336"
  //     )
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202003(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202004a() {
  //   let testCases = [
  //     (
  //       [
  //         "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
  //         "byr:1937 iyr:2017 cid:147 hgt:183cm",
  //         "",
  //         "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
  //         "hcl:#cfa07d byr:1929",
  //         "",
  //         "hcl:#ae17e1 iyr:2013",
  //         "eyr:2024",
  //         "ecl:brn pid:760753108 byr:1931",
  //         "hgt:179cm",
  //         "",
  //         "hcl:#cfa07d eyr:2025 pid:166559648",
  //         "iyr:2011 ecl:brn hgt:59in",
  //       ], "2"
  //     )
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202004(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202004bInvalid() {
  //   let testCases = [
  //     (
  //       [
  //         "eyr:1972 cid:100",
  //         "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
  //         "",
  //         "iyr:2019",
  //         "hcl:#602927 eyr:1967 hgt:170cm",
  //         "ecl:grn pid:012533040 byr:1946",
  //         "",
  //         "hcl:dab227 iyr:2012",
  //         "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
  //         "",
  //         "hgt:59cm ecl:zzz",
  //         "eyr:2038 hcl:74454a iyr:2023",
  //         "pid:3556412378 byr:2007",
  //         "",
  //       ], "0"
  //     )
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202004(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202004bValid() {
  //   let testCases = [
  //     (
  //       [
  //         "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
  //         "hcl:#623a2f",
  //         "",
  //         "eyr:2029 ecl:blu cid:129 byr:1989",
  //         "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
  //         "",
  //         "hcl:#888785",
  //         "hgt:164cm byr:2001 iyr:2015 cid:88",
  //         "pid:545766238 ecl:hzl",
  //         "eyr:2022",
  //         "",
  //         "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
  //         "",
  //       ], "4"
  //     )
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202004(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202005a() {
  //   let testCases = [
  //     (["BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"], "820")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202005(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202006a() {
  //   let testCases = [
  //     (["abc", "", "a", "b", "c", "", "ab", "ac", "", "a", "a", "a", "a", "", "b", ""], "11")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202006(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202006b() {
  //   let testCases = [
  //     (["abc", "", "a", "b", "c", "", "ab", "ac", "", "a", "a", "a", "a", "", "b", ""], "6")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202006(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202007a() {
  //   let testCases = [
  //     (["light red bags contain 1 bright white bag, 2 muted yellow bags.",
  //       "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
  //       "bright white bags contain 1 shiny gold bag.",
  //       "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
  //       "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
  //       "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
  //       "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
  //       "faded blue bags contain no other bags.",
  //       "dotted black bags contain no other bags."
  //     ], "4")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202007(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202007b1() {
  //   let testCases = [
  //     (["light red bags contain 1 bright white bag, 2 muted yellow bags.",
  //       "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
  //       "bright white bags contain 1 shiny gold bag.",
  //       "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
  //       "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
  //       "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
  //       "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
  //       "faded blue bags contain no other bags.",
  //       "dotted black bags contain no other bags."
  //     ], "32")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202007(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202007b2() {
  //   let testCases = [
  //     (["shiny gold bags contain 2 dark red bags.",
  //       "dark red bags contain 2 dark orange bags.",
  //       "dark orange bags contain 2 dark yellow bags.",
  //       "dark yellow bags contain 2 dark green bags.",
  //       "dark green bags contain 2 dark blue bags.",
  //       "dark blue bags contain 2 dark violet bags.",
  //       "dark violet bags contain no other bags."
  //     ], "126")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202007(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202008a() {
  //   let testCases = [
  //     (["nop +0",
  //       "acc +1",
  //       "jmp +4",
  //       "acc +3",
  //       "jmp -3",
  //       "acc -99",
  //       "acc +1",
  //       "jmp -4",
  //       "acc +6"
  //     ], "5")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202008(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202008b() {
  //   let testCases = [
  //     (["nop +0",
  //       "acc +1",
  //       "jmp +4",
  //       "acc +3",
  //       "jmp -3",
  //       "acc -99",
  //       "acc +1",
  //       "jmp -4",
  //       "acc +6"
  //     ], "8")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202008(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202009a() {
  //   let testCases = [
  //     (["35","20","15","25","47","40","62","55","65","95","102","117","150","182","127","219","299","277","309","576"], "127")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202009(data: input, testing: true)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202009b() {
  //   let testCases = [
  //     (["35","20","15","25","47","40","62","55","65","95","102","117","150","182","127","219","299","277","309","576"], "62")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202009(data: input, testing: true)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202010a() {
  //   let testCases = [
  //     (["16","10","15","5","1","11","7","19","6","12","4"], "35")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202010(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202010b() {
  //   let testCases = [
  //     (["16","10","15","5","1","11","7","19","6","12","4"], "8")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202010(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202010b2() {
  //   let testCases = [
  //     (["28","33","18","42","31","14","46","20","48","47","24","23","49","45","19","38","39","11","1","32","25","35","8","17","7","9","4","2","34","10","3"], "19208")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202010(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202011a() {
  //   let testCases = [
  //     (["L.LL.LL.LL",
  //       "LLLLLLL.LL",
  //       "L.L.L..L..",
  //       "LLLL.LL.LL",
  //       "L.LL.LL.LL",
  //       "L.LLLLL.LL",
  //       "..L.L.....",
  //       "LLLLLLLLLL",
  //       "L.LLLLLL.L",
  //       "L.LLLLL.LL"], "37")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202011(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202011b() {
  //   let testCases = [
  //     (["L.LL.LL.LL",
  //       "LLLLLLL.LL",
  //       "L.L.L..L..",
  //       "LLLL.LL.LL",
  //       "L.LL.LL.LL",
  //       "L.LLLLL.LL",
  //       "..L.L.....",
  //       "LLLLLLLLLL",
  //       "L.LLLLLL.L",
  //       "L.LLLLL.LL"], "26")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202011(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202012a() {
  //   let testCases = [
  //     (["F10","N3","F7","R90","F11"], "25")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202012(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202012b() {
  //   let testCases = [
  //     (["F10","N3","F7","R90","F11"], "286")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202012(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202013a() {
  //   let testCases = [
  //     (["939","7,13,x,x,59,x,31,19"], "295")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202013(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202013b() {
  //   let testCases = [
  //     (["939","7,13,x,x,59,x,31,19"], "1068781")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202013(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202014a() {
  //   let testCases = [
  //     (["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
  //       "mem[8] = 11",
  //       "mem[7] = 101",
  //       "mem[8] = 0"], "165")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202014(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202014b() {
  //   let testCases = [
  //     (["mask = 000000000000000000000000000000X1001X",
  //       "mem[42] = 100",
  //       "mask = 00000000000000000000000000000000X0XX",
  //       "mem[26] = 1"], "208")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202014(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202015a() {
  //   let testCases = [
  //     (["0,3,6"], "436"),
  //     (["1,3,2"], "1"),
  //     (["2,1,3"], "10"),
  //     (["1,2,3"], "27"),
  //     (["2,3,1"], "78"),
  //     (["3,2,1"], "438"),
  //     (["3,1,2"], "1836")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202015(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202015b() {
  //   let testCases = [
  //     (["0,3,6"], "175594"),
  //     (["1,3,2"], "2578"),
  //     (["2,1,3"], "3544142"),
  //     (["1,2,3"], "261214"),
  //     (["2,3,1"], "6895259"),
  //     (["3,2,1"], "18"),
  //     (["3,1,2"], "362")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202015(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202016a() {
  //   let testCases = [
  //     (["class: 1-3 or 5-7",
  //       "row: 6-11 or 33-44",
  //       "seat: 13-40 or 45-50",
  //       "",
  //       "your ticket:",
  //       "7,1,14",
  //       "",
  //       "nearby tickets:",
  //       "7,3,47",
  //       "40,4,50",
  //       "55,2,20",
  //       "38,6,12"], "71")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202016(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202016b() {
  //   let testCases = [
  //     (["class: 0-1 or 4-19",
  //       "row: 0-5 or 8-19",
  //       "seat: 0-13 or 16-19",
  //       "",
  //       "your ticket:",
  //       "11,12,13",
  //       "",
  //       "nearby tickets:",
  //       "3,9,18",
  //       "15,1,5",
  //       "5,14,9"], "12-11-13")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202016(data: input)
  //     XCTAssertEqual(solution.test2, answer)
  //   }
  // }


  // func test202017a() {
  //   let testCases = [
  //     ([".#.","..#","###"], "112")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202017(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202017b() {
  //   let testCases = [
  //     ([".#.","..#","###"], "848")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202017(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202018a() {
  //   let testCases = [
  //     (["1 + 2 * 3 + 4 * 5 + 6"], "71"),
  //     (["1 + (2 * 3) + (4 * (5 + 6))"], "51"),
  //     (["2 * 3 + (4 * 5)"], "26"),
  //     (["5 + (8 * 3 + 9 + 3 * 4 * 3)"], "437"),
  //     (["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], "12240"),
  //     (["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], "13632"),
  //     (["7 + 7"], "14"),
  //     (["6"], "6"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202018(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202018b() {
  //   let testCases = [
  //     (["1 + 2 * 3 + 4 * 5 + 6"], "231"),
  //     (["1 + (2 * 3) + (4 * (5 + 6))"], "51"),
  //     (["2 * 3 + (4 * 5)"], "46"),
  //     (["5 + (8 * 3 + 9 + 3 * 4 * 3)"], "1445"),
  //     (["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], "669060"),
  //     (["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], "23340"),
  //     (["7 * 7"], "49"),
  //     (["6"], "6"),
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202018(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202019a() {
  //   let testCases = [
  //     (["0: 4 1 5",
  //       "1: 2 3 | 3 2",
  //       "2: 4 4 | 5 5",
  //       "3: 4 5 | 5 4",
  //       "4: \"a\"",
  //       "5: \"b\"",
  //       "",
  //       "ababbb",
  //       "bababa",
  //       "abbbab",
  //       "aaabbb",
  //       "aaaabbb"], "2")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202019(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202019b() {
  //   let testCases = [
  //     (["42: 9 14 | 10 1",
  //       "9: 14 27 | 1 26",
  //       "10: 23 14 | 28 1",
  //       "1: \"a\"",
  //       "11: 42 31",
  //       "5: 1 14 | 15 1",
  //       "19: 14 1 | 14 14",
  //       "12: 24 14 | 19 1",
  //       "16: 15 1 | 14 14",
  //       "31: 14 17 | 1 13",
  //       "6: 14 14 | 1 14",
  //       "2: 1 24 | 14 4",
  //       "0: 8 11",
  //       "13: 14 3 | 1 12",
  //       "15: 1 | 14",
  //       "17: 14 2 | 1 7",
  //       "23: 25 1 | 22 14",
  //       "28: 16 1",
  //       "4: 1 1",
  //       "20: 14 14 | 1 15",
  //       "3: 5 14 | 16 1",
  //       "27: 1 6 | 14 18",
  //       "14: \"b\"",
  //       "21: 14 1 | 1 14",
  //       "25: 1 1 | 1 14",
  //       "22: 14 14",
  //       "8: 42",
  //       "26: 14 22 | 1 20",
  //       "18: 15 15",
  //       "7: 14 5 | 1 21",
  //       "24: 14 1",
  //       "",
  //       "abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa",
  //       "aaaabbaaaabbaaa",
  //       "babaaabbbaaabaababbaabababaaab",
  //       "bbabbbbaabaabba",
  //       "babbbbaabbbbbabbbbbbaabaaabaaa",
  //       "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
  //       "bbbbbbbaaaabbbbaaabbabaaa",
  //       "bbbababbbbaaaaaaaabbababaaababaabab",
  //       "ababaaaaaabaaab",
  //       "ababaaaaabbbaba",
  //       "baabbaaaabbaaaababbaababb",
  //       "abbbbabbbbaaaababbbbbbaaaababb",
  //       "aaaaabbaabaaaaababaa",
  //       "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
  //       "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba",
  //     ], "12")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202019(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  func test202020a() {
    let testCases = [
      (["Tile 2311:",
        "..##.#..#.",
        "##..#.....",
        "#...##..#.",
        "####.#...#",
        "##.##.###.",
        "##...#.###",
        ".#.#.#..##",
        "..#....#..",
        "###...#.#.",
        "..###..###",
        "",
        "Tile 1951:",
        "#.##...##.",
        "#.####...#",
        ".....#..##",
        "#...######",
        ".##.#....#",
        ".###.#####",
        "###.##.##.",
        ".###....#.",
        "..#.#..#.#",
        "#...##.#..",
        "",
        "Tile 1171:",
        "####...##.",
        "#..##.#..#",
        "##.#..#.#.",
        ".###.####.",
        "..###.####",
        ".##....##.",
        ".#...####.",
        "#.##.####.",
        "####..#...",
        ".....##...",
        "",
        "Tile 1427:",
        "###.##.#..",
        ".#..#.##..",
        ".#.##.#..#",
        "#.#.#.##.#",
        "....#...##",
        "...##..##.",
        "...#.#####",
        ".#.####.#.",
        "..#..###.#",
        "..##.#..#.",
        "",
        "Tile 1489:",
        "##.#.#....",
        "..##...#..",
        ".##..##...",
        "..#...#...",
        "#####...#.",
        "#..#.#.#.#",
        "...#.#.#..",
        "##.#...##.",
        "..##.##.##",
        "###.##.#..",
        "",
        "Tile 2473:",
        "#....####.",
        "#..#.##...",
        "#.##..#...",
        "######.#.#",
        ".#...#.#.#",
        ".#########",
        ".###.#..#.",
        "########.#",
        "##...##.#.",
        "..###.#.#.",
        "",
        "Tile 2971:",
        "..#.#....#",
        "#...###...",
        "#.#.###...",
        "##.##..#..",
        ".#####..##",
        ".#..####.#",
        "#..#.#..#.",
        "..####.###",
        "..#.#.###.",
        "...#.#.#.#",
        "",
        "Tile 2729:",
        "...#.#.#.#",
        "####.#....",
        "..#.#.....",
        "....#..#.#",
        ".##..##.#.",
        ".#.####...",
        "####.#.#..",
        "##.####...",
        "##..#.##..",
        "#.##...##.",
        "",
        "Tile 3079:",
        "#.#.#####.",
        ".#..######",
        "..#.......",
        "######....",
        "####.#..#.",
        ".#...#.##.",
        "#.#####.##",
        "..#.###...",
        "..#.......",
        "..#.###..."], "20899048083289")
    ]
    for (input, answer) in testCases {
      let solution = Solution202020(data: input)
      XCTAssertEqual(solution.part1, answer)
    }
  }

  // func test202020b() {
  //   let testCases = [
  //     ([""], "-1")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202020(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202021a() {
  //   let testCases = [
  //     (["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
  //       "trh fvjkl sbzzf mxmxvkd (contains dairy)",
  //       "sqjhc fvjkl (contains soy)",
  //       "sqjhc mxmxvkd sbzzf (contains fish)"], "5")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202021(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202021b() {
  //   let testCases = [
  //     (["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
  //       "trh fvjkl sbzzf mxmxvkd (contains dairy)",
  //       "sqjhc fvjkl (contains soy)",
  //       "sqjhc mxmxvkd sbzzf (contains fish)"], "mxmxvkd,sqjhc,fvjkl")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202021(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202022a() {
  //   let testCases = [
  //     (["Player 1:",
  //       "9",
  //       "2",
  //       "6",
  //       "3",
  //       "1",
  //       "",
  //       "Player 2:",
  //       "5",
  //       "8",
  //       "4",
  //       "7",
  //       "10"], "306")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202022(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202022b() {
  //   let testCases = [
  //     (["Player 1:",
  //       "9",
  //       "2",
  //       "6",
  //       "3",
  //       "1",
  //       "",
  //       "Player 2:",
  //       "5",
  //       "8",
  //       "4",
  //       "7",
  //       "10"], "291")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202022(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202023a() {
  //   let testCases = [
  //     (["389125467"], "67384529")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202023(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202023b() {
  //   let testCases = [
  //     (["389125467"], "149245887792")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202023(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202024a() {
  //   let testCases = [
  //     (["sesenwnenenewseeswwswswwnenewsewsw",
  //       "neeenesenwnwwswnenewnwwsewnenwseswesw",
  //       "seswneswswsenwwnwse",
  //       "nwnwneseeswswnenewneswwnewseswneseene",
  //       "swweswneswnenwsewnwneneseenw",
  //       "eesenwseswswnenwswnwnwsewwnwsene",
  //       "sewnenenenesenwsewnenwwwse",
  //       "wenwwweseeeweswwwnwwe",
  //       "wsweesenenewnwwnwsenewsenwwsesesenwne",
  //       "neeswseenwwswnwswswnw",
  //       "nenwswwsewswnenenewsenwsenwnesesenew",
  //       "enewnwewneswsewnwswenweswnenwsenwsw",
  //       "sweneswneswneneenwnewenewwneswswnese",
  //       "swwesenesewenwneswnwwneseswwne",
  //       "enesenwswwswneneswsenwnewswseenwsese",
  //       "wnwnesenesenenwwnenwsewesewsesesew",
  //       "nenewswnwewswnenesenwnesewesw",
  //       "eneswnwswnwsenenwnwnwwseeswneewsenese",
  //       "neswnwewnwnwseenwseesewsenwsweewe",
  //       "wseweeenwnesenwwwswnew"], "10")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202024(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202024b() {
  //   let testCases = [
  //     (["sesenwnenenewseeswwswswwnenewsewsw",
  //       "neeenesenwnwwswnenewnwwsewnenwseswesw",
  //       "seswneswswsenwwnwse",
  //       "nwnwneseeswswnenewneswwnewseswneseene",
  //       "swweswneswnenwsewnwneneseenw",
  //       "eesenwseswswnenwswnwnwsewwnwsene",
  //       "sewnenenenesenwsewnenwwwse",
  //       "wenwwweseeeweswwwnwwe",
  //       "wsweesenenewnwwnwsenewsenwwsesesenwne",
  //       "neeswseenwwswnwswswnw",
  //       "nenwswwsewswnenenewsenwsenwnesesenew",
  //       "enewnwewneswsewnwswenweswnenwsenwsw",
  //       "sweneswneswneneenwnewenewwneswswnese",
  //       "swwesenesewenwneswnwwneseswwne",
  //       "enesenwswwswneneswsenwnewswseenwsese",
  //       "wnwnesenesenenwwnenwsewesewsesesew",
  //       "nenewswnwewswnenesenwnesewesw",
  //       "eneswnwswnwsenenwnwnwwseeswneewsenese",
  //       "neswnwewnwnwseenwseesewsenwsweewe",
  //       "wseweeenwnesenwwwswnew"], "2208")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202024(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

  // func test202025a() {
  //   let testCases = [
  //     (["5764801","17807724"], "14897079")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202025(data: input)
  //     XCTAssertEqual(solution.part1, answer)
  //   }
  // }

  // func test202025b() {
  //   let testCases = [
  //     ([""], "-1")
  //   ]
  //   for (input, answer) in testCases {
  //     let solution = Solution202025(data: input)
  //     XCTAssertEqual(solution.part2, answer)
  //   }
  // }

}
