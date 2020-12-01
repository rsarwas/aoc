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
  if CommandLine.arguments[1] == "2020-01" { return Problem202001() }
  return Problem20YYDD()
}

public func getLinesFromStdin() -> [String] {
  var results = [String]()
  while let line = readLine(strippingNewline: true) {
    results.append(line)
  }
  return results
}
