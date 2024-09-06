fn main() {
    // Select one of the input methods

    //inline_tests();
    read_stdin();
    //read_file("input.txt");
}

/// Read test case input from static strings
#[allow(dead_code)]
fn inline_tests() {
    let part1_test_cases = [("R2, L3", 5), ("R2, R2, R2", 2), ("R5, L5, R5, R3", 12)];
    let part2_test_cases = [("R8, R4, R4, R8", 4)];
    for (test_number, (test_data, result)) in part1_test_cases.iter().enumerate() {
        println!("Part 1 Test #{}; Input: {}", test_number + 1, test_data);
        match solve_part1(test_data.as_bytes()) {
            Ok(answer) => {
                let status = if *result == answer { "PASS" } else { "FAIL" };
                println!("  {}; Expected {}, Got {} ", status, result, answer)
            }
            Err(error) => println!("  Execution Failed: {}", error),
        };
    }
    for (test_number, (test_data, result)) in part2_test_cases.iter().enumerate() {
        println!("Part 2 Test #{}; Input: {}", test_number + 1, test_data);
        match solve_part2(test_data.as_bytes()) {
            Ok(answer) => {
                let status = if *result == answer { "PASS" } else { "FAIL" };
                println!("  {}; Expected {}, Got {} ", status, result, answer)
            }
            Err(error) => println!("  Execution Failed: {}", error),
        };
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

struct Location {
    x: i32,
    y: i32,
}

enum Orientation {
    North,
    East,
    South,
    West,
}

enum Turn {
    Left,
    Right,
}

impl Orientation {
    /// Return the new orientation after turning left or right
    fn turn(self, direction: Turn) -> Self {
        match direction {
            Turn::Left => match self {
                Orientation::North => Orientation::West,
                Orientation::West => Orientation::South,
                Orientation::South => Orientation::East,
                Orientation::East => Orientation::North,
            },
            Turn::Right => match self {
                Orientation::North => Orientation::East,
                Orientation::East => Orientation::South,
                Orientation::South => Orientation::West,
                Orientation::West => Orientation::North,
            },
        }
    }
}

impl Location {
    /// Update the location by moving the given distance in the given direction
    fn walk(&mut self, direction: &Orientation, distance: i32) {
        match direction {
            Orientation::North => self.y += distance,
            Orientation::South => self.y -= distance,
            Orientation::East => self.x += distance,
            Orientation::West => self.x -= distance,
        }
    }
    /// Manhattan distance from (0,0)
    fn manhattan(&self) -> i32 {
        self.x.abs() + self.y.abs()
    }
}

/// Valid symbols in the input file
const LEFT: u8 = b'L'; // ASCII 'L' 76
const RIGHT: u8 = b'R'; // ASCII 'R' 82
const ZERO: u8 = b'0'; // ASCII '0' 48
const NINE: u8 = b'9'; // ASCII '9' 57
const COMMA: u8 = b','; // ASCII ',' 44
const SPACE: u8 = b' '; // ASCII ' ' 32
const NEWLINE: u8 = b'\n'; // ASCII newline 12

/// Solve Part 1 of the Puzzle
///
/// After executing a series or turns and forward motion,
/// how far from the start as we from the start
/// Give the answer in taxi/manhattan distance.
fn solve_part1(input: &[u8]) -> Result<i32, String> {
    let mut distance: i32 = 0;
    let mut location = Location { x: 0, y: 0 };
    let mut orientation = Orientation::North;
    for &symbol in input {
        match symbol {
            LEFT => {
                orientation = orientation.turn(Turn::Left);
            }
            RIGHT => {
                orientation = orientation.turn(Turn::Right);
            }
            ZERO..=NINE => {
                distance = distance * 10 + ((symbol - ZERO) as i32);
            }
            COMMA => {
                // time to make a move
                location.walk(&orientation, distance);
                distance = 0;
            }
            SPACE | NEWLINE => {}
            _ => {
                return Err(format!(
                    "Unexpected token ({}) in input.",
                    char::from(symbol)
                ));
            }
        }
    }
    //If there is an un-walked distance, then process it (input does not have a final comma)
    if distance > 0 {
        location.walk(&orientation, distance)
    }
    Ok(location.manhattan())
}
/// Solve Part 2 of the Puzzle
///
/// How many moves (input characters) until the elf is in the basement?
fn solve_part2(input: &[u8]) -> Result<usize, String> {
    Err("Not implemented".to_string())
}
