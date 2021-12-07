fn main() {
    let start = std::time::Instant::now();
    let data = std::fs::read_to_string("../2021-06/input.txt").expect("Unable to create String from input.txt");
    println!("Read file in {:?}", start.elapsed());

    let start = std::time::Instant::now();
    let timers = parse(&data);
    //println!("timer = {:#?}", timers);
    let duration = start.elapsed();
    println!("Parse file in {:?}", duration);

    let start = std::time::Instant::now();
    let answer = count_fish(timers, 80);
    let duration = start.elapsed();
    println!("2021 day 06 Part 1 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = count_fish(timers, 256);
    let duration = start.elapsed();
    println!("2021 day 06 Part 2 = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = count_fish2(timers, 80);
    let duration = start.elapsed();
    println!("2021 day 06 Part 1+ = {} in {:?}", answer, duration);

    let start = std::time::Instant::now();
    let answer = count_fish2(timers, 256);
    let duration = start.elapsed();
    println!("2021 day 06 Part 2+ = {} in {:?}", answer, duration);
}

fn parse(data: &str) -> [usize;9] {
    let mut timers: [usize;9] = [0;9];
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
    timers
}

fn count_fish(mut timers: [usize;9], days: usize) -> usize {
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

fn count_fish2(mut timers: [usize;9], days: usize) -> usize {
    // Everyday, the data in i+1 goes to i and 0 goes to n
    // If we think of the list as a circle, nothing changes
    // (except the spawning fish are added again),
    // the index of the spawning fish is the day number modulo 9
    // This reduces the number of operations per day from 30 to 9
    //
    // However:
    //  reading the file takes ~594µs +/- 179µs
    //  parsing the string to integer data takes about 4.6µs
    //  counting the old way takes about 0.32µs and 0.28µs this way (for 80 days)
    //  So we have improved efficiency by 12% in 0.05% of the problem
    //  A great example of an unnecessary optimization.
    // This solution may be easier to read/understand
    for i in 0..days {
        let start = i % 9;
        let restart = (start + 7) % 9;
        timers[restart] += timers[start];
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
        assert_eq!(count_fish2(parse(TEST_INPUT), 18), 26);
    }
    #[test]
    pub fn test2106b() {
        assert_eq!(count_fish2(parse(TEST_INPUT), 80), 5934);
    }
    #[test]
    pub fn test2106c() {
        assert_eq!(count_fish2(parse(TEST_INPUT), 256), 26984457539);
    }

}
