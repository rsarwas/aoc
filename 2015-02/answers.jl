surface_area(h, w, l) = 2*h*w + 2*h*l + 2*w*l

smallest_side_area(h, w, l) = min(h*w, h*l, w*l)

smallest_side_perimeter(h, w, l) = min(2*h+2*w, 2*h+2*l, 2*w+2*l)

volume(h,w,l) = h*w*l

ribbon(h,w,l) = volume(h,w,l) + smallest_side_perimeter(h,w,l)

paper(h,w,l) = surface_area(h,w,l) + smallest_side_area(h,w,l)

function total(presents, material)
    total = 0
    for present in split(presents,"\n")
        if occursin("x", present)
            dims = map(x->parse(Int,x), split(present,"x"))
            total += material(dims...)
        end
    end
    total
end

input = read(stdin, String)
println("Part 1: $(total(input, paper))")
println("Part 2: $(total(input, ribbon))")
