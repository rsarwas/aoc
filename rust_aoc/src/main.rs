// set cwd to the folder with cargo.toml
// test all: cargo test
// test 1: cargo test -- --nocapture test1a
// results: cargo run
// timing: cargo run --release

fn main() {
    let start = std::time::Instant::now();
    let data = std::fs::read_to_string("../2021-01/input.txt")
        .expect("Unable to create String from input.txt");
    let duration = start.elapsed();
    println!("Read input in {:?}", duration);

    let start = std::time::Instant::now();
    let answer = find_sleigh_keys1(&data);
    let duration = start.elapsed();
    println!("2021 01 Part 1 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = find_sleigh_keys1a(&data);
    let duration = start.elapsed();
    println!("2021 01 Part 1 alt = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = find_sleigh_keys2(&data);
    let duration = start.elapsed();
    println!("2021 01 Part 2 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = find_sleigh_keys2a(&data);
    let duration = start.elapsed();
    println!("2021 01 Part 2alt = {} in {:?}", answer, duration);
}

use std::str::FromStr;

/// Input an array of utf8 bytes in the ASCII range (i.e. 1 byte per character)
/// The input can be divided into lines at each newline character (\n = 10, no \r = 13)
/// Each line contains a single positive number in base 10 less than 10,000.

//fn find_sleigh_keys(input: &[u8]) -> usize {
//    let lines = std::str::from_utf8(input).expect("input is not a string").lines();

fn find_sleigh_keys1(input: &str) -> usize {
    let lines = input.lines();
    let depths = lines.map(|x| u32::from_str(x).expect("Input is not a number"));
    let mut inc: usize = 0;
    let mut last_depth = u32::MAX;
    for depth in depths {
        if depth > last_depth {
            inc += 1;
        }
        last_depth = depth;
    }
    inc
}

// Using reduce, as below, is slower than looping on depth as above
fn find_sleigh_keys1a(input: &str) -> usize {
    let lines = input.lines();
    let depths = lines.map(|x| u32::from_str(x).expect("Input is not a number"));
    let (inc, _) =
        depths.fold((0, u32::MAX), |(inc, last_depth), depth| {
            if depth > last_depth {
                (inc + 1, depth)
            } else {
                (inc, depth)
            }
        });
    inc
}

fn find_sleigh_keys2(input: &str) -> usize {
    let lines = input.lines();
    // I need to collect the ints into a vector, so that it can be referenced
    // 3 times for the zip below. Without collect() the resulting iterator cannot
    // be copied (referenced multiple times)
    // Once it is a vector on the heap, I can index the elements and skip the zip.
    let depths: Vec<u32> = lines
        .map(|x| u32::from_str(x).expect("Input is not a number"))
        .collect();
    let avg_depths = depths
        .iter()
        .zip(depths.iter().skip(1).zip(depths.iter().skip(2)))
        .map(|(d1, (d2, d3))| d1 + d2 + d3);
    let mut inc: usize = 0;
    let mut last_depth = u32::MAX;
    for depth in avg_depths {
        if depth > last_depth {
            inc += 1;
        }
        last_depth = depth;
    }
    inc
}

// Indexing the vector (as below) is slower than the iterator approach above
fn find_sleigh_keys2a(input: &str) -> usize {
    let lines = input.lines();
    // I need to collect the ints into a vector, so that it can be referenced
    // 3 times for the zip below. Without collect() the resulting iterator cannot
    // be copied (referenced multiple times)
    // Once it is a vector on the heap, I can index the elements and skip the zip.
    let depths: Vec<u32> = lines
        .map(|x| u32::from_str(x).expect("Input is not a number"))
        .collect();
    let mut inc: usize = 0;
    let mut last_depth = u32::MAX;
    for i in 0..depths.len() - 2 {
        let depth = depths[i] + depths[i + 1] + depths[i + 2];
        if depth > last_depth {
            inc += 1;
        }
        last_depth = depth;
    }
    inc
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = "199
200
208
210
200
207
240
269
260
263
";

    #[test]
    pub fn test1() {
        assert_eq!(find_sleigh_keys1(TEST_INPUT), 7);
    }
    #[test]
    pub fn test1a() {
        assert_eq!(find_sleigh_keys1a(TEST_INPUT), 7);
    }
    #[test]
    pub fn test2() {
        assert_eq!(find_sleigh_keys2(TEST_INPUT), 5);
    }
    #[test]
    pub fn test2a() {
        assert_eq!(find_sleigh_keys2a(TEST_INPUT), 5);
    }
}
