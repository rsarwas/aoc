fn main() {
    let start = std::time::Instant::now();
    let data = std::fs::read_to_string("/Users/regan/MyRepos/aoc/2021-03/input.txt")
        .expect("Unable to create String from input.txt");
    let time1 = start.elapsed();
    println!("Read file in {:?}", time1);
    let codes = parse_input(&data);
    println!("Parse file in {:?}", start.elapsed() - time1);

    let start = std::time::Instant::now();
    let (epsilon, gamma) = find_common(&codes, 12);
    let answer = epsilon * gamma;
    let duration = start.elapsed();
    println!("2021 03 Part 1 = {} in {:?}", answer, duration);
}

// Use the most common and the least common bit at each index among all codes
// to create two new numbers, consider only the right most "bits"
fn find_common(codes: &Vec<u64>, bits: usize) -> (u64, u64) {
    let mut least = 0;
    let mut most = 0;
    let half_n = codes.len() / 2;
    //println!("bits = {}; n/2 = {}",bits, half_n);
    for index in 0..bits {
        let base = 1 << index;
        //println!("index = {}; base = {}",index, base);
        let mut ones = 0;
        for code in codes {
            if code & base == base {
                ones += 1
            }
        }
        //println!("ones = {}", ones);
        if ones > half_n {
            most |= base
        } else {
            least |= base
        }
    }
    (least, most)
}

fn parse_input(input: &str) -> Vec<u64> {
    let lines = input.lines();
    let codes = lines.map(|l| u64::from_str_radix(l, 2).expect("bad input"));
    codes.collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = "00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
";

    #[test]
    pub fn test2103a() {
        let codes = parse_input(TEST_INPUT);
        let (epsilon, gamma) = find_common(&codes, 5);
        assert_eq!(epsilon * gamma, 198);
    }
}
