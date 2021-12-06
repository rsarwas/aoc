fn main() {
    let start = std::time::Instant::now();
    let data = std::fs::read_to_string("../2021-06/input.txt").expect("Unable to create String from input.txt");
    println!("Parse file in {:?}", start.elapsed());

    let start = std::time::Instant::now();
    let answer = count_fish(&data, 80);
    let duration = start.elapsed();
    println!("2021 day 06 Part 1 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = count_fish(&data, 256);
    let duration = start.elapsed();
    println!("2021 day 06 Part 2 = {} in {:?}", answer, duration);
}

fn count_fish(data: &str, days: usize) -> usize {
    let mut timers = [0;9];
    // initialize with data
    for byte in data.bytes() {
        match byte {
            b'1' => timers[1] += 1,
            b'2' => timers[2] += 1,
            b'3' => timers[3] += 1,
            b'4' => timers[4] += 1,
            b'5' => timers[5] += 1,
            b'6' => timers[6] += 1,
            b',' => (),
            b'\n' => (),
            _ => println!("Unexpected character '{}'", byte) 
        }
    }
    //println!("timer = {:#?}", timers);
    for _ in 0..days {
        let zeros = timers[0];
        for i in 0..8 {
            timers[i] = timers[i+1];
        }
        timers[6] += zeros;
        timers[8] = zeros;
    }
    timers.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = "3,4,3,1,2
";

    #[test]
    pub fn test2106a() {
        assert_eq!(count_fish(TEST_INPUT, 18), 26);
    }
    #[test]
    pub fn test2106b() {
        assert_eq!(count_fish(TEST_INPUT, 80), 5934);
    }
    #[test]
    pub fn test2106c() {
        assert_eq!(count_fish(TEST_INPUT, 256), 26984457539);
    }

}
