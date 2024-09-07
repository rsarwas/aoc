use std::collections::HashSet;

fn main() {
    // Select one of the input methods

    inline_tests();
    //read_stdin();
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

#[derive(Debug)]
struct Move {
    turn: Turn,
    distance: i32,
}

#[derive(Debug)]
struct Location {
    heading: Orientation,
    x: i32,
    y: i32,
}

#[derive(Copy, Clone, Debug)]
enum Orientation {
    North,
    East,
    South,
    West,
}

#[derive(Copy, Clone, Debug)]
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
    fn start() -> Self {
        Location {
            heading: Orientation::North,
            x: 0,
            y: 0,
        }
    }
    /// Update the location by walking as instructed
    fn walk(&mut self, instructions: &Move) {
        self.heading = self.heading.turn(instructions.turn);
        match self.heading {
            Orientation::North => self.y += instructions.distance,
            Orientation::South => self.y -= instructions.distance,
            Orientation::East => self.x += instructions.distance,
            Orientation::West => self.x -= instructions.distance,
        }
    }

    fn walk2(&self, instructions: &Move) -> Location {
        let heading = self.heading.turn(instructions.turn);
        let (mut x, mut y) = (self.x, self.y);
        match heading {
            Orientation::North => y += instructions.distance,
            Orientation::South => y -= instructions.distance,
            Orientation::East => x += instructions.distance,
            Orientation::West => x -= instructions.distance,
        };
        Location {
            heading: heading,
            x: x,
            y: y,
        }
    }

    /// Manhattan distance from (0,0)
    // fn manhattan(&self) -> i32 {
    //     self.x.abs() + self.y.abs()
    // }

    /// manhattan distance from the other location
    fn manhattan(&self, other: &Location) -> i32 {
        (other.x - self.x).abs() + (other.y - self.y).abs()
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
    let data = Data { input: input };
    let start = Location::start();
    let end = data.into_iter().fold(start, |acc, x| acc.walk2(&x));
    Ok(end.manhattan(&Location::start()))
}
/// Solve Part 2 of the Puzzle
///
/// When do we come to a location we have been to before?
fn solve_part2(input: &[u8]) -> Result<i32, String> {
    let data = Data { input: input };
    let mut locations = HashSet::new();
    let mut location = Location::start();
    locations.insert((location.x, location.y));
    for item in &data {
        location.walk(&item);
        println!(
            "move({:?},{}) to ({},{})",
            item.turn, item.distance, location.x, location.y
        );
        if locations.contains(&(location.x, location.y)) {
            break;
        }
        locations.insert((location.x, location.y));
    }
    Ok(location.manhattan(&Location::start()))
}

/// Wrapper for the input, so we can create a custom iterator for the [u8]
struct Data<'a> {
    input: &'a [u8],
}

impl<'a> IntoIterator for &'a Data<'a> {
    type Item = Move;
    type IntoIter = DataIterator<'a>;

    fn into_iter(self) -> Self::IntoIter {
        DataIterator {
            input: self.input,
            index: 0,
            distance: 0,
            turn: None,
        }
    }
}

/// Iterator over the Data which yields a sequence of Moves
struct DataIterator<'a> {
    input: &'a [u8],
    index: usize,
    distance: i32,
    turn: Option<Turn>,
}

impl<'a> Iterator for DataIterator<'a> {
    type Item = Move;
    fn next(&mut self) -> Option<Move> {
        while self.index < self.input.len() {
            let symbol = self.input[self.index];
            match symbol {
                LEFT => {
                    self.turn = Some(Turn::Left);
                }
                RIGHT => {
                    self.turn = Some(Turn::Right);
                }
                ZERO..=NINE => {
                    self.distance = self.distance * 10 + ((symbol - ZERO) as i32);
                }
                COMMA | NEWLINE => {
                    // return a move
                    if let Some(t) = self.turn {
                        let distance = self.distance;
                        self.distance = 0;
                        self.turn = None;
                        self.index += 1;
                        return Some(Move {
                            turn: t,
                            distance: distance,
                        });
                    } else {
                        //TODO: return a Result with an explanation for why parsing failed
                        return None;
                    }
                }
                SPACE => {}
                _ => {
                    // TODO: return a Result instead of aborting the iterator without explanation
                    // return Err(format!(
                    //     "Unexpected token ({}) in input.",
                    //     char::from(symbol)
                    // ));
                    return None;
                }
            }
            self.index += 1;
        }
        // in case the input did not end with a comma or a newline
        if let Some(t) = self.turn {
            self.turn = None;
            return Some(Move {
                turn: t,
                distance: self.distance,
            });
        }
        return None;
    }
}
