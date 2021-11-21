var total = 0
while let line = readLine()
{
    if let number = Int(line) { total += number }
}
print("Part 1: \(total)")
