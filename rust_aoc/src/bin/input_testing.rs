// Goal to create a Type that can 
// yield a stream of characters or lines from: 1) string literal, 2) stdin, or 3) contents of filename
// parser: consume a stream of characters or lines and yield a stream of model objects
// solver: consume a stream of model objects and return a result

// The different types of input I will support
pub enum Input {
    Const(&'static str),
    File(&'static str),
    Stdin
    //Http(url)
}

// I want to create a method on the input tpe that returns an
// sequence of strings.  However, I am unable to figure out how
// to make it work.  Most attempts fail because each Type created
// from the different input types is different even though they all
// impl Iterator<Item: String>
// struct LineGen {
//     input: Input,
// }

// impl Input {
//     // Doesn't work, because the types return be each brach are different
//     // even though they all match the return type implementation
//     //fn lines(&self) -> impl Iterator<Item: String> {
//     fn lines(&self) -> String {
//         match self {
//             Input::Const(val) => {
//                 let data = String::from(*val);
//                 let cursor = Cursor::new(data);
//                 // Error return types are different even though they all impl Iterator<Item = String>
//                 // cursor.lines().map(|x| x.expect(""))
//                 cursor.lines().next().unwrap().expect("")
//             }, 
//             Input::File(file_name) => {
//                 let f = File::open(file_name).expect("Could not open file");
//                 let reader = BufReader::new(f);
//                 //reader.lines().map(|x| x.expect(""))
//                 reader.lines().next().unwrap().expect("")
//             },
//             Input::Stdin => {
//                 //io::stdin().lock().lines().map(|x| x.expect(""))
//                 io::stdin().lock().lines().next().unwrap().expect("")
//             }
//         }
//     }
// }

// Create a struct to own the data in the input (as a String)
// This type can return a char sequence and a line sequence
struct DataFeed {
    source: String
}

impl DataFeed {
    fn from(input: Input) -> DataFeed {
        let source = match input {
            Input::Const(s) => s.to_string(),
            Input::File(s) => std::fs::read_to_string(s).expect("Unable to read file"),
            // Crazy to read all the lines into a single string only export again as line
            // necessary because stdin().lines() is a different type than cursor.lines()
            Input::Stdin => std::io::stdin().lock().lines()
            .map(|x| x.expect("stdin fail"))
            .collect::<Vec<String>>().join("\n")
        };
        DataFeed {source: source }
    }

    fn chars(&self) -> std::str::Chars {
        self.source.chars()
    }
    fn lines(&self) -> Lines<Cursor<&String>>  {
        let cursor = Cursor::new(&self.source);
        cursor.lines()
    }
}

// Example of using the DataFeed
fn data_feed() {
    // Try an input option, by removing the leading underscore from it
    let input = Input::File("input.txt");
    let _input = Input::Const("lorem\nipsum\r\ndolor");
    let _input = Input::Stdin;

    // Read data as a sequence of characters
    let data = DataFeed::from(input);
    for ch in data.chars() {
        println!("{}", ch)
    }
    // Read data as a sequence of lines
    let lines = data.lines().map(|l| l.expect("input error"));
    for line in lines {
        println!("{}", line)
    }

}


// Alternate to DataFeed is to create a CharFeed that implements iter returning Some(&Char)
// and a LineFeed that implements iter returning Some(&str)
// basically next() has three mutually exclusive branches based on match source from Input
// usage:
// let input = Input::Const("my data string")
// for line in LineFeed(source: input) {}
// for char in CharFeed(source: input) {}


//Another option is to create a separate function for each input type
//TODO: create functions that return characters
use std::io::{self, StdinLock, BufReader, BufRead, Cursor, Result, Lines};
use std::fs::File;

fn read_file_lines(file_name: &str) -> Result<Lines<BufReader<File>>> {
    let f = File::open(file_name)?;
    let reader = BufReader::new(f);
    let lines = reader.lines();
    Ok(lines)
}

fn read_stdin_lines() -> Lines<StdinLock<'static>> {
    io::stdin().lock().lines()
}

fn test_lines(s: &str) -> Lines<Cursor<String>>  {
    let data = String::from(s);
    let cursor = Cursor::new(data);
    cursor.lines()
}

fn functions() {
    let lines = read_stdin_lines();
    let _lines = read_file_lines("test.txt").expect("unable to open input file");
    let _lines = test_lines("lorem\nipsum\r\ndolor");
    for line in lines {
        println!("line {}", line.unwrap())
    }
}

fn main() {
    data_feed();
    functions();
}
