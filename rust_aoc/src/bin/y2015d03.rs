//use core::ascii;
use std::io::BufRead;
//use std::str::Chars;
use std::collections::HashSet;

pub enum Input {
    Const(&'static str),
    File(&'static str),
    Stdin,
}

impl Input {
    fn string(&self) -> String {
        match &self {
            Input::Const(s) => s.to_string(),
            Input::File(s) => std::fs::read_to_string(s).expect("Unable to read file"),
            Input::Stdin => std::io::stdin()
                .lock()
                .lines()
                .next()
                .unwrap()
                .expect("stdin fail"),
        }
    }
}

enum Direction {
    North,
    South,
    East,
    West,
}

impl Direction {
    // fn from_utf8(ch:char) -> Direction {
    //     match ch {
    //         '^' => Direction::North,
    //         'v' => Direction::South,
    //         '>' => Direction::East,
    //         '<' => Direction::West,
    //         _ => panic!("Unexpected character ({ch}) for Direction (expected: ^,v,>,<)")
    //     }
    // }
    fn from_byte(b: &u8) -> Direction {
        match b {
            b'^' => Direction::North,
            b'v' => Direction::South,
            b'>' => Direction::East,
            b'<' => Direction::West,
            _ => {
                panic!(
                    "Unexpected byte ({}) for Direction (expected: ^,v,>,<)",
                    *b as char
                )
            }
        }
    }
}

#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
struct Point {
    x: isize,
    y: isize,
}

impl Point {
    // Mutate self
    fn move_in(&mut self, direction: Direction) {
        match direction {
            Direction::North => {
                self.y += 1;
            }
            Direction::South => {
                self.y -= 1;
            }
            Direction::East => {
                self.x += 1;
            }
            Direction::West => {
                self.x -= 1;
            }
        }
    }
}

fn solve_part1(bytes: &[u8]) -> usize {
    let mut santa_location = Point { x: 0, y: 0 };
    let mut locations_visited = HashSet::new();
    locations_visited.insert(santa_location);
    for b in bytes {
        santa_location.move_in(Direction::from_byte(b));
        locations_visited.insert(santa_location);
    }
    locations_visited.len()
}

fn solve_part2(bytes: &[u8]) -> usize {
    // There are now two Santas, that alternate
    let mut santas_locations = [Point { x: 0, y: 0 }, Point { x: 0, y: 0 }];
    let santa_count = santas_locations.len();
    let mut santa_id = 0;
    let mut locations_visited = HashSet::new();
    locations_visited.insert(santas_locations[santa_id]);
    for (index, b) in bytes.into_iter().enumerate() {
        santa_id = index % santa_count;
        santas_locations[santa_id].move_in(Direction::from_byte(b));
        locations_visited.insert(santas_locations[santa_id]);
    }
    locations_visited.len()
}

fn main() {
    let input = Input::File("../2015-03/input.txt");

    let start = std::time::Instant::now();
    let answer = solve_part1(input.string().as_bytes());
    let duration = start.elapsed();
    println!("2015 03 Part 1 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = solve_part2(input.string().as_bytes());
    let duration = start.elapsed();
    println!("2015 03 Part 2 = {} in {:?}", answer, duration);
}

#[test]
fn test_2015_03a1() {
    let input = Input::Const(">");
    let result = solve_part1(input.string().as_bytes());
    assert_eq!(result, 2)
}

#[test]
fn test_2015_03a2() {
    let input = Input::Const("^>v<");
    let result = solve_part1(input.string().as_bytes());
    assert_eq!(result, 4)
}

#[test]
fn test_2015_03a3() {
    let input = Input::Const("^v^v^v^v^v");
    let result = solve_part1(input.string().as_bytes());
    assert_eq!(result, 2)
}

#[test]
fn test_2015_03b1() {
    let input = Input::Const("^v");
    let result = solve_part2(input.string().as_bytes());
    assert_eq!(result, 3)
}

#[test]
fn test_2015_03b2() {
    let input = Input::Const("^>v<");
    let result = solve_part2(input.string().as_bytes());
    assert_eq!(result, 3)
}

#[test]
fn test_2015_03b3() {
    let input = Input::Const("^v^v^v^v^v");
    let result = solve_part2(input.string().as_bytes());
    assert_eq!(result, 11)
}
