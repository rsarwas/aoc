struct Problem202014: Problem {
  var name: String { "2020-14" }
  func solveWith(data: [String]) -> Solution { Solution202014(data: data) }
}

struct Solution202014: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: UInt64 {
    var mem = [UInt64: UInt64]()
    var mask: (UInt64, UInt64) = (0,0)
    for line in data {
      if line.starts(with: "mask") {
        if let newMask = line.asMask {
          mask = newMask
        }
        //print("mask: \(mask)")
      } else {
        if let (address, value) = line.asMemoryOperation {
          mem[address] = apply(mask: mask, to: value)
          //print("write: \(value) to \(address)")
        }
      }
    }
    let total = mem.values.reduce(0) { $0 + $1 }
    return total
  }

  var answer2: UInt64 {
    var mem = [UInt64: UInt64]()
    var mask: (UInt64, UInt64) = (0,0)
    for line in data {
      if line.starts(with: "mask") {
        if let newMask = line.asMask2 {
          mask = newMask
        }
        //print("mask: \(mask)")
      } else {
        if let (address, value) = line.asMemoryOperation {
          for newAddress in addresses(for: mask, from: address) {
            //print("write: \(value) to \(address)")
            mem[newAddress] = value
          }
        }
      }
    }
    let total = mem.values.reduce(0) { $0 + $1 }
    return total
  }

  func apply(mask: (UInt64, UInt64), to value: UInt64) -> UInt64 {
    // mask.0 is all 1s except where the output should be 0; then there is a 0
    // mask.1 is all 0s except where the output should be 1; then there is a 1
    return (value | mask.1) & mask.0
  }

  func addresses(for mask: (UInt64, UInt64), from address: UInt64) -> [UInt64] {
    // mask.0 is all 0s except where there is an floating value(X) which is a 1
    // mask.1 is all 0s except where the output should be 1; then there is a 1
    let newAddress = address | mask.1  // Set bits that should always be 1
    var addresses = [newAddress]
    for i in 0..<36 {
      let floatMask: UInt64 = 1 << i
      if mask.0 & floatMask == floatMask {
        var newAddresses = [UInt64]()
        for address in addresses {
          // 1 at bit i
          newAddresses.append(address | floatMask)
          // 0 at bit i
          newAddresses.append(address & ~floatMask)
        }
        addresses = newAddresses
      }
    }
    return addresses
  }
}

extension String {
  var asMask: (UInt64, UInt64)? {
    // mask.0 is all 1s except where the output should be 0; then there is a 0
    // mask.1 is all 0s except where the output should be 1; then there is a 1
    // drop "mask = " (7 characters at start)
    let mask0 = UInt64( String(self.dropFirst(7).map { $0 == "0" ? "0" : "1" }), radix:2)
    let mask1 = UInt64( String(self.dropFirst(7).map { $0 == "1" ? "1" : "0" }), radix:2)
    if mask0 == nil || mask1 == nil { return nil }
    return (mask0!, mask1!)
  }

  var asMask2: (UInt64, UInt64)? {
    // mask.0 is all 0s except where there is an floating value(X) which is a 1
    // mask.1 is all 0s except where the output should be 1; then there is a 1
    // drop "mask = " (7 characters at start)
    let mask0 = UInt64( String(self.dropFirst(7).map { $0 == "X" ? "1" : "0" }), radix:2)
    let mask1 = UInt64( String(self.dropFirst(7).map { $0 == "1" ? "1" : "0" }), radix:2)
    if mask0 == nil || mask1 == nil { return nil }
    return (mask0!, mask1!)
  }

  var asMemoryOperation: (UInt64,UInt64)? {
    let parts = self.split(separator: " ")
    guard parts.count == 3 else { return nil }
    guard let value = UInt64(parts[2])  else { return nil }
    let parts2 = parts[0].split(separator: "[")
    guard parts2.count == 2 else { return nil }
    let parts3 = parts2[1].split(separator: "]")
    guard parts3.count > 0 else { return nil }
    guard let address = UInt64(parts3[0])  else { return nil }
    return (address, value)
  }
}