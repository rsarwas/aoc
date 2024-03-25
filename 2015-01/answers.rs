fn main() {
    // Select one of the input methods

    //inline_tests();
    read_stdin();
    //read_file("input.txt");
}

/// Read test case input from static strings
#[allow(dead_code)]
fn inline_tests() {
    let test_cases = ["((!))", "(())", "()))", ")()((", ")()\n"];
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
/// What floor is the elf on after making all the moves in the input?
fn solve_part1(input: &[u8]) -> Result<i32, String> {
    let mut current_floor = 0;
    for symbol in input {
        current_floor += up_or_down(symbol)?;
    }
    Ok(current_floor)
}
/// Solve Part 2 of the Puzzle
///
/// How many moves (input characters) until the elf is in the basement?
fn solve_part2(input: &[u8]) -> Result<usize, String> {
    let mut current_floor = 0;
    for (move_number, symbol) in input.iter().enumerate() {
        current_floor += up_or_down(symbol)?;
        if current_floor < 0 {
            return Ok(move_number + 1);
        }
    }
    Err(format!(
        "Never got to the basement after {} moves",
        input.len()
    ))
}

/// Interpret the input symbol
///
/// Return a 1 if we go up '(', and a -1 if we go down ')'
fn up_or_down(symbol: &u8) -> Result<i32, String> {
    match symbol {
        b'(' => Ok(1),
        b')' => Ok(-1),
        b'\n' => Ok(0), //Don't fail if there is a newline at the end of the input
        _ => Err(format!(
            "Invalid Input: found '{}', expecting '(' or ')'",
            char::from(*symbol)
        )),
    }
}
