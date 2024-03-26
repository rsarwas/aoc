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

// Despite the cost of allocating a Vector
// it is about twice as fast to process the input in Packages once

// fn solve(input: &[u8]) {
//     let start = std::time::Instant::now();
//     let total_paper = input
//         .split(|&c| c == b'\n')
//         .flat_map(|present| Package::new(present))
//         .fold(0, |acc, p| acc + p.paper());
//     let total_ribbon = input
//         .split(|&c| c == b'\n')
//         .flat_map(|present| Package::new(present))
//         .fold(0, |acc, p| acc + p.ribbon());
//     let duration = start.elapsed();
//     println!("Solved in {:?}", duration);

//     println!("Part 1: {}", total_paper);
//     println!("Part 1: {}", total_ribbon);
// }

/// Generic Solver and result printer
fn solve(input: &[u8]) {
    //let start = std::time::Instant::now();
    // Create a Vector of Packages from the input. Invalid input is ignored.
    let packages: Vec<Package> = input
        .split(|&c| c == b'\n')
        .flat_map(|present| Package::new(present))
        .collect();
    let total_paper = packages.iter().fold(0, |acc, p| acc + p.paper());
    let total_ribbon = packages.iter().fold(0, |acc, p| acc + p.ribbon());
    // let duration = start.elapsed();
    // println!("Solved in {:?}", duration);

    println!("Part 1: {}", total_paper);
    println!("Part 1: {}", total_ribbon);
}
struct Package {
    width: u32,
    height: u32,
    length: u32,
}

use std::cmp::min;

impl Package {
    fn paper(&self) -> u32 {
        self.surface_area() + self.smallest_side_area()
    }

    fn surface_area(&self) -> u32 {
        2 * self.side1_area() + 2 * self.side2_area() + 2 * self.side3_area()
    }

    fn smallest_side_area(&self) -> u32 {
        min(min(self.side1_area(), self.side2_area()), self.side3_area())
    }

    fn side1_area(&self) -> u32 {
        self.height * self.length
    }

    fn side2_area(&self) -> u32 {
        self.length * self.width
    }

    fn side3_area(&self) -> u32 {
        self.width * self.height
    }

    fn ribbon(&self) -> u32 {
        self.volume() + self.smallest_side_perimeter()
    }

    fn volume(&self) -> u32 {
        self.width * self.height * self.length
    }

    fn smallest_side_perimeter(&self) -> u32 {
        min(
            min(self.side1_perim(), self.side2_perim()),
            self.side3_perim(),
        )
    }

    fn side1_perim(&self) -> u32 {
        2 * (self.height + self.length)
    }

    fn side2_perim(&self) -> u32 {
        2 * (self.length + self.width)
    }

    fn side3_perim(&self) -> u32 {
        2 * (self.width + self.height)
    }

    /// Returns an Optional Package from a slice of bytes
    ///
    /// Bytes are assumed to be ASCII with three integers
    /// separated by 'x'.  E.g. b'3x4x15'
    /// While it doesn't really matter the digits will map to the
    /// height, length and width in that order.
    /// Will return None if it cannot find exactly three integers in the input
    fn new(definition: &[u8]) -> Option<Package> {
        if definition.len() < 5 {
            return None;
        }
        // FIXME: Remove use of Vector (unnecessary memory allocation)
        let dims: Vec<u32> = definition
            .split(|c| *c == b'x')
            .map(|bytes| {
                let the_string = std::str::from_utf8(bytes).unwrap_or("0");
                let number: u32 = the_string.parse().unwrap_or(0);
                number
            })
            .collect();
        if dims.len() != 3 {
            return None;
        }
        if dims[0] == 0 || dims[1] == 0 || dims[2] == 0 {
            return None;
        }
        Some(Package {
            height: dims[0],
            length: dims[1],
            width: dims[2],
        })
    }
}
