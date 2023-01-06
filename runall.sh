# Run all versions of a solution in the current folder
echo
echo "C/C++"
clang answers.c && ./a.out < input.txt && rm a.out
echo
echo "C# (mono)"
csc answers.cs && mono answers.exe < input.txt && rm answers.exe
echo
echo "dart"
dart run answers.dart < input.txt
echo
echo "Go"
go run answers.go < input.txt
echo
echo "Haskell"
ghc answers.hs && ./answers < input.txt && rm answers answers.hi answers.o
echo
echo "Java"
java answers.java < input.txt
echo
echo "Javascript (node)"
node answers.js < input.txt
echo
echo "Julia"
julia answers.jl < input.txt
echo
echo "Python"
python answers.py < input.txt
echo
echo "Rust"
rustc answers.rs && ./answers < input.txt && rm answers
echo
echo "Swift"
swiftc answers.swift && ./answers < input.txt && rm answers
echo
echo "Typescript"
echo "** TODO **"
