Advent of Code
==============

A project to solve the
[advent of code](https://adventofcode.com)
problems with various programming languages.

C/C++
-----
```sh
clang answers.c && ./a.out < input.txt && rm a.out
```

C# (mono)
---------
```sh
csc answers.cs && mono answers.exe < input.txt && rm answers.exe
```

Go
---
```sh
go run answers.go < input.txt
```

Haskell
-------
```sh
ghc answers.hs && ./answers < input.txt && rm answers answers.hi answers.o
```

Java
----
```sh
java answers.java < input.txt
```

Javascript (node)
-----------------
```sh
node answers.js < input.txt
```

Julia
-----
```sh
julia answers.jl < input.txt
```

Python
------
```sh
python3 answers.py < input.txt
```

Rust
----
```sh
rustc answers.rs && ./answers < input.txt && rm answers
```

Swift
-----
```sh
swiftc answers.swift && ./answers < input.txt && rm answers
```

Typescript
----------

Project based approach
======================

See `swiftAOC\Readme.md` for details of a swift solution to solve all puzzles
with a framework or package based approach.

## dotnet
`dotnet new console -o dotnetAOC; cd dotnetAOC`
`dotnet run`
