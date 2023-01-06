function what_floor(text)
	floor = 0
    for char in text
		char == '(' && (floor += 1)
		char == ')' && (floor -= 1)
    end
	return floor
end

function when_basement(text)
	floor = 0
    for (index,char) in enumerate(text)
		char == '(' && (floor += 1)
		char == ')' && (floor -= 1)
        floor == -1 && return index
    end
	return -1
end

input = read(stdin, String)
println("Part 1: $(what_floor(input))")
println("Part 2: $(when_basement(input))")
