public protocol Problem {
  var name: String { get }
  func solveWith(data: [String]) -> Solution
}

public protocol Solution {
  var part1: String { get }
  var part2: String { get }
}

public func getProblemFromCmdLine() -> Problem {
  guard CommandLine.arguments.count > 1 else { return Problem20YYDD() }
  if CommandLine.arguments[1] == "2015-01" { return Problem201501() }
  if CommandLine.arguments[1] == "2015-02" { return Problem201502() }
  if CommandLine.arguments[1] == "2015-03" { return Problem201503() }
  if CommandLine.arguments[1] == "2018-03" { return Problem201803() }
  if CommandLine.arguments[1] == "2020-01" { return Problem202001() }
  if CommandLine.arguments[1] == "2020-02" { return Problem202002() }
  if CommandLine.arguments[1] == "2020-03" { return Problem202003() }
  if CommandLine.arguments[1] == "2020-04" { return Problem202004() }
  if CommandLine.arguments[1] == "2020-05" { return Problem202005() }
  if CommandLine.arguments[1] == "2020-06" { return Problem202006() }
  if CommandLine.arguments[1] == "2020-07" { return Problem202007() }
  if CommandLine.arguments[1] == "2020-08" { return Problem202008() }
  if CommandLine.arguments[1] == "2020-09" { return Problem202009() }
  if CommandLine.arguments[1] == "2020-10" { return Problem202010() }
  if CommandLine.arguments[1] == "2020-11" { return Problem202011() }
  if CommandLine.arguments[1] == "2020-12" { return Problem202012() }
  if CommandLine.arguments[1] == "2020-13" { return Problem202013() }
  if CommandLine.arguments[1] == "2020-14" { return Problem202014() }
  if CommandLine.arguments[1] == "2020-15" { return Problem202015() }
  if CommandLine.arguments[1] == "2020-16" { return Problem202016() }
  if CommandLine.arguments[1] == "2020-17" { return Problem202017() }
  if CommandLine.arguments[1] == "2020-18" { return Problem202018() }
  if CommandLine.arguments[1] == "2020-19" { return Problem202019() }
  if CommandLine.arguments[1] == "2020-20" { return Problem202020() }
  if CommandLine.arguments[1] == "2020-21" { return Problem202021() }
  if CommandLine.arguments[1] == "2020-22" { return Problem202022() }
  if CommandLine.arguments[1] == "2020-23" { return Problem202023() }
  if CommandLine.arguments[1] == "2020-24" { return Problem202024() }
  if CommandLine.arguments[1] == "2020-25" { return Problem202025() }
  return Problem20YYDD()
}

public func getLinesFromStdin() -> [String] {
  var results = [String]()
  while let line = readLine(strippingNewline: true) {
    results.append(line)
  }
  return results
}
