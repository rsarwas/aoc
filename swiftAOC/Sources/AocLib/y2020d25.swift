struct Problem202025: Problem {
  var name: String { "2020-25" }
  func solveWith(data: [String]) -> Solution { Solution202025(data: data) }
}

struct Solution202025: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    guard data.count == 2 else { return -1 }
    guard let cardPublicKey = Int(data[0]) else { return -1 }
    guard let doorPublicKey = Int(data[1]) else { return -1 }
    //print(cardPublicKey, doorPublicKey)
    let magic = (7, 20201227)
    guard let cardLoopSize = decode(magic: magic, code: cardPublicKey) else { return -1 }
    //guard let doorLoopSize = decode(magic: magic, code: doorPublicKey) else { return -1 }
    //print(cardLoopSize, doorLoopSize)
    let cardEncryptionKey = encode(magic: magic, loop: cardLoopSize, subject: doorPublicKey)
    //let doorEncryptionKey = encode(magic: magic, loop: doorLoopSize, subject: cardPublicKey)
    //print(cardEncryptionKey, doorEncryptionKey)
    //guard cardEncryptionKey == doorEncryptionKey else { return -1 }
    return cardEncryptionKey
  }

  var answer2: Int {
    return -1
  }

  func decode(magic: (Int,Int), code: Int) -> Int? {
    var value = 1
    for loop in 0..<magic.1 {
      value = (value * magic.0) % magic.1
      if value == code { return loop + 1 }
    }
    return nil
  }

  func encode(magic: (Int,Int), loop: Int, subject: Int) -> Int {
    var code = 1
    for _ in 0..<loop {
      code = (code * subject) % magic.1
    }
    return code
  }

}
