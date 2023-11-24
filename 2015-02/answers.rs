fn surface_area(h: usize, w: usize, l: usize) -> usize {
    2 * h * w + 2 * h * l + 2 * w * l
}

fn smallest_side_area(h: usize, w: usize, l: usize) -> usize {
    *[h * w, h * l, w * l].iter().min().unwrap_or(&0)
}

fn smallest_side_perimeter(h: usize, w: usize, l: usize) -> usize {
    *[2 * h + 2 * w, 2 * h + 2 * l, 2 * w + 2 * l]
        .iter()
        .min()
        .unwrap_or(&0)
}

fn volume(h: usize, w: usize, l: usize) -> usize {
    h * w * l
}

fn ribbon(h: usize, w: usize, l: usize) -> usize {
    volume(h, w, l) + smallest_side_perimeter(h, w, l)
}

fn paper(h: usize, w: usize, l: usize) -> usize {
    surface_area(h, w, l) + smallest_side_area(h, w, l)
}

fn total(presents: &Vec<String>, material: fn(usize, usize, usize) -> usize) -> usize {
    let mut total: usize = 0;
    for present in presents {
        if present.contains("x") {
            let dims: Vec<usize> = present
                .split(|c: char| c == 'x')
                .map(|x| x.parse().unwrap_or_default())
                .collect();
            total += material(dims[0], dims[1], dims[2])
        }
    }
    total
}

fn read_lines() -> Vec<String> {
    use std::io::prelude::*;
    let stdin = std::io::stdin();
    let v = stdin.lock().lines().map(|x| x.unwrap()).collect();
    v
}

fn main() {
    let input = read_lines();
    println!("Part 1: {}", total(&input, paper));
    println!("Part 1: {}", total(&input, ribbon));
}
