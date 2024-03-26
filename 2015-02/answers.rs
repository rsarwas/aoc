fn main() {
    // Select one of the input methods

    //inline_tests();
    read_stdin();
    //read_file("input.txt");
}

/// Read test case input from static strings
#[allow(dead_code)]
fn inline_tests() {
    let test_cases = ["2x3x4", "2x3x4\n1x1x10\n"];
    for (test_number, &test_data) in test_cases.iter().enumerate() {
        println!("\nTest #{}; Input: {}", test_number + 1, test_data);
        solve(test_data.as_bytes());
    }
}

#[allow(dead_code)]
///Read the input from the standard input
fn read_stdin() {
    use std::io::{self, BufRead};

    let mut stdin = io::stdin().lock();
    let input = stdin.fill_buf().unwrap();
    solve(&input);
}

#[allow(dead_code)]
/// Read the input from a file
fn read_file(name: &str) {
    use std::fs;

    let input = fs::read(name).unwrap();
    solve(&input);
}

/// Generic Solver and result printer
fn solve(input: &[u8]) {
    match solve_part1(input) {
        Ok(answer) => println!("Part 1: {}", answer),
        Err(error) => println!("Part 1 Failed: {}", error),
    };
    match solve_part2(input) {
        Ok(answer) => println!("Part 2: {}", answer),
        Err(error) => println!("Part 2 Failed: {}", error),
    };
}

/// Solve Part 1 of the Puzzle
///
/// How much paper does it take to wrap all the presents
fn solve_part1(input: &[u8]) -> Result<usize, String> {
    Ok(total(&input, paper))
}

/// Solve Part 2 of the Puzzle
///
/// How much ribbon does it take to wrap all the presents
fn solve_part2(input: &[u8]) -> Result<usize, String> {
    Ok(total(&input, ribbon))
}

/// Total up all of the material for all the input
///
/// Return a 1 if we go up '(', and a -1 if we go down ')'
fn total(input: &[u8], material: fn(usize, usize, usize) -> usize) -> usize {
    let mut total: usize = 0;
    let presents = input.split(|&c| c == b'\n');
    for present in presents {
        // Skip empty present (from trailing and or duplicate newline)
        if present.len() == 0 {
            continue;
        }
        let dims: Vec<usize> = present
            .split(|c| *c == b'x')
            .map(|bytes| {
                let the_string = std::str::from_utf8(bytes).expect("not UTF-8");
                let number: usize = the_string.parse().expect("not a number");
                number
            })
            .collect();
        total += material(dims[0], dims[1], dims[2])
    }
    total
}

/// Calculate the amount of paper for a hxwxl sized present
fn paper(h: usize, w: usize, l: usize) -> usize {
    surface_area(h, w, l) + smallest_side_area(h, w, l)
}

/// Calculate the amount of ribbon for a hxwxl sized present
fn ribbon(h: usize, w: usize, l: usize) -> usize {
    volume(h, w, l) + smallest_side_perimeter(h, w, l)
}

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
