func surfaceArea(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return 2*h*w + 2*h*l + 2*w*l
}

func smallestSideArea(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return min(h*w, h*l, w*l)
}

func smallestSidePerimeter(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return min(2*h+2*w, 2*h+2*l, 2*w+2*l)
}

func volume(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return h*w*l
}

func paper(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return surfaceArea(h,w,l) + smallestSideArea(h,w,l)
}

func ribbon(_ h:Int, _ w:Int, _ l:Int) -> Int
{
    return volume(h,w,l) + smallestSidePerimeter(h,w,l)
}

func total(presents:String, material:(Int,Int,Int)-> Int) -> Int
{
    var total = 0
    for present in presents.split(separator:"\n")
    {
        if present.contains("x") {
            let dims = present.split(separator:"x").map{Int($0)!}
            total += material(dims[0],dims[1],dims[2])
        }
    }
    return total
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
print("Part 1: \(total(presents:input, material:paper))")
print("Part 2: \(total(presents:input, material:ribbon))")
