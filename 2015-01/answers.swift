func what_floor(_ text:String) -> Int
{
    var floor = 0
    for char in text
    {
        if char == "(" { floor += 1 }
        if char == ")" { floor -= 1 }
    }
    return floor
}

func when_basement(_ text:String) -> Int
{
    var floor = 0
    var position = 0
    for char in text
    {
        position += 1
        if char == "(" { floor += 1 }
        if char == ")" { floor -= 1 }
        if floor == -1 { return position }
    }
    return -1
}

func getStdin() -> String
{
    var input = ""
    while let line = readLine(strippingNewline:false)
    {
        input += line
    }
    return input
}

let input = getStdin()
print("Part 1: \(what_floor(input))")
print("Part 2: \(when_basement(input))")
