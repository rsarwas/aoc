fn test() {
    let numbers = vec!["-17", "99", "-27", "+68"];
    let answer = numbers
        .into_iter()
        .map(|x| str::parse::<i32>(x).expect("Token is not an int"))
        .sum::<i32>();
    println!("Total is {}", answer);
}

fn read_stdin() {
    use std::io::BufRead; // trait required for lines() method
    let answer =
        std::io::stdin()
            .lock()
            .lines() // The BufRead iterator yields io::Result<String> without the newline (\r\n or \n) at end
            .map(|x| {
                // x is Result<&str, _>
                x.expect("Error reading input line")
                    .parse::<i32>()
                    .expect("Line is not an integer")
            })
            .sum::<i32>();
    println!("Total is {}", answer);
}

fn read_file() {
    use std::io::BufRead; // trait required for lines() method
    let f = std::fs::File::open("input.txt").expect("Unable to open file");
    let reader = std::io::BufReader::new(f);
    let answer = reader
        .lines() //   // The BufRead iterator yields io::Result<String> without the newline (\r\n or \n) at end
        .map(|x| {
            // x is Result<&str, _>
            x.expect("Error reading input line")
                .parse::<i32>()
                .expect("Line is not an integer")
        })
        .sum::<i32>();
    println!("Total is {}", answer);
}

fn read_str() {
    let data =
        std::fs::read_to_string("input.txt").expect("Unable to create String from input.txt");
    let answer = data
        .lines() // The String iterator yields &str without the newline (\r\n or \n) at end
        .map(|x| x.parse::<i32>().expect("Line is not an integer"))
        .sum::<i32>();
    println!("Total is {}", answer);
}

fn main() {
    // test with hard coded data
    //test();

    // read stdin line by line
    //read_stdin();

    // read file line by line and process
    //read_file();

    // read entire file into a single String
    read_str();
}

// Tried to create a function that takes an "iterable" IntoIterator trait, so that
// I can implement the solution logic on a file, stdin, String::lines(), or a test vector
// I was able to write a working version that takes ownership of a Vec<&str>,
// but could not figure out how to do a borrowing version
// The BufRead::lines() yields an iterator on io::Result<String>, so it will need to be unwrapped first

/*
//fn part1<'a, T: Iterator<Item = &'a str>>(lines: &T) -> Result<i32, std::num::ParseIntError> {
fn part1<T>(lines: T) -> Result<i32, std::num::ParseIntError>
where
    T: IntoIterator,
    T::Item: FromStr,
    {
    lines.into_iter()
    .map(|x| i32::from_str(x))
    //.map(i32::from_str) //requires use std::str::FromStr;
    //.map(std::str::parse::<i32>())
    .sum()
}

// Consumes lines, I cannot figure our how to borrow lines
fn test2<'a, T>(lines: T) -> Result<i32, std::num::ParseIntError>
where
T: IntoIterator<Item = &'a str> // if the Item constraint is a type
// T: IntoIterator, T::Item = std::fmt::Debug // if the Item constraint is a trait
{
    lines.into_iter().map(|x| str::parse::<i32>(x)).sum()
    }

fn test() {
    let numbers = vec!["-17", "99", "-27", "+68"];


    //let a = (&numbers).into_iter();
    //println!("{:#?}", a);
    //for i in a { println!("{}", i); }
    //println!("{:#?}", &numbers);
    let answer: Result<i32, std::num::ParseIntError> = test2(numbers);
    //let answer: Result<i32, std::num::ParseIntError> = test2((&numbers).into_iter());
    println!("Total is {:#?}", answer);
    //test2(numbers);
    //println!("{:#?}", numbers);
    //let answer: Result<i32, std::num::ParseIntError> = test2(a);

    /*
    let answer: Result<i32, std::num::ParseIntError> = part1((&numbers).into_iter());
    println!("Total is {:#?}", answer);
    let answer: Result<i32, std::num::ParseIntError> = part1((&numbers).into_iter());
    println!("Total is {:#?}", answer);
    */
}

*/
