fn what_floor(input: &String) -> isize {
    let mut floor:isize = 0;
    for ch in input.chars() {
        if "()".contains(ch) {
            floor += if ch == '(' { 1 } else { -1 };
        }
    }
    return floor
}

fn when_basement(input: &String) -> isize {
    let mut floor:isize = 0;
    let mut position:isize = 0;
    for ch in input.chars() {
        if "()".contains(ch) {
            position += 1;
            if ch == '(' { floor += 1 } else { floor -= 1 };
            if floor == -1 {
                return position
            }
        }
    }
    return -1
}

fn main() {
    use std::io;

    let mut input = String::new();
    match io::stdin().read_line(&mut input) {
        Ok(_) => {
            println!("Part 1: {}", what_floor(&input));
            println!("Part 2: {}", when_basement(&input));
        }
        Err(error) => println!("error: {}", error),
    }
}