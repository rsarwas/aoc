import Foundation
struct Problem202004: Problem {
  var name: String { "2020-04" }
  func solveWith(data: [String]) -> Solution { Solution202004(data: data) }
}

struct Solution202004: Solution {
  let data: [String]

  var part1: String {
    return "\(countValidPassports)"
  }

  var part2: String {
    return "\(countValidPassports2)"
  }

  var countValidPassports: Int {
    let passports = data.asPassports
    return passports.filter { $0.hasAllKeys }.count
  }

  var countValidPassports2: Int {
    let passports = data.asPassports
    return passports.filter { $0.valid }.count
  }


}

extension Array where Element == String {
  var asPassports: [Passport] {
    var passports = [Passport]()
    var fields = Dictionary<String, String>()
    for line in self {
      if line.isEmpty {
        passports.append(Passport(fields: fields))
        fields.removeAll()
      }
      let pairs = line.split(separator: " ")
      for pair in pairs {
        let keyValue = pair.split(separator: ":")
        fields[String(keyValue[0])] = String(keyValue[1])
      }
    }
    return passports
  }
}

struct Passport {
  let fields: Dictionary<String,String>
    // byr (Birth Year)
    // iyr (Issue Year)
    // eyr (Expiration Year)
    // hgt (Height)
    // hcl (Hair Color)
    // ecl (Eye Color)
    // pid (Passport ID)
    // cid (Country ID)
  let requiredKeys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
  // not required: cid

  var hasAllKeys: Bool {
    for key in requiredKeys {
      if !fields.keys.contains(key) { return false }
    }
    return true
  }

  var valid: Bool {
    // byr (Birth Year) - four digits; at least 1920 and at most 2002.
    // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    // hgt (Height) - a number followed by either cm or in:
    //     If cm, the number must be at least 150 and at most 193.
    //     If in, the number must be at least 59 and at most 76.
    // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    // pid (Passport ID) - a nine-digit number, including leading zeroes.
    // cid (Country ID) - ignored, missing or not.
    guard let val1 = fields["byr"], let byr = Int(val1), 1920 <= byr, byr <= 2002 else { return false }
    guard let val2 = fields["iyr"], let iyr = Int(val2), 2010 <= iyr, iyr <= 2020 else { return false }
    guard let val3 = fields["eyr"], let eyr = Int(val3), 2020 <= eyr, eyr <= 2030 else { return false }
    guard let hgt = fields["hgt"], validHeight(hgt) else { return false }
    guard let hcl = fields["hcl"], validColor(hcl) else { return false }
    guard let ecl = fields["ecl"], ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].contains(ecl) else { return false }
    guard let pid = fields["pid"], let _ = Int(pid), pid.count == 9 else { return false }
    return true
  }

  private func validColor(_ clr: String) -> Bool {
    // A regex solution would be much nicer, but regex in swift is still ugly
    let hex = "0123456789abcdef"
    guard clr.hasPrefix("#"), clr.count == 7 else { return false }
    let clr2 = clr.replacingOccurrences(of: "#", with: "")
    for char in clr2 {
      if !hex.contains(char) { return false }
    }
    return true
  }

  private func validHeight(_ hgt: String) -> Bool {
    // A regex solution would be much nicer, but regex in swift is still ugly
    if hgt.hasSuffix("in") {
      let val = Int(hgt.replacingOccurrences(of: "in", with: ""))
      guard let inches = val, 59 <= inches, inches <= 76 else { return false }
      return true
    }
    if hgt.hasSuffix("cm") {
      let val = Int(hgt.replacingOccurrences(of: "cm", with: ""))
      guard let cm = val, 150 <= cm, cm <= 193 else { return false }
      return true
    }
    return false
  }
}