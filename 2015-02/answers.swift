struct Package {
  let width: Int
  let length: Int
  let height: Int

  var paper: Int { return surfaceArea + smallestSideArea }
  var ribbon: Int { return volume + smallestSidePerimeter }
  var smallestSideArea: Int { return min(height * width, height * length, width * length) }
  var smallestSidePerimeter: Int {
    return min(2 * height + 2 * width, 2 * height + 2 * length, 2 * width + 2 * length)
  }
  var surfaceArea: Int { return 2 * height * width + 2 * height * length + 2 * width * length }
  var volume: Int { return height * width * length }
}

extension String {
  var asPackage: Package? {
    let dims = self.split(separator: "x").compactMap { Int($0) }
    guard dims.count == 3 else { return nil }
    return Package(width: dims[0], length: dims[1], height: dims[2])
  }
}

var stdinLines: [String] {
  var lines: [String] = []
  while let line = readLine(strippingNewline: true) {
    lines.append(line)
  }
  return lines
}

func main() {
  let packages = stdinLines.compactMap { $0.asPackage }
  let total_paper = packages.reduce(0) { $0 + $1.paper }
  let total_ribbon = packages.reduce(0) { $0 + $1.ribbon }
  print("Part 1: \(total_paper)")
  print("Part 2: \(total_ribbon)")
}

main()
